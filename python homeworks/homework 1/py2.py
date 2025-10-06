from socket import *
#Create a TCP server socket
serverName = 'localhost'
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)
while True:
    #Establish the connection
    print("The server is ready to receive")
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open("./html_files/" + filename[1:])
        outputdata = f.read()
        print("File content preview:", outputdata[:100])

        #Send HTTP OK and the Set-Cookie header into the socket
        # set the cookie to whatever value you'd like
        #Code Start
        header = 'HTTP/1.1 200 OK\r\n'
        header += 'Content-Type: text/html\r\n'
        header += 'Set-Cookie: user=cs4793-student; Path=/\r\n'
        header += '\r\n'
        connectionSocket.send(header.encode())
        #Code End
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        # Close the socket
        #Code Start
        connectionSocket.close()
        #Code End
    except IOError:
        #Send HTTP NotFound response
        #Code Start
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
        response += """
            <html>
            <head><title>404 Not Found</title></head>
            <body>
              <h1>404 Not Found</h1>
              <p>The requested file was not found on this server.</p>
            </body>
            </html>
            """
        connectionSocket.send(response.encode())
        #Code End
        # Close the socket
        #Code Start
        connectionSocket.close()
        #Code End
serverSocket.close()