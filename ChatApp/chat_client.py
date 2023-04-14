import chat_pb2_grpc
import chat_pb2
import grpc
import sys
from datetime import datetime
#--------global-------
userName: str = ""

#handles stream request from client side
#---------getClientStreamRequest()--------
def getClientStreamRequest():
    #sending messages
    while True:
        message = input("Enter your message")
        messageSent = chat_pb2.ChatMessage(fromUser = userName, msg = message, time = 0)
        yield messageSent

# #gets the users name to join   
# # ----------getClientUser()-------    
# def getClientUser():
#     #joining the group
#     name = input("Enter the name to use to join: ")

#     if name == "exit()":
#         sys.exit()

#     global userName
#     userName = name
#     idName = userName + "1"
#     joinUser = chat_pb2.User(id = idName, name = userName)
#     yield chat_pb2.User(id="hello1", name ="Batman")

#handles the port to send messages 
#----------run()----------
def run():
    with grpc.insecure_channel('localhost:5000') as channel:
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            sys.exit("Error connecting to server")
        else:
            stud = chat_pb2_grpc.ChatServiceStub(channel)
        username = input("Please enter a user name: ")
        joinMessage = stud.join(chat_pb2.User(id="hello!", name=username))

        print("Join receieved: ")
        print(joinMessage)

        while True:
            userMsg = input()
            curr_time = datetime.now().strftime("%H:%M:%S")
            emptyMsg =  stud.sendMsg(chat_pb2.ChatMessage(fromUser=username, msg=userMsg, time = curr_time))
            #responses = stud.receiveMsg(chat_pb2.Empty())
            print("[" + curr_time + "] <" + username + ">", userMsg)
            #print(responses)

#--------main-----------
if __name__ == "__main__":
    run()


