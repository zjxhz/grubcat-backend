var chatServer = "http://www.fanjoin.com:7070/http-bind/"
var chatServerDomain ="@fanjoin.com"
//var chatServer = "http://localhost:8001/http-bind/"
//var chatServerDomain ="@dds-pc"
var myTemplate = {
    tplContactListItem: '<div class="avatar"><img src="<%= avatarUrl%>" alt="<%= name %>" title="<%= name %>"/></div>' +
        '<div class="nickname"><%= name %></div>' +
        '<div class="unread-count"><%=unReadCount%></div>',
    tplChatBox: '<div class="chat-title"><%= withName %></div>' +
        '            <div class="chat-message-container">' +
        '                <div class="chat-item-list"></div>' +
        '           <div class="chat-status">对方正在输入...</div>' +
        '       </div>' +
        '   <div class="chat-editor">' +
        '           <textarea type="text" class="chat-input"></textarea>' +
        '       <button class="btn btn-primary btn-send">发送</button>' +
        '       </div>',
    tplMessageListItem: '<div class="message-item <%=from%>" data-timestamp="<%=timestamp%>">' +
        '<a href="<%=profileUrl%>" target="_blank" ><img class="avatar" src="<%= avatarUrl%>" alt="<%= name %>" title="<%= name %>"></a>' +
        '<div class="message-content"><div class="message-text"><%=body%></div><div class="message-arrow"></div></div>' +
        '</div>'
}
$(function () {
    var $commonData = $("#common-data");
//    $("#chat-container").data("jid", "admin@dds-pc/dds-pc")
    $(document).trigger('connect', {
        //        jid: "weibo_1652340607@fanjoin.com",
        //        password: "2.00xQDpnBG_tW8E1b6d563b480ZUU3a"
        //        jid: "dds_xmpp@fanjoin.com",
        //        password: "ddsjiayou124126"
        jid: $commonData.data("uid")+chatServerDomain,
        password: $commonData.data("pwd")
    });

})

$(document).bind('connect', function (ev, data) {
    var conn = new Strophe.Connection(chatServer);

    conn.xmlInput = function (elem) {
//        if($(elem).find("message")[0]){
//
//        app.debug("in")
//        app.debug($(elem).find("message")[0])
//        }
        chatApp.debug(elem)
    }
    conn.xmlOutput = function (elem) {
        /*if($(elem).find("message")[0]){

        app.debug("out")
            app.debug($(elem).find("message")[0])
        }*/
        chatApp.debug(elem)
    }

    conn.connect(data.jid, data.password, function (status) {
        if (status === Strophe.Status.CONNECTED) {
            $(document).trigger('connected');
        } else if (status === Strophe.Status.DISCONNECTED) {
            $(document).trigger('disconnected');
        }
    });

    chatApp.connection = conn;
});

var $chatData = $("#chat-data");

