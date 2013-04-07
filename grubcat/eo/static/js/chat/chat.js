var $commonData = $("#common-data");
var chatServer = $commonData.data("chat-server")
var chatServerDomain ="@" + $commonData.data("chat-domain")
var myTemplate = {
    tplContactItem: '<div class="avatar"><img src="<%= avatarUrl%>" alt="<%= name %>" title="<%= name %>"/></div>' +
        '<div class="nickname"><%= name %></div>' +
        '<div class="unread-count"><%=unReadCount%></div>' +
        '<% if( typeof body != "undefined" ) { %><div class="last-message"><%- body %></div><% } %>',
    tplChatBox: '<div class="chat-title"><a href="<%=profileUrl%>" target="_blank" >' +
        '           <img class="avatar" src="<%= avatarUrl%>" alt="<%= name %>" title="<%= name %>">' +
        '           <span class="name"><%=name%></span></a>' +
        '       </div>' +
        '            <div class="chat-message-container">' +
        '                <div class="message-list"><a class="more-history" href="#">查看更多消息</a></div>' +
        '           <div class="chat-status">对方正在输入...</div>' +
        '       </div>' +
        '   <div class="chat-editor">' +
        '           <textarea type="text" class="chat-input" rows="2" ></textarea>' +
        '       <button class="btn btn-primary btn-send">发送</button>' +
        '       </div>',
    tplMessageItem:
        '<% if(typeof formattedTime != "undefined"){  %>' +
        '<div class="message-time-wrapper"><div class="message-time"><span class="time-span left"/><%=formattedTime%><span class="time-span right"/></div></div>' +
        '<% } %>' +
        '<a href="<%=profileUrl%>" target="_blank" ><img class="avatar" src="<%= avatarUrl%>" alt="<%= name %>" title="<%= name %>"></a>' +
        '<div class="message-content"><div class="message-text"><%- body%></div><div class="message-arrow"></div></div>'
}
$(function () {
    $(document).trigger('connect', {
        jid: $commonData.data("uid")+chatServerDomain,
        password: $commonData.data("pwd")
    });

})

$(document).bind('connect', function (ev, data) {
    var conn = new Strophe.Connection(chatServer);

    conn.xmlInput = function (elem) {
//        if($(elem).find("chat")[0]){
            chatApp.debug(elem)
//        }
    }
    conn.xmlOutput = function (elem) {
//        if($(elem).find("retrieve")[0]){
            chatApp.debug(elem)
//        }
    }

    conn.connect(data.jid, data.password, function (status) {
        if (status === Strophe.Status.CONNECTED) {
            $(document).trigger('connected');
        } else if (status === Strophe.Status.DISCONNECTED) {
            $(document).trigger('disconnected');
            chatApp.connection = null;
        }
    });

    chatApp.connection = conn;
});

var $chatData = $("#chat-data");

