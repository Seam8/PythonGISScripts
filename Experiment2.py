# script to count features
# import modules
import ogr, osr, os, sys

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

# ________________________________________________
# ________________________________________________

# set the working directory
os.chdir('D:/testPythonScritp/Data')

# get the driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# open the input Polygon data source
ContourFile = 'DensityShape37041970Biw250_10.shp'
ContourDS = driver.Open(ContourFile, 0)
if ContourDS is None:
	print('Could not open file')
	sys.exit(1)

# get the input Polygon data layer
ContourPolyLayer = ContourDS.GetLayer()
PolyRef = ContourPolyLayer.GetSpatialRef()

# record fieldnames of input Surveys data layer
LayerDefn = ContourPolyLayer.GetLayerDefn()
schema = []
for n in range(LayerDefn.GetFieldCount()):
	Fielddefn = LayerDefn.GetFieldDefn(n)
	schema.append(Fielddefn.name)
# ________________________________________________
# ________________________________________________

# get the target spatial reference
targetRef = osr.SpatialReference()
targetRef.ImportFromEPSG(4326)

# get the transformation between layer
coordTrans = osr.CoordinateTransformation(PolyRef, targetRef)

# ________________________________________________
# ________________________________________________

# create new datasource for contained surveys records
outDS = driver.CreateDataSource('ConvertShape.shp')
if outDS is None:
	print('Could not create file')
	sys.exit(1)
outLayer = outDS.CreateLayer('InnerMeasures', srs=targetRef, geom_type=geom_type(ContourFile))

# use the first input FieldDefn to add fields to the output
inFeature = ContourPolyLayer.GetNextFeature()
if inFeature is None:
	print("No Feature are Found inside the filtering area ! ")
fieldDefn = [inFeature.GetFieldDefnRef(Fnames) for Fnames in schema]
for f in fieldDefn:
	outLayer.CreateField(f)

# get the FeatureDefn for the output layer
featureDefn = outLayer.GetLayerDefn()

while inFeature:

	# create a new feature
	outFeature = ogr.Feature(featureDefn)
	geom = inFeature.GetGeometryRef()
	geom.Transform(coordTrans)
	outFeature.SetGeometry(geom)
	for Fnames in schema:
		outFeature.SetField(Fnames, inFeature.GetField(Fnames))

	# add the feature to the output layer
	outLayer.CreateFeature(outFeature)

	# destroy the features
	inFeature.Destroy()
	outFeature.Destroy()

	# update Feature for next loop
	inFeature = ContourPolyLayer.GetNextFeature()

# close the data sources
ContourDS.Destroy()
