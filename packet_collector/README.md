# Packet Collector

This program is designed to listen to a port and log all data collected between two instances of a 0xC0 hex duple (KISS TNC FEND). It was specifically designed to monitor a soundmodem output stream. As data is collected, it is written to a directory with the specified parameters as "satelliteName-time-zone.log".

Comments, suggestions, edits, and tips are welcome and appreciated.

### Usage
```
-h, --help      display this help and exit
-u, --utc       use UTC when logging, default is localtime
-d, --device    specify the port to recieve on
-s, --satellite specify the name of the satellite for logging
-b, --baudrate  specify the baudrate the TNC writes at
-v              verbose output
```

## License

Copyright (C) 2015  Kyle Colton

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
