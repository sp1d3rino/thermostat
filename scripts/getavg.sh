#!/bin/bash
count=0; total=0; for i in $( awk '{ print $4; }' temp-history );\
do total=$(echo $total+$i | bc ); \
((count++)); done; echo "scale=2; $total / $count" | bc
