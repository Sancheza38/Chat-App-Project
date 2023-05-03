from concurrent import futures
import chat_pb2_grpc
import chat_pb2
import grpc
import time

#-----global-------
messageSaved: any 
tempMsg: str = ""
newJoin: list = []

#--------class ChatServicer---------
'''
    Creates class to handle Chat Service
'''
class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    
    #------init()--------
    def __init__(self) -> None:
         self.subscribers = []
         self.sent_messages = set()

    #-------join()---------
    def join(self, request, context):
            global messageSaved
            print("Joining the Sever")
            print(request)

            #subscribes to broadcast
            self.subscribers.append(context)
            self.sent_messages.add(request.id)
            #newJoin.append([request.name, time.strftime("%H:%M:%S", time.localtime())])
            messageSaved = chat_pb2.ChatMessage(fromUser ="joined", msg = f"{request.name} has joined", time = time.strftime("%H:%M:%S", time.localtime()))
            
            yield chat_pb2.JoinResponse(msg=f"{request.name} has joined")
            
    #--------sendMsg()---------    
    def sendMsg(self, request, context):
        time.sleep(1)
        print("message sent")
        emptyMsg = chat_pb2.Empty()

        #store the message
        global messageSaved
        messageSaved = request
        print(messageSaved)

        return emptyMsg
    
    #--------receiveMsg()--------
    def receiveMsg(self, request, context):
        global tempMsg, counter
        
        #sends broadcast to subscribers
        time.sleep(1)
        for subscriber in self.subscribers:
                 
            try:
                   
                yield chat_pb2.ChatMessage(fromUser = messageSaved.fromUser, msg = messageSaved.msg, time = messageSaved.time)           
            except grpc.RpcError:
                self.subscribers.remove(subscriber)
                print("Thos is the subscriber: ")
                print(subscriber)
                
           
    #------getAlllUsers()--------
    def getAllUsers(self, request, context):
        return super().getAllUsers(request, context)
