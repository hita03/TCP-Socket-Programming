from socket import *
import requests
import json
from tabulate import tabulate
import pandas as pd

       
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName , serverPort))
print ('Welcome to Good Books!')
name=input("Enter your name: ").lower()
print("Check name: ",name) 
clientSocket.send(name.encode())
srn= input('Enter SRN: ')
clientSocket.send(srn.encode())


ack = clientSocket.recv(1024).decode()
print(ack)
if  ack == 'positive':
    i = clientSocket.recv(1024).decode()
    j = json.loads(i)
    print("Hello, ",j['name'],"!")
    print("Your Credit Wallet: ",j['credits'])
else:
    message = clientSocket.recv(1024).decode()
    print(message)

choice=int(input("Do you want to: 1.Borrow Books  |   2.Return Books ? "))
if choice == 1:
    if  clientSocket.recv(1024).decode() == "ack":
        clientSocket.send("ack".encode())
        books = clientSocket.recv(1024).decode()
        
        books = json.loads(books)
        print(type(books))
        clientSocket.send("borrow".encode())
        df = pd.DataFrame(books)
        print(tabulate(df, headers="keys"))
        #for i in books:    
        #    print(i['title']," (",i['uid'],")", " C-",i['credits'] )
        uid= input('Enter UID of books you want to borrow (comma separated): ')
        print(uid)
        uid=uid.split(",")
        print(type(uid))
        uid=json.dumps(uid)
        clientSocket.send(uid.encode())

        message=clientSocket.recv(1024).decode()
        if message == "nak":
            print("Insufficient credits! Add credits to borrow.")
        else:
            print("Done! You have ",message," credits left.")

        opt = input("Do you want to add credits? (y/n): ")
        if opt == 'y' or opt == 'Y':   
            value = int(input("Enter number of credits you want to be added: "))
            clientSocket.send(str(value).encode())
        else:
            clientSocket.send("0".encode())

        message = clientSocket.recv(1024).decode()
        if message == 'nak':
            pass
        else:
            print("Your total credits now are: ",message)

        print("Thank you! Come Back Again")    

    else:
        print("Error in socket communication.Try Again.")
        exit()

elif choice == 2:
    print("in choice 2")
    message = clientSocket.recv(1024).decode()
    print("message: ",message)
    if  message == "ack": #sending books
        clientSocket.send("ack".encode())
        books = clientSocket.recv(1024).decode()
        books = json.loads(books)
        clientSocket.send("return".encode())
        df = pd.DataFrame(books)
        print(tabulate(df, headers="keys"))
        uid= input('Enter UID of books you want to return (comma separated): ')
        print(uid)
        uid=uid.split(",")
        print(type(uid))
        uid=json.dumps(uid)
        clientSocket.send(uid.encode())
        remaining_books=json.loads(clientSocket.recv(1024).decode())
        print("Books left to return: ")
        print(remaining_books)
        #insert pandas table here


        opt = input("Do you want to add credits? (y/n): ")
        if opt == 'y' or opt == 'Y':   
            value = int(input("Enter number of credits you want to be added: "))
            clientSocket.send(str(value).encode())
        else:
            clientSocket.send("0".encode())

        message = clientSocket.recv(1024).decode()
        if message == 'nak':
            pass
        else:
            print("Your total credits now are: ",message)

        print("Thank you! Come Back Again")    

        
        #  for x in remaining_books:
        #     print()
        # print("You have "," left to return.")

    # if clientSocket.recv(1024)== "positive":
        #print(' From Server: ', modifiedSentence.decode())
    else:
        print("Error in socket communication.Try Again.")
        exit()

else:
    print("Invalid Option.")
    exit()    


clientSocket.close( )