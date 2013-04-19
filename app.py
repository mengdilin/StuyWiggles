from flask import Flask
from flask import session,render_template,url_for,redirect,request
import database

app=Flask(__name__)
app.secret_key="secret key"

@app.route("/")
def index():
    if not session.has_key('user'):
        return redirect(url_for('about'))
    return redirect(url_for('about'))

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('about'))

#works 
#logout does not work
@app.route('/about',methods=['GET','POST'])
def about():
    if request.method=='GET':
        return render_template('about.html',loggedout=True)
    elif request.method=="POST":
        if request.form['button']=='Login':
            username=request.form['username']
            password=request.form['password']
            if username not in database.get_usernames():
                return render_template("about.html",loggedout=True,registered=False)
            if database.validate(username,password):
                session["user"]=username
                return redirect(url_for("profile"))


@app.route('/register',methods=['GET','POST'])
def register():
    if session.has_key('user'):
        return redirect(url_for('logout'))
    elif request.method=='GET':
        return render_template("about.html",loggedout=True,registered=False)
    elif request.method=='POST':
        if request.form['button']=='Register':
            username=request.form['username']
            password=request.form['password']
            osis=request.form['osis']
            digit=request.form['digit']
            #classes=request.form.getlist['class'] 
            #teachers=request.form.getlist['teachers']
            name=request.form['name']
            exist=database.add_student(username,password)
            if exist:
                return render_template("register.html",exist=exist)
            database.set_osis(username,osis)
            database.set_id(username,digit)
            database.set_name(username,name)
            return redirect(url_for(profile))
    return redirect(url_for(register))

#works
@app.route('/profile',methods=['GET','POST'])
def profile():

    if not session.has_key('user'):
        return redirect(url_for('about'))

    if request.method=='GET':
        username=session['user']
        name=database.get_name(username)
        osis=database.get_osis(username)
        digits=database.get_id(username)
        schedule=database.get_schedule(username)
        notif=database.get_notification(username)
            
        return render_template("profile.html"
                               ,name=name
                               ,osis=osis
                               ,digits=digits
                               ,schedule=schedule
                               ,post=notif["post"]
                               ,accept=notif["accept"]
                               ,accepted=notif["accepted"])
    elif request.method=='POST':
        if request.form['button']=='Set':
            return redirect(url_for("setschedule"))
    return redirect(url_for(profile))

if __name__=="__main__":
    app.debug=True
    app.run(port=7007)
