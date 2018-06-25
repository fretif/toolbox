#!/bin/bash

# Convert to the ww3_shel format. We remove the duplicated point (the four corner)       
awk -F'|' 'BEGIN { i = 0 ; skip=0 }
     $0~/>/ {skip=1; next;}	
     { if(skip==1) { skip=0 ; next } 
       gsub(/[ \t]+$/, "", $4); gsub(/[ \t]+$/, "", $5); printf("    %s  %s \x27Point%s\x27      \n",$4,$5,i);
       i=i+1 	  
     }' $1 > insert-ww3_shel.inp

