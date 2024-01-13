from urllib.parse import parse_qs
import json

# gunicorn -c gunicorn.conf.py myapp:app
def app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET':
        data = parse_qs(environ['QUERY_STRING'])
    elif environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        data = environ['wsgi.input'].read(request_body_size)
    response = data if isinstance(data, bytes) else str.encode(json.dumps(data, indent=4))
    start_response("200 OK", [
        ("Content-Type", "application/octet-stream"),
        ("Content-Length", str(len(response)))
    ])
    return iter([response])

# curl -G "localhost:8081/?id=3&abs=name"
# curl -X POST localhost:8081 -H "Content-Type: application/json" -d '{"posts":["value2","value3"]}'