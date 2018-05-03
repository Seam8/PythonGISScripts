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

InputPolySc = 'D:/Image/Poe/ZonePoe.shp'
InputSurveysSc = 'Data/ShomSurveys.vrt'
OutputSurveysSc = 'Data/PoeInnerSurveystest2.shp' 

'''InputPolySc = str(sys.argv[1])
InputSurveysSc = str(sys.argv[2])
OutputSurveysSc = str(sys.argv[3])'''

# get the driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# open the input Polygon data source
ContourDS = driver.Open(InputPolySc, 0)
if ContourDS is None:
	print('Could not open Polygon file')
	sys.exit(1)

# get the input Polygon data layer
ContourPolyLayer = ContourDS.GetLayer()
PolyRef = ContourPolyLayer.GetSpatialRef()

# open the input Surveys data source
if InputSurveysSc[-3:]=="shp":
	SurveysDS = driver.Open(InputSurveysSc, 0)
elif InputSurveysSc[-3:]=="vrt":
	SurveysDS = ogr.Open(InputSurveysSc, 0)
else:
	print('Unknown Survey file format ! need .shp or .vrt')
	sys.exit(1)
if SurveysDS is None:
	print('Could not open Surveys file')
	sys.exit(1)

# ________________________________________________
# ________________________________________________

# get the input Surveys data layer
SurveysLayer = SurveysDS.GetLayer()
SurveysRef = SurveysLayer.GetSpatialRef()
LayerDefn = SurveysLayer.GetLayerDefn()
print('Number of Points: ',SurveysLayer.GetFeatureCount())

# record fieldnames of input Surveys data layer
schema = []
for n in range(LayerDefn.GetFieldCount()):
	Fielddefn = LayerDefn.GetFieldDefn(n)
	schema.append(Fielddefn.name)

# prepare filtering
SurveysLayer.ResetReading()

# get the area contained in the Polygon data layer
featArea = ContourPolyLayer.GetNextFeature()
poly = featArea.GetGeometryRef()

# Filter the input Surveys with the input area
SurveysLayer.SetSpatialFilter(poly)
print('Number of Points in the area: ',SurveysLayer.GetFeatureCount())

# ________________________________________________
# ________________________________________________

# create new datasource for contained surveys records
outDS = driver.CreateDataSource(OutputSurveysSc)
if outDS is None:
	print('Could not create file')
	sys.exit(1)

# create new Layer in the new datasource
newRef = osr.SpatialReference()
newRef.ImportFromWkt(PolyRef.ExportToWkt())
if PolyRef is None:
	print('Could not find projection properties')
outLayer = outDS.CreateLayer('InnerMeasures', srs=newRef, geom_type=1)

# use the first input FieldDefn to add fields to the output
inFeature = SurveysLayer.GetNextFeature()
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
	outFeature.SetGeometry(inFeature.GetGeometryRef())
	for Fnames in schema:
		outFeature.SetField(Fnames, inFeature.GetField(Fnames))

	# add the feature to the output layer
	outLayer.CreateFeature(outFeature)

	# destroy the features
	inFeature.Destroy()
	outFeature.Destroy()

	# update Feature for next loop
	inFeature = SurveysLayer.GetNextFeature()

# close the data sources
outDS.Destroy()
ContourDS.Destroy()
SurveysDS.Destroy()