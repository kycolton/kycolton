#!/usr/bin/python

# DESCRIPTION
# This program is designed to capture events from a Tektronix DPO3000
# oscilloscope over ethernet via a python-telnet script.
# This was in particular written to capture rise-time and amplitude
# on two channels of the scope, but it could easily be modified for
# almost any function of the DPO3000. The manual (see NOTES) is good
# about describing the commands and interface.
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
# NOTES
# Tektronix manual
# http://www.tequipment.net/assets/1/26/Documents/Tektronix/dpo3000_programmermanual.pdf
#

import telnetlib, time, datetime, string, sys, getopt, os.path, smtplib
from datetime import datetime # but seriously, this is needed
from time import sleep

def main(argv):
  
    HOST = "192.168.1.1"            # IP of the scope
    PORT = "4000"                   # Scope's port (Default is 4000)
    TIMEOUT = 10                    # Timeout in seconds
    verb = False                    # Vebose
    data_file = "/tmp/o_test.csv"	# File to append all the data
    image_prefix = "NA"				# File location to save pictures (must be on scope for the time being)
    samples = 500					# Number of samples to take
    initial = 0
    offset = 0						# Offset amount to start numbering at (i.e. start at sample #50)
    warn_email = "NA"				# Email to send info/warnings to
    two_channel = False				# Measure 2 channels

	try:
		opts, args = getopt.getopt(argv,"hi:p:t:f:g:n:o:vw:c",["help","ip=","port=","file=","timeout=","image=","samples=","offset=","warn=","two_ch"])
	except getopt.GetoptError:
		help()
		print "Wrong arguments.\nExiting\n"
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', "--help"):
			help()
			sys.exit()
		if opt in ("-i", "--ip"):
			HOST = arg
		if opt in ("-p", "--port"):
			PORT = arg
		if opt in ("-t", "--timeout"):
			try:
				TIMEOUT = int(arg)
			except:
				print "Error: Non-numeric Timeout.\nExiting"
				sys.exit(3)
		if opt in ("-f", "--file"):
			data_file = arg
		if opt in ("-g","--images"):
			image_prefix = arg
		if opt in ("-n","--samples"):
			try:
				samples = int(arg)
			except:
				print "Error: Non-numeric sample number.\nExiting"
				sys.exit(3)
		if opt in ("-o","--offset"):
			try:
				offset = int(arg)
			except:
				print "Error: Non-numeric offset.\nExiting"
				sys.exit(3)
		if opt in ("-w","--warn="):
			warn_email = arg
			print("WARNING: EMAIL FUNCTIONALITY NOT FINISHED.")
		if opt in ("-v"):
			verb = True
		if opt in ("-c","--two_ch"):
			two_channel = True
	
	# Calculate any offset
	initial = initial + offset
	samples = samples + offset
	# Test opening the file
	try:
		f = open(data_file,'a')
	except:
		print "Error opening file\nExiting\n"
		sys.exit(5)

	# Verbose
	if verb:
		print("Calling scope at "+str(HOST)+":"+str(PORT)+" with timeout of "+str(TIMEOUT)+" seconds for "+str(samples)+" samples")
		print("Data is logged to "+data_file)
		print("Images prefix is: "+image_prefix)
		print("Measuring "+str(int(two_channel)+1)+" channels")
	sample( HOST, PORT, TIMEOUT, data_file, image_prefix, samples, initial, f, two_channel, verb )

# Function for recording samples from the scope
def sample( HOST, PORT, TIMEOUT, data_file, image_prefix, samples, i, f, two_ch, verb ):

	tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
	# Clear the buffer of the welcome screen
	data = tn.read_until("milliseconds\r\n",TIMEOUT)
	if verb:
		print("\nINITIAL DUMP\n"+data+"END INITIAL DUMP\n")

# ===========
# SINGLE SHOT
# ===========

	while i < samples:
		# Single shot
		tn.write("ACQ:STATE ON\r\n")
		# Test if the single shot is done
		tn.write("ACQ:STATE?\r\n")
		state = tn.read_until("0",1)
		if verb:
			print("State: "+state)
		t=0
		while state != "0":
			tn.write("ACQ:STATE? \r\n")
			state = (tn.read_until("\n")).replace(">","").strip()
			if verb:
				print(str(t)+". State: "+str(state))
			t=t+1
			sleep(1) # sleep for a second before checking again
			if t > 60:
				tn.close()
				graceful_exit("Warning: No event detected for one minute, exiting.",4)
				
