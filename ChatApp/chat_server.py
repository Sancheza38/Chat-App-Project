from concurrent import futures
import grpc
import chat_pb2_grpc
import chat_pb2
import time
#-----global-----
messageSaved1: any
_ONE_DAY_IN_SECONDS = 86400

#--------class ChatServicer---------
class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def join(self, request, context):
        print("Joining the Sever")
        print(request)
        joinMessage = chat_pb2.JoinResponse()
        joinMessage.msg = f"{request.name} has joined"
        yield chat_pb2.JoinResponse(msg=f"{request.name} has joined")
    
    def sendMsg(self, request, context):
        print("message sent")
        emptyMsg = chat_pb2.Empty()
        #store the message
        global messageSaved1
        messageSaved1 = request
        print(messageSaved1)
        return emptyMsg
    
    def receiveMsg(self, request, context):
        msgRecieved = chat_pb2.ChatMessage()
        msgRecieved.message = f"{messageSaved1.fromUser}: {messageSaved1.msg} at {messageSaved1.time}"
        msgRecieved.message = "Hello"
        yield msgRecieved
    
    def getAllUsers(self, request, context):
        return super().getAllUsers(request, context)




#chat server main start 
#--------server()-----------
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port("localhost:5000")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
    # server.wait_for_termination()

#------main-------
if __name__ == "__main__":
    server()