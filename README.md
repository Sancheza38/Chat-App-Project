# Chat-App-Project

## Contributions
<u>Alexander Sanchez</u>: Implementing GUI using TKinter and helped with chat server and client implementation, and presentation slides. <br><br>

<u>Edwin Morin</u>: Implementing chat server and client and presentation slides. <br><br>

<u>Jorge Hernandez</u>: Helped with GUI and chat server/client  implementations, wrote final report, README, and presentation slides. <br><br>

## Replicating Work
### Installing gRPC
First, we must install the gRPC framework the project uses. To do so, you must first have Python (version 3.10 or higher) installed and run the following commands:
```
python -m pip install grpcio
python -m pip install grpcio-tools
```

### Running the program
To run the chat app, first launch the server by using the following command:
```
py chat_server.py
```

Then, launch the chat client by using the following command:
```
py chat_client.py
```

Type in your desired username and press "OK". Then the chat application has been officially launched and is in use! You can launch multiple user clients by using the command above and have them communicate with each other.

For the purposes of this project, we used a local network environment.