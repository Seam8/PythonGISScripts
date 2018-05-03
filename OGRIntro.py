# script to count features
# import modules
import ogr, os, sys

# set the working directory
os.chdir('D:/testPythonScritp/Data')

# get the driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# open the data source
datasource = driver.Open('test.shp', 0)
if datasource is None:
	print('Could not open file')
	sys.exit(1)

# get the data layer
layer = datasource.GetLayer()

# loop through the features and count them
cnt = 0
feature = layer.GetNextFeature()
while feature:
	cnt = cnt + 1
	feature.Destroy()
	feature = layer.GetNextFeature()
print( str(cnt) + ' features are counted')
print( str(layer.GetFeatureCount()) + ' features are recorded')
print( str(datasource.GetLayerCount()) + ' Layer are contained in the datasource')

# close the data source
datasource.Destroy()