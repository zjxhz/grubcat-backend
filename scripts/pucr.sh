echo "pullling and updating codes..."
set PROJECT_ROOT=/home/fanju/src/grubcat-backend
hg --repository $PROJECT_ROOT pull https://peterdds:dds123456@bitbucket.org/zjxhz/grubcat-backend -u
echo "installing requirements"
cd $PROJECT_ROOT
pip install -r requirements.txt

echo "dumping DB..."
cd ~/db_dumps
sh dumpdb.sh

echo "collecting static files..."
cd $PROJECT_ROOT/grubcat/
python manage.py collectstatic --noinput
echo "combine and compress css/js files..."
python manage.py assets build
echo "collecting newly compressed css/js files"
python manage.py collectstatic --noinput

echo "migrating..."
python manage.py migrate eo

echo "restarting server"
sudo /etc/init.d/apache2 restart

