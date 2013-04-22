-module(django_offline).
-author("Henrik P. Hessel").
-behaviour(gen_mod).
-export([start/2, stop/1, django_message/3, send_to_django/3]).

-include("ejabberd.hrl").
-include("jlib.hrl").

start(Host, _Opt) -> 
		?INFO_MSG("DJANGO OFFLINE MODULE LOADING", []),    
		ejabberd_hooks:add(offline_message_hook, Host, ?MODULE, django_message, 50).

stop (Host) -> 
		?INFO_MSG("STOPPING DJANGO OFFLINE MODULE", []),    
		ejabberd_hooks:delete(offline_message_hook, Host, ?MODULE, django_message, 50).

django_message(From, To, Packet) ->
		Type = xml:get_tag_attr_s("type", Packet),
		FromS = xml:get_tag_attr_s("from", Packet),
		ToS = xml:get_tag_attr_s("to", Packet),
		Body = xml:get_path_s(Packet, [{elem, "body"}, cdata]),
		if (Type == "chat") ->
             ?INFO_MSG("an offline message: ~s,~s->~s: ~s~n",[Froms,From,ToS,Body]),
			 send_to_django(FromS, ToS, Body)
		end.

send_to_django(From, To, Body) ->
		Port = open_port({spawn, "python -u /src/grubcat-backend/grubcat/manage.py ejabberd_apple_push"},
		[{packet, 4}, binary, use_stdio]),
		ReqData = term_to_binary({message, From, To, Body}),
		port_command(Port, ReqData).

