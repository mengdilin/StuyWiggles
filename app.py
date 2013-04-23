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
        if request.form['button']=='Register':
            return redirect(url_for("register"))


@app.route('/register',methods=['GET','POST'])
def register():
    if session.has_key('user'):
        session.pop('user')
    if request.method=="GET":
        return render_template("register.html", loggedout=True)
    elif request.method=='POST':
        if request.form['button']=='Register':
            username=request.form['username']
            password=request.form['password']
            osis=request.form['osis']
            digit=request.form['digit']
            classes=request.form.getlist('class') 
            teachers=request.form.getlist('teacher')
            name=request.form['name']
            exist=database.add_student(username,password)
            if exist:
                return render_template("register.html",loggedout=True,exists=exist)
            database.set_osis(username,osis)
            database.set_id(username,digit)
            database.set_name(username,name)
            database.set_schedule(username,classes,teachers)
            return redirect(url_for("profile"))
    return redirect(url_for("register"))

@app.route("/tradingfloor",methods=['GET','POST'])
def tradingfloor():
    if not session.has_key('user'):
        return redirect(url_for("about"))
    username=session['user']
    name=database.get_name(username)
    osis=database.get_osis(username)
    digits=database.get_id(username)
    floor=database.get_floor()
    if request.method=='GET':
        return render_template("trading.html"
                               ,name=name
                               ,osis=osis
                               ,digits=digits
                               ,floor=floor
                               ,validate=False)
    if request.method=='POST':
        if request.form['button']=='posts':
            clas=request.form['clas']
            period=request.form['period']
            teacher=request.form['teacher']
            error=False
            tmp=0
            try:
                tmp=int(period)
            except Exception:
                error=True
            if period=="" or teacher=="" or clas=="" or tmp<1 or tmp>10:
                error=True
                return render_template("trading.html"
                                       ,name=name
                                       ,osis=osis
                                       ,digits=digits
                                       ,floor=floor
                                       ,validate=error)
            else:
                req=[str(period),str(clas),str(teacher)]
                database.post_request(username,req)
                return redirect(url_for("tradingfloor"))
        else:
            index=int(request.form['button'])-1
            req=floor[index]["request"]
            postername=floor[index]["username"]
            acceptername=username
            database.accept_request(postername,acceptername,req)
            return redirect(url_for("tradingfloor"))


@app.route('/profile',methods=['GET','POST'])
def profile():
    if not session.has_key('user'):
        return redirect(url_for('about'))
    username=session['user']
    name=database.get_name(username)
    osis=database.get_osis(username)
    digits=database.get_id(username)
    schedule=database.get_schedule(username)
    notif=database.get_notification(username)
    if request.method=='GET':        
        return render_template("profile.html"
                               ,name=name
                               ,osis=osis
                               ,digits=digits
                               ,schedule=schedule
                              # ,post=notif["post"]
                               ,accept=notif["accept"]
                               ,accepted=notif["accepted"]
                               )
if __name__=="__main__":
    app.debug=True
    app.run(port=7007)
