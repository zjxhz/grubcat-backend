host=localhost:8000
url=/api/v1/login/
username=xuaxu
password=1qaz2wsx
curl $host$url --data "username=$username&password=$password" --dump-header cookies
