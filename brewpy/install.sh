#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
sed -i -e '$i \# Start brewpy\n'$DIR'/start\n' /etc/rc.local
