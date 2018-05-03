
import ogr, osr, os, sys

# set the working directory
os.chdir('D:/testPythonScritp/Data')
ogr.UseExceptions()

inDataSource = ogr.Open("ShomSurveys.vrt")
lyr = inDataSource.GetLayer('ShomSurveys')
count = 0
for feat in lyr:
    geom = feat.GetGeometryRef()
    X = geom.GetX()
    print( geom.ExportToWkt())
    print( type(X))
    print( X)
    print('Date: '+ str(feat.GetField('Date')))
    print(type(feat.GetField('Date')))
    print('Depth: '+ str(feat.GetField('Depth')))
    count = count +1
    if count > 10:
    	break

LayerDefn = lyr.GetLayerDefn()

