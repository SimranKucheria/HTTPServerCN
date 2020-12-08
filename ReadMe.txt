System Requirements

sudo apt-get install python-magic
python -m pip install lzw
python -m pip install langid

Partner: 111803134(Shruti Susan Mathews)

To run

Set Server/server.conf with all the correct paths

Go to directory of project and run
./startserver.sh wait for "Server Running"-else connection refused errors

To stop the server type
./stopserver.sh (located in same directory)

Conformance tests(Various kinds of queries and requests)
We used postman to create and send queries that we then saved and exported as a .json file(ConformanceTest.json)
To run these, download the postman app and import the json file
Go to Runner and run the collection.

The MT testing can be tested by using the folder Testing
Go to the folder
and run python MTtestingsuite.py(No need to start/stop the server)

Files in the project

htmldocs folder with html documents(Can be set via DocumentRoot in server.conf)

Inside the Server folder we have various modules
httpserver-main file that calls other modules
Put.py-handles put requests
get.py-handles get/head requests
post.py-handles post requests
del.py-handles delete requests
codes.py-Sets the data for HTTP codes returned
Compressedclean.py-handles all the content negotations
ForFiles.py-Runs before the server starts accepting connection. Helps server in content negotiation

We also have a confiles folder that contains

Server.conf- set locations for htmldocs, and other files that will drive content negotiation

Version.txt-if a particular file has multiple versions that can be sent out depending on content negotiation, user needs to add name of file here(Just name)

Redirect.txt-if a particular file is under maintenance and needs to be redirected, add in this file.
SYNTAX:- name of file requested;entire url to redirected file,code(301,302)

Protect.txt-If any files require additional authentication add them here.
SYNTAX:-name of file;U/N;P/W;(protect/proxy)-depending on what authentication is req

error/    -collection of all html pages that are sent when an error code occurs

logs/     - error and access logs

varfiles/ -used for content negotiation

Headers Implemented
Accept: Content-Type(Entity Header)
Accept-Charset: raises 406(not acceptable)
Accept-Encoding: Content-Encoding(Entity Header)
Accept-Language: Content-Language 
Authorization: sent after 401 and WWW-Authenticate in response
Expect: Send codes 100/417
From: (Nothing needs to be done so just allows user to input)
Host:400 if no host
If-Modified-Since: codes are 200 and 304
If-Range:codes 200/206 (Check Accept-Ranges below)(Mostly No)
If-Unmodified-Since:error code is 412
Proxy Authorization: sent after 407 Proxy-Authenticate in response
Range:Codes200/206/416
TE: Just returns a string(Allows user to input but we dont send anything in return)
UA: Sends a string

Response headers
Accept-ranges: return bytes wherever req
Age:related to proxy cache(So proxy authenticate ke saath nahi implement kiya)
Location:for 301/302/308
Proxy-Authenticate:sets it as basic along with 407
Retry After: setting a value of 5 secs
Server: return a sting only(Ubuntu wala)(Input in dic) 
WWW-Authenticate:Authentication method to be used along with 401

Entity Headers
Allow
Content-Encoding
Content-Language
Content-Length
Content-Location
Content-MD5
Content-Range
Content-Type
Last-Modified

General Headers:
Date
Connection
Cache-Control
Pragma

Status Codes that are done:
100
200
201
204
206
301
302
304
400
401
403
404
405
406
407
408
409
411
412
416
417
501
505


