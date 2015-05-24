#!/bin/bash

# DESCRIPTION
# Gpredict only allows fetching TLEs from one web server. This script
# is designed to consolidate TLEs from multiple sources into a single
# file. I have this in a cron on my computer so fresh TLEs are always
# in a destination file for me to grab. I hope to update this into
# Python at some point, but for now it remains a Bash script.
#
# This script is for use with Gpredict's 'Update TLEs from File'
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


# Destination File
DEST_DIR="/tmp/new.tle"

# Sources to Fetch From
# URLs go in URL
# Individual text files at each URL go in FILES#
URL=(	http://www.celestrak.com/NORAD/elements/
	http://mstl.atl.calpoly.edu/~ops/gemsat_tle/
	http://lasp.colorado.edu/csswe/plots/daily/
	)
FILES0=(amateur.txt
	cubesat.txt
	dmc.txt
	education.txt
	engineering.txt
	galileo.txt
	geo.txt
	geodetic.txt
	globalstar.txt
	glo-ops.txt
	goes.txt
	gorizont.txt
	gps-ops.txt
	intelsat.txt
	iridium.txt
	military.txt
	molniya.txt
	musson.txt
	nnss.txt
	noaa.txt
	orbcomm.txt
	other.txt
	other-comm.txt
	radar.txt
	raduga.txt
	resource.txt
	sarsat.txt
	sbas.txt
	science.txt
	tdrss.txt
	tle-new.txt
	visual.txt
	weather.txt
	x-comm.txt
	)
FILES1=(39463-FIREBIRD-A.txt
	39464-FIREBIRD-B.txt
	39469-MCUBED-2.txt
	)
FILES2=(Text_TLE.txt
	)

# Make sure the destination exists and is empty
[ -f $DEST_DIR ] && mv $DEST_DIR "$DEST_DIR.old"
touch $DEST_DIR

# For each URL, go through the applicable FILES array and wget from each file at the URL
num_urls=${#URL[@]}
i=0
while [ $i -lt $num_urls ]
do
	eval var=( \"\${FILES${i}[@]}\" )
	for tle in "${var[@]}"
	do
		# -O - outputs to standard output, then appends to $DEST_DIR
		wget "${URL[$i]}$tle" -nv -O - >> $DEST_DIR
	done
	i=$[$i+1]
done

exit 0
