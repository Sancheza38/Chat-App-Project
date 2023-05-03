from concurrent import futures
import chat_pb2_grpc
import chat_pb2
import grpc
import time
import chat_service


#--------server()-----------

class Server(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.chats = []

    def receiveMsg(self, request_iterator, context):
        
        lastindex = 0
        while True:
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def sendMsg(self, request: chat_pb2.ChatMessage, context):
        print("[{}] <{}> {}".format(request.time, request.fromUser, request.msg))
        self.chats.append(request)
        return chat_pb2.Empty()
    

#------main-------
if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(Server(), server)
    print("Server started, Listening...")
    server.add_insecure_port("localhost:5000")
    server.start()
    while True:
        time.sleep(64 * 64 * 100)
