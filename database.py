from pymongo import Connection

Connection=Connection('mongo2.stuycs.org')
db=Connection.admin
res=db.authenticate('ml7','ml7')
db=Connection["StuyWiggles"]
students=db.students

#default setting: 
#username: Osis
#password: 4 digit ID
def add_student(username,password):
    db=Connection["StuyWiggles"]
    if not username in get_usernames():
        #need to test this
        student={"username":str(username),"password":str(password),"schedule":[], "osis":0,"id":0}
        students.insert(student)
        return False
    else:
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

#format for parameter schedule:
#A list length of 10 which contains 10 lists: [list 1, list 2, list 3, ..., list 10]
#for each list within the big list: ["class","teacher"]
def set_schedule(username,schedule):
    db=Connection["StuyWiggles"]
    student=find_student(username)
    student["schedule"]=schedule
    students.update({"username":str(username)},student)

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


