#!/bin/bash
# Ett skript f�r att generera fysiografi-filer f�r maskorna till BUM-k�rningen
# Det kr�ver tillg�ng till grundfysiografifilerna HOMEsei_sum_fysio_newgrib_0001000000+000H00M och 
# HOMEsei_win_fysio_newgrib_0001000000+000H00M. Dessa skall ligga i $fysorg
# mask.F finns i matchkoden.
# Skriptet �r skrivet av Martin Torstensson 2011-04

yyyy=2008
fysorg=/data/proj/Luftkvalitet/emissioner/verktyg/miljo2008/verktyg/fysorg/
EXE=/path/to/mask.x

mkdir -p fys
for mask in 1..17; do
  for season in win sum; do
    cp $fysorg/HOMEsei_${season}_fysio_newgrib_0001000000+000H00M fys/HOME-mask${mask}_${season}_${yyyy:2:2}01010000+000H00M
    echo ../../../Masker_SWEREF99/Mask${mask}/mask${mask}.txt>mask.inf
    echo ${yyyy}>>mask.inf
    echo "./fys/HOME-mask${mask}_${season}">>mask.inf
    $EXE
  done
done
