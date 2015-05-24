#!/usr/bin/python

# DESCRIPTION
# This is a basic housekeeping mailer designed to send reminders from
# the "remind" package, tasks (from "taskwarrior"), ip info (both
# internal and external), temperature, and uptime info.
# For me, this command is on a cron, giving me an update daily.
#
# Comments, suggestions, edits, and tips are welcome and appreciated.
#
# LICENSE
# Copyright (C) 2015  Kyle Colton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os, urllib2, os.path, smtplib, getopt, time, sys
from subprocess import Popen, PIPE
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main(argv):
	
	recipient = 'your.email@domain'
	subject = "Email Subject "#server time is appended
	verb = False
	
	try:
		opts, args = getopt.getopt(argv,"he:s:v",["help","email=","subject="])
	except getopt.GetoptError:
		help()
		print "Wrong arguments.\nExiting\n"
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', "--help"):
			help()
			sys.exit()
		if opt in ('-e', "--email"):
			recipient = arg
		if opt in ('-s', '--subject'):
			subject = arg
		if opt in ('-v'):
			verb = True
	collector(recipient, subject,verb)
			
def collector(to_address, subj, verb):
	(stdout, stderr) = Popen(["remind","/path/to/.reminders"],stdout=PIPE).communicate()
	reminders = stdout

	(stdout, stderr) = Popen(["task"], stdout=PIPE).communicate()
	tasks = stdout

	(stdout, stderr) = Popen(["/sbin/ifconfig","eth0"], stdout=PIPE).communicate()
	int_eth0 = stdout

	ext_ip = urllib2.urlopen('http://checkip.dyndns.org').read()
	ext_ip = ext_ip.split('Address: ',1)[-1]
	ext_ip = ext_ip.split('</body>',1)[0]

	(stdout, stderr) = Popen(["/opt/vc/bin/vcgencmd","measure_temp"], stdout=PIPE).communicate()
	temp = stdout

	(stdout, stderr) = Popen(["uptime"], stdout=PIPE).communicate()
	uptime = stdout
	
	from_address = 'sender address'

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subj +  str(int(time.time()))
	msg['From'] = 'sender address'
	msg['To'] = 'recipient address'

	html = """\
	<html>
	<head></head>
	<body>
	<h3>Reminders</h3>
	""" + reminders.replace('\n','<br>') + """\
	<br><h3>Tasks</h3><PRE><tt>
	""" + tasks.replace('\n','<br>') + """</tt></PRE>\
	<br><h3>External IP</h3><tt>
	""" + ext_ip.replace('\n','<br>') + """</tt>\
	<br><h3>Internal IP</h3><PRE><tt>
	""" + int_eth0.replace('\n','<br>') + """</tt></PRE>\
	<br><h3>Temperature IP</h3><tt>
	""" + temp.replace('\n','<br>') + """</tt>\
	<br><h3>Uptime IP</h3><tt>
	""" + uptime.replace('\n','<br>') + """</tt>\
	</body>
	</html>
	"""

	msg.attach(MIMEText(html, 'html'))

	# Credentials
	u = 'sender username'
	p = 'sender password'

	serv = smtplib.SMTP('smtp.gmail.com:587')
	serv.starttls()
	serv.login(u,p)
	serv.sendmail(from_address,to_address,msg.as_string())
	serv.quit()


def help():
	print "\nUsage: " + sys.argv[0] + " [OPTION] ..."
	print "Daily mailer with housekeeping info\n"
	print "Arguments:\n"
	print "  -h, --help\t\tdisplay this help and exit"
	print "  -e, --email\t\tspecify the email to send the message to"
	print "  -s, --subject\t\tspecify the subject for the email to have"
	print "  -v\t\t\tverbose output"
	print "\nCreated by Kyle Colton\nComments, tips, edits, etc. are welcome\nVersion 0.2\n"

	
if __name__ == "__main__":
  main(sys.argv[1:])
