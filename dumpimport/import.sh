#!/bin/bash

##########
# Imports data downloaded with the dwnld.sh by iterating over
# directories with different entity types, unpacking gzip files
# and running the import.py script on them.
#
# - An optional first parameter indicates the data location.
# - All other parameters are passed to the import.py script.
# - An optional IMPORTSCRIPT environment variable indicates the location
#   of the import.py. If it's not present, it's assumed it exists
#   in the working directory.
##########

IMPORTSCRIPT=${IMPORTSCRIPT:="`pwd`/import.py"}
LOCATION=$1
LOCATION=${LOCATION:=.}
cd "$LOCATION"
for TYPE in `find . -maxdepth 1 -type d | grep -v "\.$" | sort` ; do
  TYPE=${TYPE:2}
  echo "### $TYPE"
  for j in `ls -1 $TYPE/*gz` ; do
    FILE=${j:0:-3}
    gunzip -c "$j" > "$FILE"
    python3 $IMPORTSCRIPT $TYPE "$FILE" "${@:2}" 2>&1 | tee -a "import_$TYPE.log"
    rm -f "$FILE"
  done
done
