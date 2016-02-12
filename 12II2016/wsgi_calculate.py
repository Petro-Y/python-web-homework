#from cgi import parse_qs, escape
from urllib.parse import parse_qs
#from html import escape
import re

def check_parentheses(expr):
    expr=re.sub(r'[^()]', '', expr)
    lvl=0
    for c in expr:
        if c=='(':
            lvl+=1
        elif c==')':
            lvl-=1
        if lvl<0:
            return False
    return lvl==0

def app(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    expr=parameters['expr'][0] if 'expr' in parameters else ''
    # verify expr using regex:
    if not re.fullmatch(r'\(*-?[0-9]+([-+*/]\(*-?[0-9]+\)*)*\)*',expr) or not check_parentheses(expr):
        expr=''
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