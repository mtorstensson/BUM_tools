#!/usr/bin/python
# Ett skript för att översätta punktkällorna från RT90 till SWEREF99
# Det kräver att proj4 är installerat, mer exakt att cs2cs, som är ett 
# verktyg som hör till proj4 är installerat.
# Skriptet är skrivet av Martin Torstensson 2011-04

import subprocess

sp='   '
rf = open("punktkallor.csv")
noxf = open("nox.txt",'w')
cof = open("co.txt",'w')
pm10f = open("pm10.txt",'w')
benzenef = open("benzene.txt",'w')
factor={r'Gg/year':365*24*3600*float(10**-9),r'':0}
nmvocFactor=0.0344827586207

for line in rf.readlines():
    try:
	[x,y,cHgt,gT,gf,cD,hHgt,nox,uNOX,co,uCO,pm10,uPM,nmvoc,uNMVOC]=line.split('\t')
    except:
	print line
    # Raden som styr vilken översättning som görs. I nuläget är det RT90->SWEREF99
    cmd="""cs2cs -f "%.7f" +proj=tmerc +lat_0=0 +lon_0=15d48\\'29.8\\\" +x_0=1500000 +k_0=1 +ellps=bessel +towgs84=414.1,41.3,603.1,-0.855,2.141,-7.023,0 +to +proj=utm +zone=33 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs  <<EOF \n"""+x+' '+y + 'EOF'
    cs2cs = subprocess.Popen(cmd,stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    breakCode=cs2cs.wait()
    errMsg=cs2cs.stderr.read()
    outMsg=cs2cs.stdout.read()
    if breakCode!=0:
        raise IOError, "Command cs2cs did not finish correctly:\n"+errMsg
    [x,y]=outMsg.split()[:2]
    lineStart = sp+x+sp+y+sp
    lineEnd = sp+cHgt+sp+cD+sp+gf+sp+gT+sp+hHgt+'    5    0\n'
    if uNOX not in factor:
	print uNOX +" not known\n"
	print 'NOX'
	print factor
	break
    if uNOX!='':
	nox = str(float(nox)*factor[uNOX])
	if nox != '0.0':
	    noxf.write(lineStart+nox+lineEnd)
    if uCO not in factor:
	print uCO +" not known\n"
	print 'CO'
	break
    if uCO != '':
	co=str(float(co)*factor[uCO])
	if co != '0.0':
	    cof.write(lineStart+co+lineEnd)
    if uPM not in factor:
	print uPM +" not known\n"
	print 'PM10'
	break
    if uPM != '':
	pm10=str(float(pm10)*factor[uPM])
	if pm10 != '0.0':
	    pm10f.write(lineStart+pm10+lineEnd)
    if uNMVOC[-1:] == '\n':
	uNMVOC=uNMVOC[:-1]
    if uNMVOC not in factor:
	print uNMVOC +" not known\n"
	print 'NMVOC'
	break
    if uNMVOC != '':
	nmvoc=str(float(nmvoc)*factor[uNMVOC]*nmvocFactor)
	if nmvoc != '0.0':
	    benzenef.write(lineStart+nmvoc+lineEnd)

rf.close() 
noxf.close() 
cof.close() 
pm10f.close() 
benzenef.close() 
