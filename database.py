from pymongo import Connection

Connection=Connection('mongo2.stuycs.org')
db=Connection.admin
res=db.authenticate('ml7','ml7')
db=Connection["StuyWiggles"]
students=db.students
floor=db.floor
class_info=db.classinfo

def dbupdate(username,user):
    db=Connection["StuyWiggles"]
    students.update({"username":username},user)

#accept: when user accepts other people's requests
#accepted: when other people accept user's requests
def add_student(username,password):
    db=Connection["StuyWiggles"]
    if (username not in get_usernames()) and validate_password(password):
        s=["","free","n/a","","",""]
        student={"username":str(username),"password":str(password),"schedule":[s,s,s,s,s,s,s,s,s,s], "osis":0,"id":0,"posted request":[],"notification":{"post":[],"accept":{},"accepted":{}},"name":"","email":""}
        students.insert(student)
        return False
    else:
        return True

def set_email(username,email):
    db=Connection["StuyWiggles"]
    user=find_student(username)
    user["email"]=str(email)
    dbupdate(username,user)

def set_password(username,password):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    student["password"]=password
    students.update({"username":username},student)

def set_name(username, name):
    db=Connection["StuyWiggles"]
    user=find_student(username)
    user["name"]=str(name)
    dbupdate(username,user)

def get_email(username):
    db=Connection["StuyWiggles"]
    user=find_student(username)
    return user["email"]

def get_name(username):
    db=Connection["StuyWiggles"]
    user=find_student(username)
    name=user["name"]
    return name

def post_request(username,request):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    current_schedule=get_schedule(username)
    current_schedule=current_schedule[int(request[0])-1]
    row_data={"name":get_name(username),"username":username,"request":request,"current schedule":current_schedule, "period":request[0]}
    floor.insert(row_data)
        
def get_notification(username):
    db=Connection["StuyWiggles"]
    user=find_student(username)
    return user["notification"]


def accept_request(postername,acceptername,request):
    db=Connection["StuyWiggles"]
    poster=find_student(postername)
    accepter=find_student(acceptername)

    if postername not in accepter["notification"]["accept"].keys():
        accepter["notification"]["accept"][postername]=[]
    if acceptername not in poster["notification"]["accepted"].keys():
        poster["notification"]["accepted"][acceptername]=[]
    if len(accepter["notification"]["accept"][postername])>=7:
        accepter["notification"]["accept"][postername].pop(0)
    accepter["notification"]["accept"][postername].append(request)
    
    if len(poster["notification"]["accepted"][acceptername])>=7:
        poster["notification"]["accepted"][acceptername].pop(0)
    poster["notification"]["accepted"][acceptername].append(request)
    accept_class=accepter["schedule"][int(request[0])-1]
    post_class=poster["schedule"][int(request[0])-1]
    accepter["schedule"][int(request[0])-1]=post_class
    #print [accepter["schedule"][int(request[0])],post_class]
    poster["schedule"][int(request[0])-1]=accept_class
    floor.remove({"username":postername,"request":request})
    dbupdate(postername,poster)
    dbupdate(acceptername,accepter)

def remove_item(l,x):
    l=[item for item in l if (str(item[0])!=str(x[0]) or str(item[1])!=str(x[1]) or str(item[2])!=str(x[2]))]
    return l

def get_request(username):
    db=Connection["StuyWiggles"]
    user=find_student(username)
    return user["posted request"]

#THIS IS FOR APP.PY!!
#check if username matches with password
def validate(username,password):
    if username not in get_usernames():
        return False
    user=find_student(username)
    if user["password"]!=password:
        return False
    return True

#check if username is already taken
#if user already taken, returns False
def validate_user(username):
    if str(username) in get_usernames():
        return False
    return True

#check if password has more than 6 characters
#if no, returns False
def validate_password(password):
    password=str(password)
    if len(password)<6:
        return False
    return True

#check if the two passwords match 
def match_password(p1,p2):
    if str(p1)!=str(p2):
        return False
    return True


def get_usernames():
    db=Connection["StuyWiggles"]
    names=[]
    for line in students.find():
        names.append(str(line["username"]))
    return names

def set_password(username,password):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    student["password"]=password
    students.update({"username":username},student)

def floorupdate(row_data):
    floor.insert(row_data)

def set_schedule(username,clas,teacher):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    l=[]
    l=[[clas[i],teacher[i]] for i in range(len(clas))]
    student["schedule"]=l
    dbupdate(username,student)

def get_floor():
    l=[item for item in floor.find()]
    return l

def get_schedule(username):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    return student["schedule"]

def set_osis(username,osis):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    student["osis"]=osis
    dbupdate(username,student)

def get_osis(username):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    return student["osis"]

def set_id(username,digits):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    student["id"]=digits
    dbupdate(username,student)
    
def get_id(username):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    return student["id"]

def get_period(username,period_number):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    schedule=student["schedule"]
    return schedule[period_number-1]
    
#parameter period: an int 
def set_period(username,period,clas):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    schedule=student["schedule"]
    schedule[int(period)-1]=clas
    students.update({"username":str(username)},student)

def find_student(username):
    return students.find_one({"username":str(username)})

#This is for dropping classes
def drop_period(username,period):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    schedule=student["schedule"]
    schedule[int(period)-1]=[str(period),"free","n/a","","",""]
    students.update({"username":str(username)},student)

def has_lunch(username,period):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    schedule=student["schedule"]
    if schedule[int(period)-1][1]=="Cafe":
        return True
    else:
        return False

def get_lunch(username):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    schedule=student["schedule"]
    l=""
    for i in schedule:
        if i[1]=="Cafe":
            l=i[0]
    return l

'''
=================================================================
Methods for the class info page database
'''

def prep_class_file():
    f=open("classes.txt","r")
    classes=f.readlines()
    classes=[x.strip() for x in classes]
    classes=[x.split(",") for x in classes]
    classes=[[x[2],x[5],x[4],x[0],x[1],x[6]] for x in classes]
    return classes

def get_class_info():
    l=class_info.find_one()["classes"]
    return l

def save_classes():
    clas=prep_class_file()
    info=class_info.find_one()
    for item in clas:
        info["classes"].append(item)
    classupdate(info)

def classupdate(info):
    db=Connection["StuyWiggles"]
    class_info.update({"name":"name"},info)


def remove_request(username, request):
    floor.remove({"username":username,"request":request})

def l_equal(a,b):
    for index in range(len(a)):
        if (a[index]!=b[index]):
            return False
    return True

def refresh_floor():
    for item in floor.find():
        username=str(item['username'])
        request=(item["request"])
        period=int(item["request"][0])
        schedule=get_schedule(username)[period-1]
        item["current schedule"]=schedule
        floor.update({"username":username,"request":request},item)

