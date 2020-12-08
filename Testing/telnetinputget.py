import telnetlib
import time

print ("running get")
telnet = telnetlib.Telnet()
telnet.open('127.0.0.1', 1234)
time.sleep(1.5)
print ("Sendin query")
telnet.write("GET http://localhost:1234/ HTTP/1.1\r\n\r\n")
print(telnet.read_all())