//contact
var Contact = Backbone.Model.extend({
    defaults: {
//        jid: "",
        show: "offline",
        name: "",
        isTyping: false,
        unReadCount: 0,
        current: false, // is current chat user
        avatarUrl: $chatData.data("default-avatar"),
        profileUrl: "",
        hasMoreUnReadMessages: true,
        hasMoreReadMessages: false
        //other attributes, profileUrl,tags
    },

    initialize:function(){
        this.messages = new MessageCollection();
    },

    url: $chatData.data("get-user-info-url"),

    addMessage: function(msg){ //Message
        if (msg.isIn()) //msg in
        {
            var sender = msg.sender
            if (!msg.get("isRead")) {
                if (chatApp.isWindowFocused && sender.get("current")) {
                    sender.sendReceivedRecipts();
                } else {
                    sender.increaseUnReadCount(1);
                }
            }
        }
        this.messages.add(msg);
    },

    retrieveUnReadMessages: function(){
        var before = this.messages.length > 0 ? this.messages.first().get("timestamp").getTime() : ""
        var user = this
        this.retrieveMessages(before, function () {
            if (user.get("hasMoreUnReadMessages")) {
                user.retrieveUnReadMessages()
            }
        })
    },

    retrieveMessages: function(before, callback){
        var user = this, max = 10, rsm = new Strophe.RSM({max: max, before: before||""})
        chatApp.connection.archive.retrieveMessages(this.get("jid"), rsm , function(messages, rsm, hasMoreMessages){
            var hasMoreUnReadMessages = hasMoreMessages;
            _.each(messages, function (oldMsg) { //from old to new
                var msg = new Message({
                    from: Strophe.getNodeFromJid(oldMsg.from),
                    to: Strophe.getNodeFromJid(oldMsg.to),
                    body: oldMsg.body,
                    timestamp: oldMsg.timestamp,
                    isRead: oldMsg.isRead
                })
                if (hasMoreUnReadMessages && msg.sender == chatApp.myProfile || oldMsg.isRead) {
                    hasMoreUnReadMessages = false;
                }
                if (msg.isIn() && msg.sender) {
                    msg.sender.addMessage(msg);
                } else if (!msg.isIn() && msg.receiver) {
                    msg.receiver.addMessage(msg);
                }
            })
            user.set("hasMoreUnReadMessages", hasMoreUnReadMessages)
            user.set("hasMoreReadMessages", hasMoreMessages)
            callback && callback()
        });
    },

    increaseUnReadCount: function( num){
        var unReadCount = this.get("unReadCount");
        this.set("unReadCount",unReadCount + num);
        chatApp.totalUnReadCount += num;

        var $totalUnReadCount = $("#total-unread-count");
        $totalUnReadCount.text(chatApp.totalUnReadCount).show();

        if(!chatApp.unReadMsgInterval){
            chatApp.unReadMsgInterval = setInterval(function(){
                if( chatApp.totalUnReadCount > 0){
//                    if( $("title").text() == chatApp.orignalWindowTitle){
//                        $("title").text('您有' + chatApp.totalUnReadCount + '条未读消息')
//                    } else {
//                        $("title").text(chatApp.orignalWindowTitle);
//                    }
                    $totalUnReadCount.is(":visible") ? $totalUnReadCount.hide() : $totalUnReadCount.show();
                } else {
//                    $("title").text(chatApp.orignalWindowTitle);
                    $totalUnReadCount.hide();
                }
            }, 1000)
        }
    },

    clearUnReadCount: function(){
        var unReadCount = this.get("unReadCount");
        if (unReadCount) {
            this.sendReceivedRecipts();
            this.set("unReadCount", 0);

            chatApp.totalUnReadCount -= unReadCount;
            $("#total-unread-count").text(chatApp.totalUnReadCount)
            if (chatApp.totalUnReadCount == 0) {
                $("#total-unread-count").hide();
//                $("title").text(chatApp.orignalWindowTitle);
            }
        }
    },

    sendReceivedRecipts: function(){
        var out = $msg({to: this.get("jid")}).c("received", {'xmlns': "urn:xmpp:receipts", 'id': 1});
        chatApp.connection.send(out);
    }
});

var ContactCollection = Backbone.Collection.extend({
    model: Contact ,
    url: $chatData.data("get-user-info-url"),
    getCurrentUser: function(){
        return this.findWhere({current: true});
    }
});

