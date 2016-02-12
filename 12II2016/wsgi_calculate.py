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
    err=''
    if expr:
        if not re.fullmatch(r'\(*-?([0-9]+\.)?[0-9]+([-+*/]\(*-?([0-9]+\.)?[0-9]+\)*)*\)*',expr) or not check_parentheses(expr):
            err='<span style="color:red">Помилка: </span>'+expr
            expr=''
        else:
            try:
                expr=expr+' = '+str(eval(expr))
            except ZeroDivisionError:
                err='<span style="color:red"> - Ділення на 0</span>'

    start_response('200 OK', [('Content-Type', 'text/html; charset=UTF-8')])
    return [
        b"""<form> <input name=expr> <input type=submit></form>""",
        expr.encode(),
        err.encode()
    ]

if __name__=='__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, app)
    print ("Serving HTTP on port 8000...")

    # Respond to requests until process is killed
    httpd.serve_forever()