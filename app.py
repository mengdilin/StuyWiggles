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

@app.route("/edit",methods=['GET','POST'])
def edit():
    if not session.has_key('user'):
        return redirect(url_for("about"))
    username=session['user']
    name=database.get_name(username)
    #email=database.get_email(username)
    osis=database.get_osis(username)
    digit=database.get_id(username)
    if request.method=='GET':
        return render_template("edit.html"
                               ,username=username
                               ,name=name
                               #,email=email
                               ,osis=osis
                               ,digit=digit
                               ,loggedout=False)
    if request.method=='POST':
        if request.form['button']=='Edit':
            password=request.form['password']
            name=request.form['name']
            #email=request.form['email']
            digit=request.form['digit']
            osis=request.form['osis']
            classes=request.form.getlist('class')
            teachers=request.form.getlist('teacher')
            database.set_password(username,password)
            database.set_name(username,name)
            #database.set_email(username,email)
            database.set_id(username,digit)
            database.set_osis(username,osis)
            database.set_schedule(username,classes,teachers)
            return redirect(url_for('profile'))
        return redirect(url_for('edit'))

@app.route("/classinfo",methods=['GET','POST'])
def classinfo():
    if not session.has_key('user'):
        return redirect(url_for("about"))
    username=session['user']
    name=database.get_name(username)
    osis=database.get_osis(username)
    digits=database.get_id(username)
    classes=database.get_class_info()
    if request.method=='GET':
        return render_template("class.html"
                               ,name=name
                               ,osis=osis
                               ,digits=digits
                               ,classes=classes)
    if request.method=="POST":
        value=request.form['button']
        value=value.split(" ")
        index=int(value[1])-1
        if (str(value[0])=="set"):
            period=classes[index][0]
            clas=classes[index]
            print clas
            database.set_period(username,period,clas)
        if (str(value[0])=="req"):
            req=classes[index]
            print "req"
            database.post_request(username,req)
        return redirect(url_for("classinfo"))

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
        index=int(request.form['button']-1)
        req=floor[index]["request"]
        acceptername=username
        schedule=get_schedule(username)[index]
        if l_equal(req,schedule):
            database.accept_request(postername,acceptername,req)
            return redirect(url_for("tradingfloor"))
        else:
            return render_template("trading.html"
                                   ,name=name
                                   ,osis=osis
                                   ,digits=digits
                                   ,floor=floor
                                   ,validate=True)


def l_equal(a,b):
    for index in range(len(a)):
        if (a[index]!=b[index]):
            return False
    return True
    
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
