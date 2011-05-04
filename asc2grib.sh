#!/bin/bash

# Detta körskript läser in ascii filer och skriver ut grib-filer. 
# Det ändrar också enheten från g/år till Gg/år och ändrar från
# att mäta molekylmassa till ämnesmassa.
# Se även asc2grib.F i MATCH-koden för koden till asc2grib.x
#
# Skrivet av Martin Torstensson 2011-02-18

YYYY=2008
gribslut=' 01 01 00'
IN_PATH=.
OUT_PATH=./grib
unit=gperyear
power=e-9
maskunit=Ggperyear
maskpower=
SPECIES_LIST="NOx" # SOx NH3"
species=NOx
MASK=2
ROOT=ascii/
maskroot=/data/proj/Luftkvalitet/emissioner/verktyg/miljo2008/tmp/output/
EXE=/path/to/asc2grib.x

for species in $SPECIES_LIST
do
    if [ $species = NOx ]; then
	#Do stuff
	FAKTOR=0.30435
	SOURCELIST="navigation residential traffic rest"
	for SOURCE in $SOURCELIST
	do
	    if [ $SOURCE = navigation ]; then
		outsource=sea
	    elif [ $SOURCE = rest ]; then
		outsource=fix
	    else
		outsource=${SOURCE:0:3}
	    fi
	    echo $ROOT${SOURCE}_${unit}_${species}_${YYYY}.asc>asc2grib.inf
	    echo $YYYY$gribslut>>asc2grib.inf
	    echo $FAKTOR$power>>asc2grib.inf
	    echo ${OUT_PATH}/SWE_${species}${species:0:1}${outsource}>>asc2grib.inf
	    #     echo ${species}_${SOURCE}.asc>>asc2grib.inf
	    echo \>\>\> Now running $species from $SOURCE \<\<\<
	    $EXE
	    for MASK in {1..17}
	    do
		echo $maskroot${SOURCE}${species}${maskunit}${YYYY}_${MASK}.asc>asc2grib.inf
		echo $YYYY$gribslut>>asc2grib.inf
		echo $FAKTOR$maskpower>>asc2grib.inf
		echo ${OUT_PATH}/SWEMA${MASK}_${species}${species:0:1}${outsource}>>asc2grib.inf
		#         echo ${species}_${SOURCE}.asc>>asc2grib.inf
		echo \>\>\> Now running mask $MASK for $species from $SOURCE \<\<\<
		$EXE
	    done
	done
    else
	if [ $species = NH3 ];then 
	    SOURCELIST="agriculture navigation residential traffic rest"
	    FAKTOR=0.82353
	fi
	if [ $species = SOx ]; then
	    SOURCELIST="aviationCruise navigation residential traffic rest"
	    FAKTOR=0.5
	fi
	for SOURCE in $SOURCELIST
	do
	    if [ $SOURCE = navigation ]; then
		outsource=sea
	    elif [ $SOURCE = rest ]; then
		outsource=fix
	    else
		outsource=${SOURCE:0:3}
	    fi
	    echo $ROOT${SOURCE}_${unit}_${species}_${YYYY}.asc>asc2grib.inf
	    echo $YYYY$gribslut>>asc2grib.inf
	    echo $FAKTOR$power>>asc2grib.inf
	    echo ${OUT_PATH}/SWE_${species}${species:0:1}${outsource}>>asc2grib.inf
	    #       echo ${species}_${SOURCE}.asc>>asc2grib.inf
	    echo \>\>\> Now running $species from $SOURCE \<\<\<
	    ./asc2grib.x
	done
    fi
done
