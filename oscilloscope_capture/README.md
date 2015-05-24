# Oscilloscope Capture

This program is designed to capture events from a Tektronix DPO3000 oscilloscope over ethernet via a python-telnet script. This was in particular written to capture rise-time and amplitude on two channels of the scope, but it could easily be modified for almost any function of the DPO3000. The manual (see Notes) is good about describing the commands and interface.

Comments, suggestions, edits, and tips are welcome and appreciated.

### Quirks
* The scope requires `\r\n` (Windows style) for a command to be read.
* I added in waits between commands because the scope doesn't handle buffering well (or at all) as far as I can tell

### Notes
Tektronix manual
http://www.tequipment.net/assets/1/26/Documents/Tektronix/dpo3000_programmermanual.pdf

### Usage
```
Arguments:
-h, --help\t\tdisplay this help and exit
-i, --ip\t\tspecify the ip that the scope is at
-p, --port\t\tspecify the port the scope is listening on
-t, --timeout\t\tspecify the amount of time to wait for a reply
-f, --file\t\tspecify the file to write data to
-g, --images\t\tspecify the image name prefix, save under a folder by using foo/bar
-n, --samples\t\tspecify the number of samples to capture
-o, --offset\t\tallows the user to start at any sample number
-w, --warn\t\tis a planned function that allows the program to send info or warning emails
-c, --two_ch\t\ttwo channel capture
-v\t\t\tverbose output
```
## License

Copyright (C) 2015  Kyle Colton

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