var ContactItemView = Backbone.View.extend({

    tagName: "div",

    className: "contact-item",

    id: function(){
      return "contact-" + this.model.id;
    },

    template: _.template(myTemplate.tplContactItem),

    initialize: function () {
        this.listenTo(this.model, "change", this.render);
        this.listenTo(this.model.messages, "add", this.render);
        this.listenTo(this.model, "destory", this.close);
    },
    close: function () {
        this.$el.unbind();
        this.$el.remove();
    },
    render: function () {
        var messages = this.model.messages,
            lastMsg, lastMsgJson;
        if (messages.length) {
            lastMsg = messages.last()
            lastMsgJson = {"body": lastMsg.get("body").slice(0, 20), "timestamp": lastMsg.get("timestamp").getTime()}
        } else {
            lastMsgJson = {}
        }
        this.$el.html(this.template(_.extend({},this.model.attributes, lastMsgJson ))).removeClass("online offline").addClass(this.model.get("show"));
        if(this.model.get("current")){
            this.$el.addClass("current")
        } else {
            this.$el.removeClass("current")
        }
        if(this.model.get("unReadCount") > 0){
            this.$el.find(".unread-count").show();
        } else {
            this.$el.find(".unread-count").hide();
        }

        return this;
    },

    events: {
        "click": "openChat"
    },

    openChat: function (event) {
        if(!chatApp.hasAvatar()){
            $("#no-avatar-tip").show();
            return false;
        }
        var beforeUser = chatApp.contactList.getCurrentUser()
        beforeUser && beforeUser.set("current", false)

        var currentUID = $(event.currentTarget).attr("id").replace("contact-","")
        var currentUser = chatApp.contactList.get(currentUID)
        currentUser.set("current", true)
        //send received
        currentUser.clearUnReadCount();
        return false;
    }

});
var ContactListView = Backbone.View.extend({

    el: "#roster",

    initialize: function () {
        this.itemViewList = [];
        this.model.each(function(contact){
            var contactItemView = new ContactItemView({model: contact});
            this.itemViewList.push(contactItemView);

            this.listenTo(contact.messages, "sort add", function(){
                this.sortContacts()
                this.render();
            })

        }, this)

        this.listenTo(this.model, "change", this.render)
        this.listenTo(this.model, "change:show", function(){
            this.sortContacts()
            this.render()
        })
        this.listenTo(this.model, "add", function (contact) {
            if ($("#no-roster-tip")[0]) {
                $("#no-roster-tip").remove()
                $("#chat-left-column, #chat-right-column").show()
            }
            var contactItemView = new ContactItemView({model: contact});
            this.itemViewList.push(contactItemView);
            this.sortContacts()
            this.render()
        });
        this.sortContacts()
        this.render()
    },

    render: function () {
        _.each(this.itemViewList, function (contactView) {
            this.$el.prepend(contactView.el);
        }, this);
        this.$el.children().removeClass("first").first().addClass("first")
        if (this.$el.children().size() == 9) {

            this.$el.children().removeClass("last").last().addClass("last")
        }
        return this;
    },

    sortContacts: function(){
        this.itemViewList = _.sortBy(this.itemViewList, function(view){
            var messages = view.model.messages
            return   messages.length ? messages.last().get("timestamp").getTime() : (view.model.get("show") == "online" ? 1 : 0)
        })
    }

});

var Message = Backbone.Model.extend({
    defaults: {
        isRead: false
    },

    initialize: function(){
        var fromUID = this.get("from"), toUID = this.get("to")
        if(chatApp.contactList.get(fromUID)){
            this.sender = chatApp.contactList.get(fromUID)
        } else if(fromUID == chatApp.myProfile.id ){
            this.sender = chatApp.myProfile
        } else {
            this.sender = chatApp.createContact(fromUID + chatServerDomain)
            this.sender.retrieveUnReadMessages()
        }
        if(chatApp.contactList.get(toUID)){
            this.receiver = chatApp.contactList.get(toUID)
        } else if(toUID == chatApp.myProfile.id ){
            this.receiver = chatApp.myProfile
        } else {
            this.receiver = chatApp.createContact(toUID + chatServerDomain)
            this.receiver.retrieveUnReadMessages()
        }

    },
    shouldShowTime: function(){
        var list = this.collection, index = list.indexOf(this), previousMsg, ifShowTime = false;
        if(index > 0){
            previousMsg = list.at(index-1);
            (this.get("timestamp")-previousMsg.get("timestamp"))/1000/60 >= 15 && (ifShowTime = true); // show time if time gaps > 10 minutes
        } else if( index == 0){
            ifShowTime = true;
        }
        return ifShowTime

    },

    isIn: function(){
        return this.get("from") != chatApp.myProfile.id
    }
    // sender, receiver, body, timestamp
    //from: fromUID, //who I am chatting with
})

var MessageCollection = Backbone.Collection.extend({
    model: Message,

    comparator: function(msg){
        return msg.get("timestamp").getTime();
    }

})

