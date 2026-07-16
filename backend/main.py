from server import create_server
from server.socketHandler import socketio
server = create_server()

if __name__ == "__main__":
    
    socketio.run(server,host=server.config["SERVER_HOST"],
                port=server.config["SERVER_PORT"],
                debug=True,)