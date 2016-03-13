#!/usr/bin/env python
import subprocess
import time
import urllib2

class bot:
	def __init__(self, url):
		self.url = url

	def sendMessage(self, chat_id, text):
		urllib2.urlopen(self.url + '/sendMessage?chat_id=' + str(chat_id) + '&text=' + text)

def getServices(ip):
	serv = 'nmap -Pn ' + ip
	(out, err) = subprocess.Popen(serv, stdout=subprocess.PIPE, shell=True).communicate()
	
	serv = []

	if err == None:
		if "Host is up" in out.split('\n')[3]:
			if out.split('\n')[4][:3] != "All":
				for service in out.split('\n')[6:]:
					if service == "":
						break

					serv.append(service.split()[::2]) 

		else:
			print ip, "not up"

	else:
		print "There was an error with the command", comm, '\n', err

	return serv

def main(yourAPIKey, conversationID):


	comm = 'nmap -sP 192.168.100.0/24'
	
	while True:
		usrs = {}
		print "Executing", comm

		proc = subprocess.Popen(comm, stdout=subprocess.PIPE, shell=True)

		(out, err) = proc.communicate()

		if err == None:
			times = 0
			out = out.split('\n')
			while times < 5:
				
				print "Getting services"

				for line in out:
					if "Nmap scan report for" in line:
						ip = line.split()[-1]
						
						if ip[0] == '(':
							ip = ip[1:-1]
						
						usrs[ip] = getServices(ip)

				differences = writeDocAndGetDifferences(usrs,yourAPIKey, conversationID)

				if differences == 1:
					print "Something changed"
					break
				
				if times < 4:
					waitingTime = times * 120 + 120
					print "Waiting for", waitingTime, 'seconds' 
					time.sleep(waitingTime)
					times += 1


		else:
			print "There was an error with the command", comm, '\n', err



def writeDocAndGetDifferences(usr,yourAPIKey, conversationID):

	usrBefore = {}
	with open('log', 'r') as f:

		for line in f:
			line = line.split(':')
			
			usrBefore[line[0]] = []
			
			for i in xrange(0, len(line[1].split()), 2):
				usrBefore[line[0]].append([line[1].split()[i], line[1].split()[i + 1]])

	with open('log', 'w') as f:

		for ip in usr:
			f.write(ip + ':' + ' '.join([serv[0] + ' ' + serv[1] for serv in usr[ip]]) + '\n')

	log = []
	for ip in usr:
		if ip in usrBefore:
			if usr[ip] != usrBefore[ip]:
				log.append(ip + ' down and up with services ' + ' '.join([serv[0] + ' ' + serv[1] for serv in usr[ip]]) if len(usr[ip]) > 0 else ' goes down and up with no services')
			else:
				pass
		else:
			log.append(ip + (' goes up with services ' + ' '.join([serv[0] + ' ' + serv[1] for serv in usr[ip]]) if len(usr[ip]) > 0 else ' goes up with no services'))

	for ip in usrBefore:
		if ip not in usr:
			log.append(ip + ' goes down')

	if len(log) > 0:
		url = 'https://api.telegram.org/' + yourAPIKey
		thisBot = bot(url)
		for l in log:
			thisBot.sendMessage(conversationID, l)
		return 1
	else:
		return 0





if __name__ == "__main__":
	yourAPIKey = 'ENTERHEREYOURAPI'
	conversationID = 00000000
	main(yourAPIKey, conversationID)