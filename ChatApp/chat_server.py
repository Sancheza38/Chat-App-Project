from concurrent import futures
import chat_pb2_grpc
import chat_pb2
import grpc
import time
import chat_service


#--------server()-----------
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(chat_service.ChatServicer(), server)
    server.add_insecure_port("localhost:5000")
    server.start()
    server.wait_for_termination()

#------main-------
if __name__ == "__main__":
    server()
