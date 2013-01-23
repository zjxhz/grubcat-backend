host=localhost:8000
url=/api/v1/login/
username=xuaxu
password=qqqqqq
curl $host$url --data "username=$username&password=$password" --dump-header cookies
