#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# Ett skript för att konvertera lokala edb:er från RT90 till SWEREF99 
# Skriptet är skrivet av Martin Torstensson 2011-04
# Det är väldigt inspirerat (plagierat) av ett av David Segerssons skript
# för konvertering av ascii-grid-filer.

import os, numpy, math, subprocess, sys

proj4Dict={
    'EMEP50km':"+proj=stere +lat_0=90 +lat_ts=60 +lon_0=-32 +k=1 +x_0=8 +y_0=110 +a=127.4",
    'RT9025gonV':"+proj=tmerc +lat_0=0 +lon_0=15d48\\'29.8\\\" +x_0=1500000 +k_0=1 +ellps=bessel +towgs84=414.1,41.3,603.1,-0.855,2.141,-7.023,0",
    'WGS84':"+proj=longlat +datum=WGS84",
    'rotLat-30Lon-10':"+proj=ob_tran +o_proj=eqc +o_lat_p=30 +lon_0=-10.0 +a=57.29577953604224884 +b=57.29577953604224884",
    'SWEREF99TM':"+proj=utm +zone=33 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
    }

def transform(x,y,fromProj, toProj):
    """Converts coordinates from fromProj to toProj
    @param x: X-coordinates (east-west), can be a list or an array
    @param y: Y-coordinates (north-south), can be a list or an array
    @param fromProj: Dictionary defining the original projection in the format of arguments to the proj.4 application cs2cs
    @param toProj: Dictionary defining the target projection in the format of arguments to the proj.4 application cs2cs
    """
        
    coordStr=""
    try:
        #First expecting x and y to be sequences, und thus interable (i.e. lists, arrays...)
        iter(x)
        iter(y)
    except TypeError:
        x=[x]
        y=[y]

    #map(str,x)
    #map(str,y)

    coords=zip(x,y)
    coordString='\n'.join(['%s %s' % point for point in coords])

    #if tmpDir is None:
        #inTmpFile=tempfile.NamedTemporaryFile('w',suffix=".tmp")
    #else:
        #inTmpFile=tempfile.NamedTemporaryFile('w',suffix=".tmp",dir=tmpDir)

    #open(inTmpFile.name,'w').write(coordString).close()
    #outTmpFile=tempfile.NamedTemporaryFile('w',suffix=".tmp",dir=tmpDir)
    #cmd="""cs2cs -f "%.7f" """+fromProj+" +to "+toProj+" "+inTmpFile.name+" > "+outTmpFile.name
    cmd="""cs2cs -f "%.7f" """+fromProj+" +to "+toProj+" <<EOF \n"+coordString + 'EOF'
    cs2cs = subprocess.Popen(cmd,stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    returnCode=cs2cs.wait()
    errMsg=cs2cs.stderr.read()
    #outMsg=open(outTmpFile.name,'r').read()
    outMsg=cs2cs.stdout.read()
        
    if returnCode!=0:
        raise IOError, "Command cs2cs did not finish correctly:\n"+errMsg    
    result=numpy.fromstring(outMsg,dtype=float,sep="\t",count=len(x)*3)
    result=numpy.reshape(result,(len(x),3))

    if result.ndim==1:        
        resX=numpy.array(result[0])
        resY=numpy.array(result[1])
    elif result.ndim>1:
        resX=numpy.array(result[:,0])
        resY=numpy.array(result[:,1])
    else:
        raise IOError, "Command cs2cs did not finish correctly"

    return resX, resY

def main():
    infile=sys.argv[1]
    if len(sys.argv) > 2:
	outfile=sys.argv[2]
    else:
	outfile=infile+'_SWEREF'
    rf=open(infile,'r')
    wf=open(outfile,'w')
    rt_x=[]
    rt_y=[]
    text=''
    for line in rf:
        if 'NAME ' in line.upper():
            # NAME "389191 389219"
            try:
                name=line.split('"')[1]
            except:
                print line
            # Fixa start_id och stop_id
        elif 'INFO ' in line.upper():
            try:
                info=line.split('"')[1]
            except:
                print line
        elif 'X' in line and 'Y' in line:
            # X0  1722624 Y0  7126640
            rt_x.append(int(line.split()[1]))
            rt_y.append(int(line.split()[3]))
        elif len(line.split())==0:
            wf.write('NAME "'+name+'"\n')
            wf.write('INFO "'+info+'"\n'+text)
            swe_x,swe_y = transform(rt_x,rt_y,fromProj=proj4Dict['RT9025gonV'],toProj=proj4Dict['SWEREF99TM'])
            for i in range(len(swe_x)):
                wf.write('X'+str(i)+'  '+str(int(round(swe_x[i],0)))+' Y'+str(i)+'  '+str(int(round(swe_y[i],0)))+'\n')
            wf.write('\n')
            rt_x=[]
            rt_y=[]
            text=''
        else:
            text+=line
    rf.close()
    wf.close()




if __name__=="__main__":
    main()


