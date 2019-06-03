#!/bin/bash

pbsID=$(qsub jobneo.pbs)
echo "NEO_begins"
#echo $pbsID
echo "The job $pbsID is submitted..."
tt=$(qstat | grep "$pbsID")
sleep 1
while [ ${#tt} -gt 0 ] ; do
  echo "The job $pbsID is still running..."
  sleep 7
  tt=$(qstat | grep "$pbsID")
done

#echo "The job $pbsID is completed!"
echo "NEO completed!!"
