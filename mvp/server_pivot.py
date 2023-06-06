import time, subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
hostName = "localhost"
serverPort = 8081 #You can choose any available port; by default, it is 8000
class MyServer(BaseHTTPRequestHandler):  
    def do_GET(self): #the do_GET method is inherited from BaseHTTPRequestHandler
        company = self.path[1:]
        out = subprocess.run(['python', 'server-ml-mainContent.py', company], stdout=subprocess.PIPE)
        print('INSIDE server_pivot')
        content = str(out.stdout)
        content = content[2:len(content) - 5]
        print(content)

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')    
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

def main():
    try:
          webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()  #Executes when you hit a keyboard interrupt, closing the server
        print("Server stopped.")

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))  #Server starts
    main()
