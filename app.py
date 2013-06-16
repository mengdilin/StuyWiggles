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
    if session.has_key('user'):
        return redirect(url_for('profile'))
    elif request.method=="GET":
        return render_template("about.html",loggedout=True)
    elif request.method=="POST":
        if request.form['button']=='Login':
            username=request.form['username']
            password=request.form['password']
            if username not in database.get_usernames():
                return render_template("register.html",loggedout=True)
            if database.validate(username,password):
                session["user"]=username
                return redirect(url_for("profile"))
        if request.form['button']=='Register':
            return redirect(url_for("register"))
        return redirect(url_for("about"))

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
            name=request.form['name']
            email=request.form['email']
            lunch=request.form['lunch']
            exist=database.add_student(username,password)
            if exist:
                return render_template("register.html",loggedout=True,exists=exist)
            database.set_osis(username,osis)
            database.set_id(username,digit)
            database.set_name(username,name)
            database.set_email(username,email)
            database.set_period(username,
                                 int(lunch),
                                 [str(lunch),
                                  "Cafe",
                                  "Chi Kun Wang",
                                  "ZLN5",
                                  "0"+str(lunch)])
                                  
            return redirect(url_for("profile"))
    return redirect(url_for("register"))

@app.route("/edit",methods=['GET','POST'])
def edit():
    if not session.has_key('user'):
        return redirect(url_for("about"))
    username=session['user']
    email=database.get_email(username)
    osis=database.get_osis(username)
    digit=database.get_id(username)
    if request.method=='GET':
        return render_template("edit.html"
                               ,username=username
                               ,email=email
                               ,osis=osis
                               ,digit=digit
                               ,loggedout=False)
    if request.method=='POST':
        if request.form['button']=='Edit':
            password=request.form['password']
            email=request.form['email']
            digit=request.form['digit']
            osis=request.form['osis']
            lunch=request.form['lunch']
            schedule=database.get_schedule(username)
            current_lunch=database.get_lunch(username)
            pos=database.get_period(username,int(lunch))[1]
            if not (pos == ' free' or pos=='Cafe'):
                return render_template("edit.html"
                                       ,username=username
                                       ,email=email
                                       ,osis=osis
                                       ,digit=digit
                                       ,loggedout=False
                                       ,invalid=True)
            database.set_period(username,current_lunch,[""," free","n/a","",""])
            database.set_period(username,lunch,[str(lunch),"Cafe","Chi Kun Wang","ZLN5","0"+str(lunch)])
            database.set_password(username,password)
            database.set_email(username,email)
            database.set_id(username,digit)
            database.set_osis(username,osis)
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
    email=database.get_email(username)
    schedule=database.get_schedule(username)
    classes=database.get_class_info()
    if request.method=='GET':
        return render_template("class.html"
                               ,name=name
                               ,osis=osis
                               ,digits=digits
                               ,email=email
                               ,classes=classes
                               ,schedule=schedule
                               ,get=True)
    if request.method=="POST":
        value=request.form['button']
        value=value.split(" ")
        index=int(value[1])-1
        validate=True
        if (str(value[0])=="set"):
            period=classes[index][0]
            clas=classes[index]
            schedule=database.get_schedule(username)
            if schedule[int(period)-1][1]==" free":
                database.set_period(username,period,clas)
            else:
                validate=False
        if (str(value[0])=="req"):
            req=classes[index]
            period=classes[index][0]
            if database.has_lunch(username,period) or l_equal(schedule[int(period)-1],req):
                validate=False
            else:
                database.post_request(username,req)
        return render_template("class.html"
                               ,name=name
                               ,osis=osis
                               ,digits=digits
                               ,email=email
                               ,classes=classes
                               ,schedule=schedule
                               ,validate=validate)

