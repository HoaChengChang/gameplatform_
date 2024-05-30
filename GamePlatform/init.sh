while ! nc -z db 3306
do
	echo "Waiting for the MySQL Server"
	sleep 3
done

python manage.py collectstatic --noinput&&
python manage.py makemigrations&&
python manage.py migrate&&
python manage.py init_superuser&&
celery -A GamePlatform worker -l info --beat&&
uwsgi --ini /www/html/GamePlatform/uwsgi.ini&&
tail -f /dev/null
exec "$@"
