#!/bin/bash

for k in $( seq 5 100)
do
  c=$k
  echo $c
  python Word2Veckmeansclustering.py $c
  if [ $(echo "$? < 0.5" | bc) == 1 ] 
  then
  echo 'right'
  break
  else
  echo 'wrong'
  fi
done
