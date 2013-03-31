from flask import Flask
from flask import session,render_template,url_for,redirect,request

app=Flask(__name__)
app.secret_key="secret key"

@app.route("/")
def index():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop():
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return 

if __name__=="__main__":
    app.debug=True
    app.run(port=7007)