//contact
var Contact = Backbone.Model.extend({
    defaults: {
        show: "offline",
        name: "user",
        unReadCount: 0,
        current: false, // is current chat user
        avatarUrl: $chatData.data("default-avatar")
        //other attributes
        // profileUrl
    },
    parse: function (contact) {
        this.has("jid") && (contact["jid"] = this.get("jid"))
        this.has("show") && (contact["show"] =this.get("show"))
        return contact;
    },

    retrieveMessages: function(before){
        if(!before){
            before = "";
        }
        var user = this;
        var max = 5;
        chatApp.connection.archive.retrieveMessages(this.get("jid"), new Strophe.RSM({max:max, before:before}), function(messages){
            var isRetrieveAgain = messages.length == max;
            for (var i in messages) {
                var oldMsg = messages[i];
                var msg = {
                    from: Strophe.getNodeFromJid(oldMsg.from),
                    to: Strophe.getNodeFromJid(oldMsg.to),
                    body: oldMsg.body,
                    timestamp: oldMsg.timestamp,
                    isRead: oldMsg.isRead
                }
                if(msg.isRead || msg.from == chatApp.myProfile.id){
                    isRetrieveAgain = false;
                    break; // currently just show unread msgs, don't show history msgs which are read
                }
                chatApp.getChat(user.id).addMessage(msg);
            }
            if ( isRetrieveAgain) {
                before = messages[messages.length - 1].timestamp.valueOf();
                user.retrieveMessages( before);
            }
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
                    $totalUnReadCount.toggleClass("hide")
                } else {
//                    $("title").text(chatApp.orignalWindowTitle);
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
    model: Contact,

    parse: function (contacts) {
        var collection = this;
        _.each(contacts, function (contact) {
            contact["jid"] = collection.get(contact["id"]).get("jid")
            contact["show"] = collection.get(contact["id"]).get("show")
        })
        return contacts;
    }
});

var ContactListItemView = Backbone.View.extend({
    tagName: "div",

    className: "contact-item",

    id: function(){
      return "contact-" + this.model.id;
    },

    template: _.template(myTemplate.tplContactListItem),

    initialize: function () {
        this.listenTo(this.model, "change", this.render);
        this.listenTo(this.model, "destory", this.close);
    },

    render: function () {
        this.$el.html(this.template(this.model.attributes)).removeClass("offline online").addClass(this.model.get("show"));
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
        var currentUID = $(event.currentTarget).attr("id").replace("contact-","");
        var beforeOpenChat = chatApp.currentChat;
        var chatToOpen = chatApp.getChat(currentUID);
        if (chatToOpen) {
            beforeOpenChat && beforeOpenChat.set("isVisible", false);
            chatToOpen.set("isVisible", true);
            chatApp.currentChat = chatToOpen;

            beforeOpenChat && chatApp.contactList.get(beforeOpenChat.id).set("current", false);
            chatApp.contactList.get(currentUID).set("current", true);

        }
        //send received
        chatApp.contactList.get(currentUID).clearUnReadCount();
        return false;
    },

    close: function () {
        this.$el.unbind();
        this.$el.remove();
    }
});
var ContactListView = Backbone.View.extend({

    el: "#roster",

    initialize: function () {
        this.listenTo(this.model, "reset", this.render, this);
        this.listenTo(this.model, "add", function (contact) {
            this.$el.append(new ContactListItemView({model: contact}).render().el);
        });
    },

    render: function () {
        _.each(this.model.models, function (contact) {
            this.$el.append(new ContactListItemView({model: contact}).render().el);
        }, this);
        return this;
    }

});

/**
 *  msg={from:"", to:"",body:"", timestamp:L}
 *  from to are all user id
 **/

var Chat = Backbone.Model.extend({
    defaults: {
        isVisible: false,
        isOtherTyping: false,
        lastInMessage: null,
        lastOutMessage: null
    },
    getChatJID : function(){
        return chatApp.contactList.get(this.get("id")).get("jid");
    },
    addMessage: function(msg){
        if( msg.from === chatApp.myProfile.id  ) //msg out
        {
            this.set("lastOutMessage", msg);
        } else
        {
            var uid = msg.from;
            if (!msg.isRead){
                if(chatApp.isWindowFocused && uid == chatApp.currentChat.id){
                    chatApp.contactList.get(uid).sendReceivedRecipts();
                } else {
                    chatApp.contactList.get(uid).increaseUnReadCount(1);
                }
            }
            this.set("lastInMessage", msg);
        }

    }

})

var ChatCollection = Backbone.Collection.extend({
    model: Chat
})

var ChatBoxView = Backbone.View.extend({
    tagName: "div",
    className: "chat-box",
    template: _.template(myTemplate.tplChatBox),

    initialize: function () {
        var contact = chatApp.contactList.get(this.model.id);
        this.$el.html(this.template({
            withName: contact.get("name")
        }));
//        this.$el.find(".chat-item-list").lionbars()
        this.listenTo(this.model, "change", this.render);
        this.listenTo(this.model, "destory", this.close);
    },

    close: function () {
        this.$el.unbind();
        this.$el.remove();
    },

    _renderMessageItemView: function (msg) {

        var fromUser ;

        fromUser = msg.from === chatApp.myProfile.id ? chatApp.myProfile : chatApp.contactList.get(msg.from);
        var data = {
            name: fromUser.get("name"),
            body: msg.body,
            from: msg.from === chatApp.myProfile.id ? "me" : "others" ,
            timestamp: msg.timestamp.getTime(),
            avatarUrl: fromUser.get("avatarUrl"),
            profileUrl: fromUser.get("profileUrl"),
            isRead: msg.isRead
        }
        if(this.$el.find(".message-item:contains('" + msg.body + "')")[0]){
           var i = 3+3;
        }
        var elToInsertBefore = _.find(this.$el.find(".chat-item-list .message-item"), function(elMsg){
            return $(elMsg).data("timestamp") >= data.timestamp;
        });
        if(elToInsertBefore){
            $(elToInsertBefore).before(_.template(myTemplate.tplMessageListItem, data));
        } else {
            this.$el.find(".chat-item-list").append(_.template(myTemplate.tplMessageListItem, data))
        }
    },

    _scrollChatToBottom: function(){
        var div = this.$el.find(".chat-item-list")[0];
        div.scrollTop = div.scrollHeight;
    },

    render: function () {
        if (this.model.hasChanged("isVisible")) {
            var show = this.model.get("isVisible");
            show ? this.$el.show() && this.$el.find(".chat-input").focus(): this.$el.hide();
            this._scrollChatToBottom()
        }
        if (this.model.hasChanged("lastInMessage")) {
            this._renderMessageItemView(this.model.get("lastInMessage"))
            this._scrollChatToBottom()
        }
        if (this.model.hasChanged("lastOutMessage")) {
            this._renderMessageItemView(this.model.get("lastOutMessage"))
            this._scrollChatToBottom()
        }
        if (this.model.hasChanged("isOtherTyping")) {
            this.model.get("isOtherTyping") ? this.$el.find(".chat-status").show() : this.$el.find(".chat-status").hide();
        }
        return this;
    },

    events: {
        "keypress .chat-input": "keyPressed",
        "focusout .chat-input": "sendPausedStatus",
        "click .btn-send": "sendMessage"
    },

    keyPressed: function(ev){

        if (ev.which === 13) {
            ev.preventDefault();
            this.sendMessage();
        } else {
            this.sendTypingStatus();
           // app.getChat(app.currentChatUID)
        }
    },
    sendMessage: function () {
        var $chatInput = this.$el.find(".chat-input");
        var body = $chatInput.val();
        if (!body){
            return false;
        }
        $chatInput.val("");
        chatApp.connection.message.send(chatApp.currentChat.getChatJID(), body)
        chatApp.currentChat.addMessage({
                from: chatApp.myProfile.id,
                to: chatApp.currentChat.id,
                body: body,
                timestamp: new ServerDate()
        })
        return false;
    },

    sendTypingStatus: function(){
        if( !chatApp.isMeTyping ){ // previous not typing
//            app.isMeTyping = true;
            chatApp.connection.chatstates.sendComposing(chatApp.currentChat.getChatJID(), "chat");

            chatApp.isMeTyping = true;
        }
        if (chatApp.statesTimeOut) {
            clearTimeout(chatApp.statesTimeOut);
            chatApp.statesTimeOut = null;
        } else {
            chatApp.statesTimeOut = setTimeout(this.sendPausedStatus, 10000);
        }


    },


    sendPausedStatus: function () {
        if( chatApp.isMeTyping ){
            chatApp.isMeTyping = false;
            chatApp.connection.chatstates.sendPaused(chatApp.currentChat.getChatJID(), "chat");
        }
        if (chatApp.statesTimeOut) {
            clearTimeout(chatApp.statesTimeOut);
            chatApp.statesTimeOut = null;
        }
    }

})

var ChatBoxListView = Backbone.View.extend({
    el: "#chat-right-column",
    initialize: function () {
        this.listenTo(this.model, "add", function (chat) {
            this.$el.append(new ChatBoxView({model: chat}).render().el);
        }, this);
    }
})

var chatApp = {

    isVisible: function(){
        return $("#chat-dialog").is(":visible");
    },

    connection: null,

    totalUnReadCount:0,

    myProfile: new Contact({
        id: $("#common-data").data("uid"),
//        jid: "",
        avatarUrl: $chatData.data("my-avatar"),
        profileUrl: $chatData.data("profile-url"),
        name: $chatData.data("my-name")
    }),
    isMeTyping: false,

    currentChat: null,

    isWindowFocused: false,

    orignalWindowTitle: $("title").text(),

    unReadMsgInterval: null,

    initialize: function () {
        this.chatList = new ChatCollection();
        this.chatListView = new ChatBoxListView({model: this.chatList})
    },

    getChat: function (uid) {
        var chat = chatApp.chatList.get(uid);
        if (!chat) {
            var chatData = {
                id: uid
            }
            chat = new Chat(chatData)
            chatApp.chatList.add(chat)
        }
        return chat;
    },

    listContacts: function (roster) {
        var contacts = _.map(roster, function (contact, jid) {
            return new Contact({"id":Strophe.getNodeFromJid(jid) , "jid": jid});
        })
        this.contactList = new ContactCollection(contacts);
        this.contactListView = new ContactListView({model: this.contactList})
        contacts.length && this.contactList.fetch({
            url: $chatData.data("get-user-info-url"),
            type: 'post',
            data: {
                ids : _.pluck(contacts, "id").join(",")
            }
        })
        this.contactList.each(function(contact){
            contact.retrieveMessages();
        })
    },
    createContact: function(bareJID){
        var contact = new Contact({"id": Strophe.getNodeFromJid(bareJID), "jid":bareJID});
        contact.fetch({
            url: $chatData.data("get-user-info-url"),
            type: 'post',
            data: {
                id: contact.id
            }
        })
        chatApp.contactList.add(contact);
        return contact;
    },
    log: function (msg) {
        console && console.log(msg);
    },

    debug: function (msg) {
        console && console.log(msg);
    }
}

$(document).bind('connected', function () {

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
        }
        chatApp.contactListView.$el.find("#contact-" + toUID).click();
        //add to roster
        chatApp.connection.roster.subscribe(toJID);
        return false;
    })

    chatApp.initialize();
    chatApp.connection.roster.get().done(function (roster) {
        chatApp.listContacts(roster)
        chatApp.connection.send($pres());
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
        //TODO full jid?
        if (fromUID != chatApp.myProfile.id) { //come from others
            var msg = {
                from: fromUID, //who I am chatting with
                to: chatApp.myProfile.id,
                body: data.body,
                timestamp: new ServerDate()
            }
            var chat = chatApp.getChat(fromUID);
            chat.addMessage( msg);
        }
    });

    $(document).bind("composing.chatstates", function(ev, jid){
        var uid = Strophe.getNodeFromJid(jid);
        chatApp.getChat(uid).set("isOtherTyping", true)
    }).bind("paused.chatstates", function(ev, jid){
            var uid = Strophe.getNodeFromJid(jid);
            chatApp.getChat(uid).set("isOtherTyping", false)
    })
});

$(window).bind("beforeunload", function(){
    chatApp.connection.disconnect();
    chatApp.connection = null;
});
$(window).focus(function(){
    chatApp.isWindowFocused = true;
    if (chatApp.currentChat && chatApp.isVisible() && chatApp.contactList.get(chatApp.currentChat.id).get("unReadCount") > 0) {
        chatApp.contactListView.$el.find(".current").click();
    }
}).blur(function(){
    chatApp.isWindowFocused = false;
})

$(document).bind('disconnected', function () {
    chatApp.log("dis-connected");
});