var MessageItemView = Backbone.View.extend({

    tagName: "div",
    className: "message-item",
    template: _.template(myTemplate.tplMessageItem),

    initialize: function(){
      this.listenTo(this.model, "change:shouldScrollIntoView",function(){
          if (this.model.get("shouldScrollIntoView")) {
              this.el.scrollIntoView(false)
              var $list = this.$el.parents(".message-list")
              $list.scrollTop($list.scrollTop() + 55)
          }
      })
    },

    render: function () {
        var extraAttrs = {}
        if(this.model.shouldShowTime()){
            extraAttrs["formattedTime"] = this.formatTime(this.model.get("timestamp"))
        }
        this.$el.html(this.template(_.extend({}, this.model.attributes, this.model.sender.attributes, extraAttrs))).addClass(this.model.isIn() ? "others": "me")
        return this;
    },

    formatTime: function(date){
        var today = new ServerDate()
        var d1, d2, dayGap, resultTime=date.getHourMinute()/* + "." + date.getMilliseconds()*/, resultDate;
        d1 = new Date(date.getFullYear(), date.getMonth(), date.getDate());
        d2 = new Date(today.getFullYear(), today.getMonth(), today.getDate());
        dayGap = Math.abs(d1 - d2)/1000/60/60/24
        if (dayGap == 0) {
            resultDate = ""
        } else if (dayGap == 1) {
            resultDate = "昨天"
        } else if (dayGap == 2){
            resultDate = "前天"
        }  else {
            resultDate = date.getTwoDigitMonth() + "-" + date.getTwoDigitDate()
        }
        return resultDate + " " + resultTime;
    }
})



//model Contact
var ChatBoxView = Backbone.View.extend({

    tagName: "div",
    className: "chat-box",
    template: _.template(myTemplate.tplChatBox),

    initialize: function () {
        this.listenTo(this.model, "change:current change:isTyping change:name change:hasMoreReadMessages change:hasMoreUnReadMessages", this.render);
        this.listenTo(this.model.messages, "add", this.addMessageView);
        this.$el.html(this.template(this.model.attributes));

    },

    addMessageView: function(msg, msgCollection){
        var msgItemEl = new MessageItemView({model:msg}).render().el
        var index = msgCollection.indexOf(msg)
        if( index == 0){
            this.$(".message-list .more-history").after(msgItemEl)
        } else {
            this.$(".message-list .message-item:eq(" + (index-1) + ")").after(msgItemEl)
            if(index + 1 < msgCollection.length && !msgCollection.at(index+1).shouldShowTime()){
             this.$(".message-list .message-item:eq(" + (index+1) + ")").find(".message-time-wrapper").hide()
            }
        }

    },

    render: function () {
        if (this.model.hasChanged("name")) {
            var $mesageList = this.$(".message-list");
            this.$el.html(this.template(this.model.attributes));
            $mesageList[0] && this.$(".message-list").replaceWith($mesageList)
        }

        if(this.model.hasChanged("hasMoreUnReadMessages") || this.model.hasChanged("hasMoreReadMessages")){
            if(!this.model.get("hasMoreUnReadMessages") && this.model.get("hasMoreReadMessages")){
                this.$(".more-history").show()
            } else {
                this.$(".more-history").hide()
            }
        }

        var show = this.model.get("current");
        if (this.model.hasChanged("current")) {
            if (show) {
                this.$el.show()
                this.$el.find(".chat-input").focus();
            } else {
                this.$el.hide();
            }
            this._scrollChatToBottom()
        }
        show && this.model.get("isTyping") ? this.$el.find(".chat-status").css('visibility','visible') : this.$el.find(".chat-status").css('visibility','hidden');

        return this;
    },

    events: {
        "keypress .chat-input": "keyPressed",
        "focusout .chat-input": "sendPausedStatus",
        "click .btn-send": "sendMessage",
        "click .more-history": "getMoreHistory"
    },

    keyPressed: function(ev){
        if (ev.which === 13) {
            ev.preventDefault();
            this.sendMessage();
            this.sendPausedStatus();
        } else {
            if(!chatApp.checkConnection()){
                return
            }
            this.sendTypingStatus();
        }
    },
    sendMessage: function () {
        var $chatInput = this.$el.find(".chat-input");
        var body = $chatInput.val();
        if (!body){
            return false;
        }
        $chatInput.val("");
        if(!chatApp.checkConnection()){
            return false
        }
        var currentUser = chatApp.contactList.getCurrentUser()
        chatApp.connection.message.send(currentUser.get("jid"), body)
        currentUser.addMessage(new Message({
            from: chatApp.myProfile.id,
            to: currentUser.id,
            body: body,
            timestamp: new ServerDate()
        }))
        this._scrollChatToBottom()
        $("#chat-left-column").scrollTop(0)
        return false;
    },

    sendTypingStatus: function(){
        if( !chatApp.myProfile.get("isTyping") ){ // previous not typing
            chatApp.connection.chatstates.sendComposing(chatApp.contactList.getCurrentUser().get("jid"), "chat");
            chatApp.myProfile.set("isTyping", true)
        }
        if (chatApp.statesTimeOut) {
            clearTimeout(chatApp.statesTimeOut);
            chatApp.statesTimeOut = null;
        } else {
            chatApp.statesTimeOut = setTimeout(this.sendPausedStatus, 10000);
        }
    },

    sendPausedStatus: function () {
        if(chatApp.myProfile.get("isTyping") ){
            chatApp.myProfile.set("isTyping", false)
            chatApp.connection.chatstates.sendPaused(chatApp.contactList.getCurrentUser().get("jid"), "chat");
        }
        if (chatApp.statesTimeOut) {
            clearTimeout(chatApp.statesTimeOut);
            chatApp.statesTimeOut = null;
        }
    },

    getMoreHistory: function(){
        var currentUser = chatApp.contactList.getCurrentUser()
        var firstMsgInView = currentUser.messages.first()
        currentUser.retrieveMessages(currentUser.messages.first().get("timestamp").getTime(),function(){
//            currentUser.messages.at(currentUser.messages.indexOf(firstMsgInView)-1).set("shouldScrollIntoView",true)
            currentUser.messages.at(currentUser.messages.indexOf(firstMsgInView)-1).set("shouldScrollIntoView",true)
        })
        return false;
    },

    _scrollChatToBottom: function(){
        var div = this.$(".message-list")[0];
        div.scrollTop = div.scrollHeight;
    }

})

