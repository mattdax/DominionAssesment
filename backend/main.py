from server import create_server

server = create_server()

if __name__ == "__main__":
    server.run(host="localhost",
                port=4000,
                debug=True,)