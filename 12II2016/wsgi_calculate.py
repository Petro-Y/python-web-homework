#from cgi import parse_qs, escape
from urllib.parse import parse_qs
#from html import escape
import re

def app(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    expr=parameters['expr'][0] if 'expr' in parameters else ''
    # TODO: verify expr using regex...
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [
        b"""<form> <input name=expr> <input type=submit></form>""",
        (expr+' = '+str(eval(expr)) if expr else '').encode()
    ]

if __name__=='__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, app)
    print ("Serving HTTP on port 8000...")

    # Respond to requests until process is killed
    httpd.serve_forever()