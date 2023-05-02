import chat_pb2_grpc
import chat_pb2
import time
import grpc
import sys
import threading
#--------global-------
userName: str = ""
gCommand : str = ""
oldMsgTime : str = time.strftime("%H:%M:%S", time.localtime())
joinedTime : str = ""

  
# ----------getClientUser()-------
'''
    This will ask the user to enter a username for the server

    Pre: stub type ChatServiceStub

    Post: sends a join message to the server
'''   
def getClientUser(stub) -> object:

    name = input("Enter the name to use to join: ")

    if name == "exit()":
        sys.exit()

    global userName, joinedTime
    userName = name
    idName = userName + "1"
    joinedTime = time.strftime("%H%M%S", time.localtime())
   
    return stub.join(chat_pb2.User(id=idName, name = userName))




#---------getClientStreamRequest()--------
'''
    This sends a empty messages to server to get an update on messages 
    the is sending

    Pre: stub stub type ChatServiceStub

    Post: prints new messages
'''
def getClientStreamRequest(stub: any) -> object:
   
    global oldMsgTime
    #getting messages
    while True:
       #break out of loop
        if(gCommand == "!quit"):
            break
            # "[" + curr_time + "] <" + username + ">", userMsg
        try:
            for message in stub.receiveMsg(chat_pb2.Empty()):
                
                if(message.time != oldMsgTime and (int(joinedTime) < int(message.time.replace(":", "")))):
                    if(message.fromUser == "joined" and (int(oldMsgTime.replace(":", "")) < int(message.time.replace(":", "")))):
                        print(f" [{message.time}] <{message.fromUser}> {message.msg}\n")
                        # print(f"{message.msg} \n")
                        oldMsgTime = time.strftime("%H:%M:%S",time.localtime())
                    elif(message.fromUser != "joined"):
                        print(f" [{message.time}] <{message.fromUser}> {message.msg}\n")
                        oldMsgTime = message.time     
        except grpc.RpcError as e:
                #print(e)
                time.sleep(2)


#-------sendClientMessage()--------
'''
    Send message to server to communicate with other clients

    Pre: stub stub type ChatServiceStub

    Post: no return / sends message to server
'''
def sendClientMessage(stub):
    while True:
        message = input("Enter your message:\n")
        if(message == "!quit"):
            global gCommand
            gCommand = "!quit"
            break

        userTime = time.localtime()
        currentUserTime = time.strftime("%H:%M:%S", userTime)
        stub.sendMsg(chat_pb2.ChatMessage(fromUser = userName, msg = message, time = currentUserTime))




#----------run()----------
'''
    Handles the locating the channel

    Pre: none

    Post: no return / connects to server
'''
def run():
    with grpc.insecure_channel('localhost:5000') as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        joinMessage = getClientUser(stub) #stud.join(chat_pb2.User(id="hello1", name ="Batman"))

        """for message in joinMessage:
            print(message.msg)"""

        #thread started here
        t1 = threading.Thread(target = getClientStreamRequest, args =(stub,))
        t1.start()

        t2 = threading.Thread(target = sendClientMessage, args=(stub,))
        t2.start()

        t1.join()
        t2.join()



#--------main-----------
if __name__ == "__main__":
    run()
    


