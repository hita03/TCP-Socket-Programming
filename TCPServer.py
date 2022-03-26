from socket import *
import json

def write_json(newobj, filename='data.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["users"].append(newobj)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def addUser(srn,name):
    newobj = {"name":name,
            "credits":50,
            "borrows":[],
            "srn":srn }
    write_json(newobj)
    # newobj=json.dumps(newobj)
    # print(newobj)
    # data["users"].append(newobj); 
    # print("Your account has been registered. You are provided with 50 credits to start with.")



def disp_user(srn,name):
    f =open('data.json')
    flag=0
    data = json.load(f)
    for i in data['users']:
        #print(i['srn'],srn,type(i['srn']) ,type(srn))
        if i['srn']==srn:
            f.close()
            flag=1
            return i
    if flag==0:
        f.close()
        addUser(srn,name)
    x=[]    
    return x
def send_books(flag,obj):

    if flag ==0:
        f =open('data.json')
        data = json.load(f)
        f.close()
        return data['books']
    else:
        return_books =[]
        f = open('data.json')
        data = json.load(f)
        obj=json.loads(obj)
        #print("obj:  ",obj,type(obj))
        for i in data['users']:

            if i['srn'] == obj['srn']:
                for j in data['books']:
                    for k in i['borrows']:
                        if j['uid'] == k:
                            return_books.append(j)


        f.close()
        return return_books


def borrow_user(uids,obj):
    sum=0
    f = open('data.json')
    data = json.load(f)
    obj=json.loads(obj)
    #print("obj:  ",obj,type(obj))
    for i in data['books']:
        for j in uids:
            if i['uid'] == j:
                sum+=i['credits']

    f.close()


    with open('data.json','r+') as file:
        data = json.load(file)
        temp=0
        for item in data['users']:
            if item['srn'] == obj['srn']:
                item['credits']-=sum
                if item['credits'] < 0:
                    file.close()
                    return "Insufficient credits! Add credits to borrow."

                for x in uids:
                    item['borrows'].append(x)
                #print("borrowed list ",item['borrows'])
                temp=item['credits']
    
        file.seek(0)
        json.dump(data,file,indent=4)
        file.close()
        return temp


def return_user(uids,obj):
    obj = json.loads(obj)
    book_names=[]
    temp=[]
    with open('data.json','r+') as file:
        data = json.load(file)

        for item in data['users']:
            if item['srn'] == obj['srn']:
                for x in uids:
                    item['borrows'].remove(x)
                #print("remaining borrowed books list ",item['borrows'])
                temp=item['borrows']        
        file.seek(0)
        file.close()

    open('data.json', 'w').close()

    with open('data.json','r+') as file:
        json.dump(data,file,indent=4)
        file.close()

    f = open('data.json')
    data = json.load(f)
    for i in data['books']:
            for j in temp:
                if i['uid'] == j:
                    book_names.append(i['title'])
    #print(book_names)
    f.close()                
    return book_names
                    

def add_credits(obj,c):
    obj = json.loads(obj)
    with open('data.json','r+') as file:
        data = json.load(file)
        for i in data['users']:
            if obj['srn'] == i['srn']:
                i['credits'] +=c
                total = i['credits']
        file.seek(0)
        file.close()

    open('data.json', 'w').close()

    with open('data.json','r+') as file:
        json.dump(data,file,indent=4)
        file.close()
    return total
    


def check_valid_uid(obj,uids):
    obj = json.loads(obj)
    f = open('data.json')
    data = json.load(f)
    flag=1
    for i in data['users']:
        if i['srn']==obj['srn']:
            for j in uids:
                #flag=1
                if j in i['borrows']:
                    pass
                else:     
                    flag=0
                    #("flaggg!!! ",flag,end=" ")
                    f.close()
                    return flag  

    f.close()
    return flag


serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('' ,serverPort))
serverSocket.listen(1)
while True:
    connectionSocket, addr = serverSocket.accept()
    name = connectionSocket.recv(1024).decode()
    srn = connectionSocket.recv(1024).decode()
    ack = "positive"
    nak="negative"
    obj= json.dumps(disp_user(srn,name))
    #print("obj:   ",obj,type(obj))
    if obj!="[]":
        connectionSocket.send(ack.encode())
        ack=connectionSocket.recv(1024).decode()
        connectionSocket.send(obj.encode())
    else:
        connectionSocket.send(nak.encode())
        ack=connectionSocket.recv(1024).decode()
        connectionSocket.send("Oops you aren't registered. We'll Register you ;)".encode())


    connectionSocket.send( "ack".encode()) #sending books
    choice=connectionSocket.recv(1024).decode()
    if choice == "borrow":
        l = json.dumps(send_books(0,""))
        connectionSocket.send( l.encode())
    else:
       return_books = json.dumps(send_books(1,obj))
       connectionSocket.send(return_books.encode())     
    # choice=connectionSocket.recv(1024).decode()
    uid = connectionSocket.recv(1024).decode()
    #print(type(uid),uid)
    uids=json.loads(uid)
    #print(type(uids),uids)
    if choice == "borrow":
        c = borrow_user(uids,obj)
        if(type(c) == type("nak")):
            connectionSocket.send("nak".encode())
        else:
            c=str(c)
            connectionSocket.send(c.encode())
    else:
        flag = check_valid_uid(obj,uids)
        
        #print("flag value: ",flag)
        if flag ==1:
            remaining_books = json.dumps(return_user(uids,obj))
            connectionSocket.send(remaining_books.encode())
        else:
            remaining_books = "invalid"
            connectionSocket.send(remaining_books.encode())
            connectionSocket.close()
            exit()
    
    response = int(connectionSocket.recv(1024).decode())
    if response!=0:
        total= str(add_credits(obj,response))
        connectionSocket.send(total.encode())
    else:
        connectionSocket.send("nak".encode())

    connectionSocket.close ()