bind = "127.0.0.1:8081"
workers = 2
wsgi_app = "askme_zubkov.wsgi"
accesslog = '-'
errorlog = '-'

# gunicorn -c gunicorn -c wsgi/gunicorn.conf.py
# gunicorn -c gunicorn.conf.py myapp:app