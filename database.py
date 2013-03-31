from pymongo import Connection


Connection=Connection('mongo2.stuycs.org')
db=Connection.admin
res=db.authenticate('ml7','ml7')
db=Connection["StuyWiggles"]
students=db.students

#default: 
#username: Osis
#password: 4 digit ID
def add_student(username,password):
    db=Connection["StuyWiggles"]
    if not username in get_usernames():
        student={"username":str(username),"password":str(password)}
        students.insert(student)

def get_usernames():
    db=Connection["StuyWiggles"]
    names=[]
    for line in students.find():
        names.append(str(line["username"]))
    return names

def set_password(username,password):
    db=Connection["StuyWiggles"]
    student=students.find_one({"username":str(username)})
    student={"username":str(username),"password":str(password)}
    students.update({"username":username},student)


