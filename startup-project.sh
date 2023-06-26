if [[ ! -v APP ]]; then
    echo Неопределена переменная APP
    exit 1
fi

echo `whoami` `id` `date`

if [ ! -f $APP/reload ]; then
    poetry install
    poetry run django-admin startproject $APP
    touch $APP/reload
fi


poetry run gunicorn --config gunicorn.conf.py --reload-extra-file $APP_HOME/$APP/reload --chdir $APP  $APP.wsgi:application --log-level=DEBUG
