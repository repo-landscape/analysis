#!/bin/bash
IMPORTSCRIPT=/home/openaire/analysis/dumpimport/import.py
for TYPE in `find . -maxdepth 1 -type d | grep -v "\.$" | grep -v publication | sort` ; do
  TYPE=${TYPE:2}
  echo "### $TYPE"
  for j in `ls -1 $TYPE/*gz` ; do
    FILE=${j:0:-3}
    gunzip -c "$j" > "$FILE"
    python3 $IMPORTSCRIPT $TYPE "$FILE" "$@" | tee -a "import_$TYPE.log"
    rm -f "$FILE"
  done
done