@app.route("/tradingfloor",methods=['GET','POST'])
def tradingfloor():
    if not session.has_key('user'):
        return redirect(url_for("about"))
    username=session['user']
    name=database.get_name(username)
    osis=database.get_osis(username)
    digits=database.get_id(username)
    email=database.get_email(username)
    database.refresh_floor()
    floor=database.get_floor()
    if request.method=='GET':
        return render_template("trading.html"
                               ,name=name
                               ,osis=osis
                               ,digits=digits
                               ,floor=floor
                               ,email=email
                               ,validate=False)
    if request.method=='POST':
        value=request.form["button"]
        value=value.split(" ")
        index=int(value[1])-1
        req=floor[index]["request"]
        period=int(req[0])-1
        acceptername=username
        postername=floor[index]['username']
        schedule=database.get_schedule(username)[period]
        validate=False
        myself=False
        illegaldel=False
        try:
            if not str(postername)==str(username):
                if value[0]=="accept":
                    if l_equal(req,schedule):
                        database.accept_request(postername,acceptername,req)
                        return redirect(url_for("tradingfloor"))
                    else:
                        validate=True
                elif value[0]=="delete":
                    validate=True
                    myself=False
                    illegaldel=True
            else:
                if value[0]=="accept":
                    validate=True
                    myself=True
                else:
                    database.remove_request(username,req)
                    database.refresh_floor()
                    floor=database.get_floor()
            return render_template("trading.html"
                                   ,name=name
                                   ,osis=osis
                                   ,digits=digits
                                   ,email=email
                                   ,floor=floor
                                   ,validate=validate
                                   ,myself=myself
                                   ,illegaldel=illegaldel)
        except Exception:
            return render_template("trading.html"
                                   ,name=name
                                   ,osis=osis
                                   ,digits=digits
                                   ,email=email
                                   ,floor=floor
                                   ,validate=True)

@app.route('/<username>',methods=['GET','POST'])
def visit(username=""):
    if not session.has_key('user'):
        return redirect(url_for('about'))
    me=session['user']
    if str(username)==str(me):
        return redirect(url_for('profile'))
    name=database.get_name(username)
    osis=database.get_osis(username)
    digits=database.get_id(username)
    email=database.get_email(username)
    schedule=database.get_schedule(username)
    notif=database.get_notification(username)
    if request.method=='GET':        
        return render_template("visit.html"
                               ,name=name
                               ,osis=osis
                               ,digits=digits
                               ,schedule=schedule
                               ,email=email
                               ,accept=notif["accept"]
                               ,accepted=notif["accepted"]
                               )
    
@app.route('/profile',methods=['GET','POST'])
def profile():
    if not session.has_key('user'):
        return redirect(url_for('about'))
    username=session['user']
    name=database.get_name(username)
    osis=database.get_osis(username)
    digits=database.get_id(username)
    email=database.get_email(username)
    schedule=database.get_schedule(username)
    notif=database.get_notification(username)
    if request.method=='GET':        
        return render_template("profile.html"
                               ,name=name
                               ,osis=osis
                               ,digits=digits
                               ,schedule=schedule
                               ,email=email
                               ,accept=notif["accept"]
                               ,accepted=notif["accepted"]
                               )
    elif request.method=="POST":
        value=request.form["button"]
        value=value.split(" ")
        index=int(value[1])-1
        if str(value[0])=="drop":
            schedule=database.get_schedule(username)
            clas=schedule[index]
            if not (clas[1]==" free" or clas[1]=="Cafe"):
                database.drop_period(username,clas[0])
                schedule=database.get_schedule(username)
        return render_template("profile.html"
                               ,name=name
                               ,osis=osis
                               ,digits=digits
                               ,schedule=schedule
                               ,email=email
                               ,accept=notif["accept"]
                               ,accepted=notif["accepted"]
                               )

@app.route('/grad15',methods=['GET','POST'])
def grad15():
    if not session.has_key('user'):
        return redirect(url_for('about'))
    if request.method=='GET':
        return render_template('grad2015.html')

@app.route('/grad07',methods=['GET','POST'])
def grad07():
    if not session.has_key('user'):
        return redirect(url_for('about'))
    if request.method=='GET':
        return render_template('grad07.html')

def l_equal(a,b):
    for index in range(len(a)):
        if (a[index]!=b[index]):
            return False
    return True                                           
                                           
                                           
if __name__=="__main__":
    app.debug=True
    app.run(port=7007)
