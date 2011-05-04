#!/bin/ksh
#
#                     run_mean.ksh 
#
# ------------------------------------------------------------------------
#              
#           Camilla Andersson, Aug 2009, smhi
#
#           
#
#          Runs metgraf to plot the results from the mask-files
#          To check for immediate errors that may have occurred
#          Compare to other runs to see if parameters seem ok
#          check O3, NO2, NOx, SO2, SULFATE, NITRATE, NH42SO4, NH4NO3, ...?
#
#
# -------------------------------------------------------------------------

#setenv TABLE_PATH /data/proj/MATCH/bin/dbase/.

# Variables
# -------------------------------------------------------------------------

EXE=/data/proj/MATCH/bin/Linux/met2ps


#Only the year is of importance, all months will be plotted
YYYY=2008
PAR_LIST="NOxNtra NOxNfix NOxNsea NOxNres"
masks="MA1 MA2 MA3 MA4 MA5 MA6 MA7 MA8 MA9 MA10"
masks=""

#  -------------------------------------------------------------------------

# Plot met2ps
# -------------------------------------------------------------------------

for PAR in ${PAR_LIST}
do
echo $PAR


IY=$YYYY
IM=1
ID=1
IH=0
EY=$YYYY
EM=1
ED=1
EH=0

mkdir -p results
OUTFILE=results/${PAR}_$YYYY$MM$DD$HH.png
echo utfil = $OUTFILE
export YYYY PAR
$EXE -D $IY $IM $ID $IH -d $EY $EM $ED $EH -dI 1 -i mall -o $OUTFILE -nv
cp error.log error.log.$PAR


for mask in $masks;do

OUTFILE=results/${PAR}_${mask}_$YYYY$MM$DD$HH.png
echo utfil = $OUTFILE
export mask
$EXE -D $IY $IM $ID $IH -d $EY $EM $ED $EH -dI 1 -i mask_mall -o $OUTFILE -nv
cp error.log error.log.$PAR$mask

done 

done
