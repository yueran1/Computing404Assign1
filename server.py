#  coding: utf-8 
import SocketServer
import os


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall("OK \r\n")
        self.serve(self.data)

    def serve(self,request):
	
	#We split the reqest line to separate out
	#the address and Http version	
	addr=self.data.split()[1]
        HTTP_Version=self.data.split()[2]

	#If request directory valid, we will redirect
	#request to the index.html
        if(os.path.isdir("www"+addr)):
	    if("/" in addr[-1]):
		addr=addr+"index.html"
	    else:
		addr=addr+"/index.html"

	#Based on the request, update the http mime type at here
	if ".html" in addr:
            mimetype="text/html"
        elif ".css" in addr:
            mimetype="text/css"
	else:
	    mimetype="text/plain"

	
	#Condition of Http status 404
	#If the directory is not exist or there are /../../../
	#in the directory, we will return headers and 404 error page to the
	#user
        if (os.path.exists("www"+addr)==False) or "/../" in addr:
            StatusCode=" 404 Not Found"
            headers= HTTP_Version + StatusCode + "\r\n" + \
                      "Content-type: " + mimetype + "\r\n" +\
                      "www" + addr + "\r\n\r\n" 
            Error_Page="<html><body><h1>404 Not Found</h1>"+\
            		"<p>The requested URL "+ addr + " was not found on this server.</p></body></html>"+"\r\n\r\n"
            Content_Length= str(len(headers)+len(Error_Page))

            headers= HTTP_Version + StatusCode + "\r\n" + \
                     "Content-type: " + mimetype +"\r\n"+"charset=utf-8"+"\r\n"+"Content-Length: "+ Content_Length+ "\r\n"+ \
                     "www" + addr + "\r\n\r\n" 
            self.request.send(headers)
            self.request.send(Error_Page)

	#Condition of Http status 200
	#If the directory do exist, we will of the file in directory,
	#return the Http status 200, headers and display the corresponding webpage.
        else:
	    file= open("www"+addr)
	    location=file.read()
	    file.close()
	    StatusCode=" 200 OK"
	    headers= HTTP_Version + StatusCode + "\r\n" + \
		     "Content-Type: "+mimetype + "\r\n" + "charset=utf-8"+"\r\n\r\n"+ \
		     location + "\r\n"
            Content_Length= str(len(headers))

            headers=  HTTP_Version + StatusCode + "\r\n" + \
		      "Content-Type: "+mimetype +"\r\n"+ "charset=utf-8 "+" Content-Length: "+ Content_Length+"\r\n\r\n" + \
		      location + "\r\n"


	    self.request.send(headers)
	   
	
	
   
		

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
