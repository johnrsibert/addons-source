#!/bin/bash

echo $#
echo $0
echo $1
SRC="./*"
DEST="/home/player1/GrampsTesting/addons-source/TimelineContingency/"
echo $SRC
echo $DEST

#\cp -uv ~/GrampsTesting/addons-source/TimelineContingency/
\cp -uv $SRC $DEST
if [ $# -ge 1 ]; then
   echo "----------"
   echo "-m "$1
   echo $1
   git -C $DEST commit --dry-run -av "-m "$1
fi
