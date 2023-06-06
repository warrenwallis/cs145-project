import socketserver, subprocess

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        parsed_data = str(self.data).split(" ")
        company = (parsed_data[1])[1:]
        print(company)
        out = subprocess.run(['python', 'server-ml-mainContent.py', company], stdout=subprocess.PIPE)

        # will need data received from subprocess and use self.request.sendall() to send data back, preferably JSON
        content = str(out.stdout)
        content = content[2:len(content) - 5]
        print(content)
        to_send = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: ' + str(len(str(content))) + '\r\nConnection: close' + str(content)
        print(to_send)
        self.request.sendall(to_send)
        exit(0)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()