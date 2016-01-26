from flask import Flask, request, redirect
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def mytwitter():
    if request.method=='POST':
        message=request.form['message']
        with open('mytwitter.txt', mode='a') as f:
            f.write(message+'\n')
            return redirect('/')
    res=''
    try:
        with open('mytwitter.txt') as f:
            res+='<br/>'.join(f)
    except Exception:
        pass
    res+='''
    <form method=POST>
        <input name=message>
        <input type=submit>
    </form>
    '''
    return res


if __name__ == '__main__':
    app.run()