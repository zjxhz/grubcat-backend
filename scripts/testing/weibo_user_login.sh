#1.  create a user for the weibo user that logs in for the first time
# curl localhost:8000/api/v1/weibo_user_login/ --data "weibo_id=54321&access_token=12345" --dump-header weibo_user_cookies

#2. run same command again so we just logs the user in

#3. weibo user logs in as a logged in weibo user
# curl localhost:8000/api/v1/weibo_user_login/ --data "access_token=12345&weibo_id=54321" --cookie weibo_user_cookies

#4. weibo user logs in as a ordinary user
curl localhost:8000/api/v1/weibo_user_login/ --data "access_token=12345&weibo_id=54321" --cookie cookies
