#!/usr/bin/python
# This file is part of BackupBox.
#
# Copyleft 2017-20whatever Simone Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 3 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import argparse
import os
import time

parser = argparse.ArgumentParser(description='BackupBox - My job is backupping stuff and keep backups in sync.')

parser.add_argument( '-s','--source', help='Source mount point.',required=True)
parser.add_argument( '-d','--destination', help='Destination mount point', required=True)
parser.add_argument( '-c','--command', help='Command to execute when both mount points are detected.',
                     default="rsync -va --delete {SOURCE} {DESTINATION} > {DESTINATION}/backup_{TIMESTAMP}.log")
args = parser.parse_args()
 
source = os.path.abspath( args.source )
destination = os.path.abspath( args.destination )
template = args.command

were_plugged = False
are_plugged = False

print "BackupBox is running, press CTRL-C or just kill me biatch!\n"

while True:
    are_plugged = ( os.access( source, os.R_OK ) and os.access( destination, os.W_OK ) )
    
    if are_plugged and not were_plugged:
        cmd = template.replace("{SOURCE}", source)
        cmd = cmd.replace("{DESTINATION}", destination)
        cmd = cmd.replace("{TIMESTAMP}", str(int(time.time())))

        print "Both medias detected, executing command:"
        print "  %s\n" % cmd
        os.system(cmd)
        print "\nDone, sync ..."
        os.system("sync")
        print "You can unmount and unplug the device now."

    were_plugged = are_plugged
    time.sleep(1)

    
