# Gunicorn configuration file
# Рекомендуется использовать этот файл в фоне (gunicorn -c gunicorn.conf.py config.wsgi:application)
# Настройки ориентированы на небольшое приложение; адаптируйте workers/threads под вашу среду

workers = 3  # замените на (2*CPU)+1 для более высокой нагрузки
threads = 2
bind = "0.0.0.0:8000"
worker_class = "gthread"
timeout = 30
keepalive = 2
loglevel = "info"
accesslog = "-"  # лог в stdout
errorlog = "-"  # лог ошибок в stdout

# Дополнительно можно настроить preload_app = True при использовании shared memory/cache
preload_app = False
