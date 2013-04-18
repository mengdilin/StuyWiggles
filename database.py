from pymongo import Connection

Connection=Connection('mongo2.stuycs.org')
db=Connection.admin
res=db.authenticate('ml7','ml7')
db=Connection["StuyWiggles"]
students=db.students

def add_student(username,password):
    db=Connection["StuyWiggles"]
    if (username not in get_usernames()) and validate_password(password):
        #need to test this
        student={"username":str(username),"password":str(password),"schedule":[], "osis":0,"id":0,"posted request":[],"notification":[],"first name":"","last name":""}
        students.insert(student)
        return False
    else:
        return True

def set_firstname(username, first):
    db=Connection["StuyWiggles"]
    user=find_student(username)
    user["first name"]=str(first)
    dbupdate(username,user)

def set_lastname(username, last):
    db=Connection["StuyWiggles"]
    user=find_student(username)
    user["last name"]=str(last)
    dbupdate(username,user)

def get_name(username):
    db=Connection["StuyWiggles"]
    user=find_student(username)
    name=user["first name"]+" "+user["last name"]
    return name

#Incomeplete!!
#request needs to add to trading floor collection
def post_req(username,request):
    db=Connection["StuyWiggles"]
    user=find_student(username)
    user["posted request"].append(request)
    notif="You just requested "+request
    user["notification"].append(notif)
    dbupdate(username,user)

def get_notification(username):
    db=Connection["StuyWiggles"]
    user=find_student(username)
    return user["notification"]
'''
#sender:a username
#receiver: a username
#request:a request message in string
def request(sendername,receivername,request):
    db=Connection["StuyWiggles"]
    sender_user=find_student(sendername)
    sender=sender_user["request"]["sent"]
    if receivername not in sender.keys():
        sender[receivername]=[]
    sender[receivername].append(request)
    receiver_user=find_student(receivername)
    receiver=receiver_user["request"]["received"]
    if sendername not in receiver.keys():
        receiver[sendername]=[]
    receiver[sendername].append(request)
    dbupdate(sendername,sender_user)
    dbupdate(receivername,receiver_user)

#approve requests received by username1
#add request to the approve dict for both users
#remove request from dict for both users
def approve(username1,username2,request):
    db=Connection["StuyWiggles"]
    user1=find_student(username1)
    user2=find_student(username2)
    user1["request"]["approved"].append(request)
    user2["request"]["approved"].append(request)
    user1["request"]["received"][username2]=[data for data in user1["request"]["received"][username2] if str(data)!=str(request)]
    user2["request"]["sent"][username1]=[data for data in user2["request"]["sent"][username1] if str(data)!=str(request)]
    dbupdate(username1,user1)
    dbupdate(username2,user2)

#decline requests received by username1
#add request to the declined dict for both users
def decline(username1,username2,request):
    db=Connection["StuyWiggles"]
    user1=find_student(username1)
    user2=find_student(username2)
    user1["request"]["declined"].append(request)
    user2["request"]["declined"].append(request)
    dbupdate(username1,user1)
    dbupdate(username2,user2)

'''
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
    student={"username":str(username),"password":str(password)}
    students.update({"username":username},student)

def dbupdate(username,user):
    db=Connection["StuyWiggles"]
    students.update({"username":username},user)

#format for parameter schedule:
#A list length of 10 which contains 10 lists: [list 1, list 2, list 3, ..., list 10]
#for each list within the big list: ["class","teacher"]
def set_schedule(username,schedule):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    student["schedule"]=schedule
    students.update({"username":str(username)},student)
    
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
#parameter clas: ["class","teacher"]
def set_period(username,period,clas):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    schedule=student["schedule"]
    schedule[period-1]=clas
    students.update({"username":str(username)},student)

def find_student(username):
    return students.find_one({"username":str(username)})



username1="mengdilin"
password1="abcdefg"
first1="mengdi"
last1="lin"
digits1="8744"
osis1="211451265"
schedule1=[["a","a1"]
          ,["b","b2"]
          ,["c","c3"]
          ,["d","d4"]
          ,["e","e5"]
          ,["f","f6"]
          ,["g","g7"]
          ,["h","h8"]
          ,["i","i9"]
          ,["j","j10"]]

username2="georgiii"
password2="abcdefg"
first2="georgi"
last2="huh"
digits2="1111"
osis2="111111111"
schedule2=[["A","a1"]
          ,["B","b2"]
          ,["C","c3"]
          ,["D","d4"]
          ,["E","e5"]
          ,["F","f6"]
          ,["G","g7"]
          ,["H","h8"]
          ,["I","i9"]
          ,["J","j10"]]
'''
add_student(username1,password1)
set_firstname(username1,first1)
set_lastname(username1,last1)
set_id(username1,digits1)
set_osis(username1,osis1)
set_schedule(username1,schedule1)

request_georgi="I want more and more and more of YOUR classes!!"
#request(username2,username1,request_georgi)


ss=find_student(username2)
ss["request"]["approved"]=[]
ss["request"]["declined"]=[]
dbupdate(username2,ss)
aa=find_student(username1)
aa["request"]["approved"]=[]
aa["request"]["declined"]=[]
dbupdate(username1,aa)
approve(username1,username2,request_georgi)


print find_student(username2)
'''