# =============
# FIRST CHANNEL
# =============

		if verb:
			print("Capture")
		# Let the Scope work for a second
		sleep(1)
		
		if two_ch:
			if verb:
				print("Measuring first channel")
			tn.write("MEASU:IMM:SOU CH1\r\n")
		
		# Get Rise
		tn.write("MEASU:IMMED:TYPE RISE\r\n")
		tn.write("MEASU:IMMED:VAL?\r\n")
		sleep(.1)
		rise = (tn.read_until("\n")).replace(">","").strip()

		if verb:
			print("Wave Rise: "+str(rise))

		# Get Amplitude
		tn.write("MEASU:IMMED:TYPE AMP\r\n")
		tn.write("MEASU:IMMED:VAL?\r\n")
		sleep(.1)
		amp = (tn.read_until("\n")).replace(">","").strip()

		if verb:
			print("Wave Amplitude: "+str(amp))

# =======================
# OPTIONAL SECOND CHANNEL
# =======================
		
		if two_ch:
			if verb:
				print("Measuring second channel")
			tn.write("MEASU:IMM:SOU CH2\r\n")
				
			# Get Rise
			tn.write("MEASU:IMMED:TYPE RISE\r\n")
			tn.write("MEASU:IMMED:VAL?\r\n")
			sleep(.1)
			rise2 = (tn.read_until("\n")).replace(">","").strip()

			if verb:
				print("Wave Rise: "+str(rise2))

			# Get Amplitude
			tn.write("MEASU:IMMED:TYPE AMP\r\n")
			tn.write("MEASU:IMMED:VAL?\r\n")
			sleep(.1)
			amp2 = (tn.read_until("\n")).replace(">","").strip()
		
			if verb:
				print("Wave Amplitude: "+str(amp2))
			
# ========================
# RECORD TIMES / SAVE DATA
# ========================

		# Get Oscilloscope time
		tn.write("TIME?\r\n")
		o_time = (tn.read_until("\n")).replace(">","").strip()
		o_time = o_time.replace("\"","")
		
		if verb:
			print("Oscilloscope Time: "+o_time)
		
		# Get Server time
		s_time = str(datetime.now())

		if verb:
			print("Server Time: "+s_time)

		pre_csv = str(i)+","+s_time+","+o_time+","+str(rise)+","+str(amp)
		if (two_ch):
			pre_csv = pre_csv+","+str(rise2)+","+str(amp2)
		
		if image_prefix == "NA":
			csv_form = pre_csv +",NA\n"

		# Save image
		if image_prefix != "NA":
			sav_img = "SAV:IMAGE \"E:/"+str(image_prefix)+"_"+str(i)+".png\"\r\n"
			tn.write(sav_img)
			if verb:
				print("Image Saved as "+sav_img)
			csv_form = pre_csv+",\"E:/"+str(image_prefix)+"_"+str(i)+".png\"\n"
			sleep(2) # Let the scope save, without this, data is thrown off

		if verb:
			print(csv_form)
		f.write(csv_form)
		# Increase i
		i=i+1
	
	tn.close() # Close the telnet, then gracefully exit
	graceful_exit("Finished at sample "+str(samples)+".",0)

def help():
	print "\nUsage: " + sys.argv[0] + " [OPTION] ..."
	print "Log amplitude and rise times for a waveform as detected by a Tectronix Oscilloscope\n"
	print "Arguments:\n"
	print "  -h, --help\t\tdisplay this help and exit"
	print "  -i, --ip\t\tspecify the ip that the scope is at"
	print "  -p, --port\t\tspecify the port the scope is listening on"
	print "  -t, --timeout\t\tspecify the amount of time to wait for a reply"
	print "  -f, --file\t\tspecify the file to write data to"
	print "  -g, --images\t\tspecify the image name prefix, save under a folder by using foo/bar"
	print "  -n, --samples\t\tspecify the number of samples to capture"
	print "  -o, --offset\t\tallows the user to start at any sample number"
	print "  -w, --warn\t\tis a planned function that allows the program to send info or warning emails"
	print "  -c, --two_ch\t\ttwo channel capture"
	print "  -v\t\t\tverbose output"
	print "\nCreated by Kyle Colton, \nComments, tips, edits, etc. are welcome\nVersion 0.4\n"

def graceful_exit(m,status,to_address = 'NA'):
	# Future function to come
	# 1. Print message to screen
	print(m)
	
	# 2. Email message from a gmail account to a preselected address
	# 	 Not yet implemented
	if to_address != 'NA':
		print "Sending Mail..."
		from_address = 'email address here'
		subject = 'Scope Warning!'
		if status == 0:
			subject = 'Scope Information'
		
		message = 'Subject: %s\n\n%s' % (subject,m)
		
		# Credentials
		u = 'username'
		p = 'password'
		
		
		serv = smtplib.SMTP('smtp.gmail.com:587')
		serv.starttls()
		serv.login(u,p)
		serv.sendmail(from_address,to_address,message)
		
	# 3. Exit
	sys.exit(status)
	
if __name__ == "__main__":
  main(sys.argv[1:])
