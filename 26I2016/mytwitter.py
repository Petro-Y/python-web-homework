from flask import Flask, request, redirect
app = Flask(__name__)

@app.route('/', methods=['POST'])
def mytwitter_post():
    message=request.form['message']
    with open('mytwitter.txt', mode='a') as f:
        f.write(message+'\n')
        return redirect('.')


@app.route('/', methods=['GET'])
def mytwitter():
    res=''
    try:
        with open('mytwitter.txt') as f:
            res+='<br/>'.join(tuple(f)[-1:-10:-1])
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