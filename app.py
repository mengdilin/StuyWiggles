from flask import Flask
from flask import session,render_template,url_for,redirect,request

app=Flask(__name__)
app.secret_key="secret key"

@app.route("/")
def index():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    return redirect(url_for('about'))

@app.route('/logout')
def logout():
    session.pop():
    return redirect(url_for('index'))

@app.route('/login')
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        if request.form['button']=='Login':
            username=request.form['username']
            password=request.form['password']
            session['user']=username
            if not username in database.get_usernames():
                return redirect(url_for('register')
            return render_template("login.html",username,password)
            

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/register')
def register():
    if session.has_key('user'):
        return redirect(url_for('logout'))
    elif request.method=='GET':
        return render_template('register.html')
    elif request.method=='POST':
        if request.form['button']=='Register':
            username=request.form['username']
            password=request.form['password']
            invalid = (username==password)
            osis=request.form['osis']
            digit=request.form['digit']
            exist=database.add_student(username,password,osis,digit)
            return render_template("register.html",username,password,invalid,osis,digit,exist)
    return redirect(url_for(register))

@app.route('/profile')
def profile():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    elif request.method=='GET':
        user=session['user']
        schedule=database.get_schedule(user)
        digit=database.get_id(user)
        osis=database.get_osis(user)
        return render_template("profile.html",user,schedule,digit,osis)
    elif request.method=='POST':
        if request.form['button']=='Set':
            return redirect(url_for("setschedule"))
    return redirect(url_for(profile))

if __name__=="__main__":
    app.debug=True
    app.run(port=7007)