var ChatBoxListView = Backbone.View.extend({

    el: "#chat-right-column",

    initialize: function () {
        this.listenTo(this.model, "add", function (chat) {
            this.$el.append(new ChatBoxView({model: chat}).render().el);
        }, this);
        this.render()
    },

    render: function () {
        _.each(this.model.models, function (contact) {
            this.$el.append(new ChatBoxView({model: contact}).render().el);
        }, this);
        return this;
    }
})

var chatApp = {

    isVisible: function(){
        return $("#chat-dialog").is(":visible");
    },
    connection: null,

    totalUnReadCount:0,

    myProfile: new Contact({
        id: $commonData.data("uid"),
        avatarUrl: $chatData.data("my-avatar"),
        profileUrl: $chatData.data("profile-url"),
        name: $chatData.data("my-name")
    }),
    hasAvatar: function(){
        return this.myProfile.get("avatarUrl") != $chatData.data("defaultAvatar")
    },

    isWindowFocused: false,

    orignalWindowTitle: $("title").text(),

    unReadMsgInterval: null,

    initialize: function () {
    },

    checkConnection: function(){
        if (!this.connection){
            alert("连接已断开，点击确认后自动刷新页面")
            setTimeout(function(){
                location.reload()
            }, 1000)
            return false
        } else {
            return true
        }
    },

    listContacts: function (roster) {
        var contacts = _.map(roster, function (contact, jid) {
            return new Contact({"id":Strophe.getNodeFromJid(jid) , "jid": jid});
        })
        this.contactList = new ContactCollection(contacts);
        this.contactListView = new ContactListView({model: this.contactList})
        this.chatBoxListView = new ChatBoxListView({model: this.contactList})
        if(contacts.length == 0){
//            $("#chat-left-column, #chat-right-column").hide()
//            $("#no-roster-tip").show()
            return ;
        }
        contacts.length && this.contactList.fetch({
            type: 'post',
            data: {
                ids : _.pluck(contacts, "id").join(",")
            }
        })
        $(window).resize()
        this.contactList.each(function(contact){
            contact.retrieveUnReadMessages();
        })
    },
    createContact: function(bareJID){
        var contact = new Contact({"id": Strophe.getNodeFromJid(bareJID), "jid":bareJID});
        contact.fetch({
            type: 'post',
            data: {
                id: contact.id
            }
        })
        chatApp.contactList.add(contact);
        return contact;
    },
    log: function (msg) {
        if(typeof console != "undefined"){
            console.log(msg);
        }
    },

    debug: function (msg) {
        if(typeof console != "undefined"){
            console.log(msg);
        }
    }
}

