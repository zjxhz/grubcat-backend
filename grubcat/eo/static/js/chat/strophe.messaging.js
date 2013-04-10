//    XMPP plugins for Strophe v0.2

//    (c) 2012 Yiorgis Gozadinos.
//    strophe.plugins is distributed under the MIT license.
//    http://github.com/ggozad/strophe.plugins

    Strophe.addConnectionPlugin('message', {

        _connection: null,

        init: function (conn) {
            this._connection = conn;
            Strophe.addNamespace('XHTML_IM', 'http://jabber.org/protocol/xhtml-im');
            Strophe.addNamespace('XHTML', 'http://www.w3.org/1999/xhtml');
            _.extend(this, Backbone.Events);
        },

        // Register message notifications when connected
        statusChanged: function (status, condition) {
            if (status === Strophe.Status.CONNECTED || status === Strophe.Status.ATTACHED) {
                this._connection.addHandler(this._onReceiveChatMessage.bind(this), null, 'message', 'chat');
            }
        },

        // Upon message receipt trigger an `xmpp:message` event.
        _onReceiveChatMessage: function (message) {
            var body, html_body;
            if($(message).find("delay")[0]){
                return true; //currently doesn't act for offline messages, because they are handled for the unread messages
            }
            body = $(message).children('body').text();
            if (body === '') {
                return true; // Typing notifications are not handled.
            }
            html_body = $('html[xmlns="' + Strophe.NS.XHTML_IM + '"] > body', message);
            if (html_body.length > 0) {
                html_body = $('<div>').append(html_body.contents()).html();
            } else {
                html_body = null;
            }
            this.trigger('xmpp:message', {jid: message.getAttribute('from'),
                                                        type: message.getAttribute('type'),
                                                        body: body,
                                                        html_body: html_body});
            return true;
        },

        // **send** sends a message. `body` is the plaintext contents whereas `html_body` is the html version.
        send: function (to, body, html_body) {
            var msg = $msg({to: to, type: 'chat'});

            if (body) {
                msg.c('body', {}, body);
            }

            if (html_body) {
                msg.c('html', {xmlns: Strophe.NS.XHTML_IM})
                    .c('body', {xmlns: Strophe.NS.XHTML})
                    .h(html_body);
            }

            this._connection.send(msg.tree());
        }
    });
