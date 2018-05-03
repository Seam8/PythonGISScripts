# script to count features
# import modules
import ogr, osr,  os, sys

# Define used function
def geom_type(shapefile_location):

	# get the driver
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(shapefile_location)
	if shapefile is None:
		print('Could not open file')
		sys.exit(1)

	layer = shapefile.GetLayer()
	feature = layer.GetNextFeature()
	geometry = feature.GetGeometryRef()
	
	return geometry.GetGeometryType()

# set the working directory
os.chdir('D:/testPythonScritp/Data')

# get the driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# open the input data source
inDS = driver.Open('ContourLIne10.shp', 0)
if inDS is None:
	print('Could not open file')
	sys.exit(1)

# get the input data layer
inLayer = inDS.GetLayer()

# create a new data source and layer
# erase previous data if exist
if os.path.exists('test.shp'):
	driver.DeleteDataSource('test.shp')

# create new datasource
outDS = driver.CreateDataSource('test.shp')
if outDS is None:
	print('Could not create file')
	sys.exit(1)

# create new Layer in the new datasource
spatialRef = inLayer.GetSpatialRef()
newRef = osr.SpatialReference()
newRef.ImportFromWkt(spatialRef.ExportToWkt())
if spatialRef is None:
	print('Could not find projection properties')
outLayer = outDS.CreateLayer('test', srs=newRef, geom_type=geom_type('ContourLIne10.shp'))

# use the input FieldDefn to add a field to the output
fieldDefn = inLayer.GetFeature(0).GetFieldDefnRef('id')
outLayer.CreateField(fieldDefn)

# get the FeatureDefn for the output layer
featureDefn = outLayer.GetLayerDefn()

# loop through the input features
cnt = 0
inFeature = inLayer.GetNextFeature()
while inFeature:

	# create a new feature
	outFeature = ogr.Feature(featureDefn)
	outFeature.SetGeometry(inFeature.GetGeometryRef())
	outFeature.SetField('id', inFeature.GetField('id'))

	# add the feature to the output layer
	outLayer.CreateFeature(outFeature)

	# destroy the features
	inFeature.Destroy()
	outFeature.Destroy()

	# increment cnt and if we have to do more then keep looping
	cnt = cnt + 1
	if cnt < 10000: 
		inFeature = inLayer.GetNextFeature()
	else: 
		break
# close the data sources
inDS.Destroy()
outDS.Destroy()