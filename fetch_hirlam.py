#!/usr/bin/env python
# Ett skript f�r att h�mta det som beh�vs fr�n hirlam f�r att kunna k�ra BUM
# p� gimle utan att flytta ~1T data. Det kr�ver en pythonpath som inkluderar FOU:s 
# pygrib och pydate. Det f�ruts�tter ocks� att kataloger p� formen YYYYMM redan finns.
# Skriptet �r skrivet av Martin Torstensson 2011-04

import pygrib as pg

start=pg.setdate("2009010100")
end=pg.setdate("2010010100")

out="/E11"

slp=['PS','TS','SNOW','ALBEDO','ISPA_ICE','LANDMASK','Z0']
mlp=['U','V','T','QML']
lev=[60,59,58,57,56,55]

while start<end:
    for ll in 0,3,6:
        d=start%ll
        print d.format()
        prefix="/data/arkiv/field/f_archive/hirlam/E11_60lev/%s/E11" % (start.format("%Y%m"))
        g = pg.open(prefix,date=d)
        h = pg.open(start.format("%Y%m")+out,"w",date=d)
        for p in slp:
            h.put(g.get(p))
        for p in mlp:
            h.put(g.get(p,lev))
        h.close()
        g.close()
    start=start+6