$(document).bind('connected', function () {

    chatApp.initialize();
    chatApp.connection.roster.get().done(function (roster) {
        chatApp.listContacts(roster)
        chatApp.connection.send($pres());
    })

    $(".btn-follow").live("click", function(){
        chatApp.connection.roster.subscribe($(this).data("uid")+chatServerDomain);
    })
    $(".btn-chat").click(function(){
        var toUID = $(this).data("uid");
        var toJID = toUID + chatServerDomain;
        //show chat dialog
        $("#chat-dialog").modal({
            show: true
        })
        if (!chatApp.contactList.get( toUID)) {
            chatApp.createContact(toJID).retrieveMessages();
            chatApp.connection.roster.subscribe(toJID);
        }
        chatApp.contactListView.$el.find("#contact-" + toUID).click();
        //add to roster

        return false;
    })

    chatApp.connection.roster.on("xmpp:presence:available",function (data) {

        var contact = chatApp.contactList.get(Strophe.getNodeFromJid(data.jid));
        contact && contact.set('show', "online")

    }).on("xmpp:presence:unavailable",function (data) {

            var contact = chatApp.contactList.get(Strophe.getNodeFromJid(data.jid));
            contact && contact.set('show', "offline")

        }).on("xmpp:presence:subscriptionrequest", function (data) {

            chatApp.connection.roster.authorize(data.jid);
            chatApp.connection.roster.subscribe(data.jid);

        }).on("xmpp:roster:set", function(items){
            //add new contacts
            _.each(items, function (item) {
                if (item.subscription != 'remove' && !chatApp.contactList.get(Strophe.getNodeFromJid(item.jid))) {
                    chatApp.createContact(item.jid).retrieveMessages();
                }
            });

        })
    chatApp.connection.message.on("xmpp:message", function (data) {

        // data = {jid: "", type:"" , body:"" , html_body: ""}
        var fromUID = Strophe.getNodeFromJid(data.jid);
        if (fromUID != chatApp.myProfile.id) { //come from others
            var msg = new Message({
                from: fromUID, //who I am chatting with
                to: chatApp.myProfile.id,
                body: data.body,
                timestamp: new ServerDate()
            })
            msg.sender.addMessage(msg)
        }
    });

    $(document).bind("composing.chatstates", function(ev, jid){

        var contact = chatApp.contactList.get(Strophe.getNodeFromJid(jid));
        contact && contact.set("isTyping", true)

    }).bind("paused.chatstates", function(ev, jid){

            var contact = chatApp.contactList.get(Strophe.getNodeFromJid(jid));
            contact && contact.set("isTyping", false)

    })
});

$(window).bind("beforeunload", function(){
    if (chatApp.connection) {
        chatApp.connection.sync = true; // Switch to using synchronous requests since this is typically called onUnload.
        chatApp.connection.flush();
        chatApp.connection.disconnect();
        chatApp.connection = null;
    }
});
$(window).focus(function(){
    chatApp.isWindowFocused = true;
    try {

        if (chatApp.isVisible() && chatApp.contactList.getCurrentUser() && chatApp.contactList.getCurrentUser().get("unReadCount") > 0) {
            chatApp.contactListView.$el.find(".current").click();
        }
    } catch (e) {
    }
}).blur(function(){
    chatApp.isWindowFocused = false;
})

$(window).resize(function(){
    if($("#chat-container")){
        var windowHeight = $(window).height();
        if(windowHeight > 700 ){
            $("#chat-dialog").height(630)
            $("#chat-container").height(590)
            $(".message-list").height( 470)
        } else if(windowHeight < 250 ){
            $("#chat-dialog").height(180)
            $("#chat-container").height(140)
            $(".message-list").height( 20)
        } else {
            $("#chat-dialog").height(windowHeight - 70)
            $("#chat-container").height(windowHeight - 110)
            $(".message-list").height( windowHeight - 230)
        }
    }
})
