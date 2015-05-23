#!/usr/bin/python

# DESCRIPTION
# This program is designed to listen to a port and log all data
# collected between two instances of a 0xC0 hex duple (KISS TNC FEND).
# It was specifically designed to monitor a soundmodem output stream.
# As data is collected, it is written to a directory with the specified
# parameters as "satelliteName-time-zone.log"
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

import serial, time, sys, getopt, os.path
from time import gmtime

def main(argv):

  satName = ''			# Name of the satellite
  devName = ''			# Name of the device the TNC is dumping to
  baudrate = None		# Baudrate of the TNC write
  utc = False			# Whether to use UTC or local time for timestamp, local by default
  verb = False			# Verbose mode

  try:
    opts, args = getopt.getopt(argv,"hud:s:b:v",["help","utc","device=","satellite=","baudrate="])
  except getopt.GetoptError:
    help()
    print "Wrong arguments, exiting"
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-h', "--help"):
      help()
      sys.exit()
    if opt in ("-u", "--utc"):
      print "Making UTC true"
      utc=True
    if opt in ("-d", "--device"):
      devName = arg
    if opt in ("-s", "--satellite"):
      satName = arg
    if opt in ("-b", "--baudrate"):
      baudrate = arg
      try:
	int(baudrate)
      except:
	print "Error: Non-numeric baudrate.\nExiting"
	sys.exit(3)
    if opt in ("-v"):
      verb = True

  if satName == '':
    print "Warning: No satellite name entered"
  if devName == '':
    devName = "/tmp/soundmodem0"
    print "Warning: Assuming device is " + devName
  if not baudrate:
    baudrate = 9600
    print "Warning: Assuming baudrate is " + str(baudrate)

  # Verbose
  if verb:
    print "Calling record( " + str(utc) + ", " + devName + ", " + satName + ", " + str(baudrate) + ", " + str(verb) + " )"
  record( utc, devName, satName, baudrate, verb )

# Function for recording the actual packets
def record( utc, devName, satName, baudrate, verb ):
  soundmodem = serial.Serial(devName, baudrate)

  while True:
    hexval = soundmodem.read()
    if hexval.encode("hex") == "c0":
      # Verbose
      if verb:
	print "Start Packet Rx\n" + time.strftime("%H%M%S")
      data = hexval
      hexval = soundmodem.read()
      while hexval.encode("hex") != "c0":
        data += hexval
        hexval = soundmodem.read()
      data += hexval
      # Verbose
      if verb:
	print "End Packet Rx\n" + time.strftime("%H%M%S")
      hexval = None
      if not utc:
	if not satName:
	  filename = time.strftime("%Y%m%d-%H%M%S%Z") + ".log"
	else:
	  filename = satName + "-" + time.strftime("%Y%m%d-%H%M%S%Z") + ".log"
      else:
	if not satName:
	  filename = time.strftime("%Y%m%d-%H%M%SUTC", gmtime()) + ".log"
	else:
	  filename = satName + "-" + time.strftime("%Y%m%d-%H%M%SUTC", gmtime()) + ".log"
#      if os.path.isfile(filename):
#	print "Error: file " + filename + " exists.\nExiting to avoid overwrite"
#	sys.exit(4)
      file = open(filename, 'a')
      file.write(data)
      file.close()
      data = None

def help():
  print "\nUsage: " + sys.argv[0] + " [OPTION] ..."
  print "Log packets demodulated by a TNC and save them by timestamp\n"
  print "Arguments:\n"
  print "  -h, --help\t\tdisplay this help and exit"
  print "  -u, --utc\t\tuse UTC when logging, default is localtime"
  print "  -d, --device\t\tspecify the port to recieve on"
  print "  -s, --satellite\tspecify the name of the satellite for logging"
  print "  -b, --baudrate\tspecify the baudrate the TNC writes at"
  print "  -v\t\t\tverbose output"
  print "\nCreated by Kyle Colton\nComments, tips, edits, etc. are welcome\nVersion 1.0\n"

if __name__ == "__main__":
  main(sys.argv[1:])
