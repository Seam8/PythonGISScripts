# script to count features
# import modules
import ogr, osr, os, sys
import tkinter 
from tkinter.filedialog import askopenfile, asksaveasfile

def GoOnProcess():
    InputPolySc = InPathAr.get()
    InputSurveysSc = InPathPt.get()
    OutputSurveysSc = Outpath.get()
    form.quit()
    form.destroy()
    print("Point", InputSurveysSc)
    print("Area", InputPolySc)
    print("Out", type(OutputSurveysSc))


    # ________________________________________________
    # ________________________________________________

    # get the driver
    driver = ogr.GetDriverByName('ESRI Shapefile')

    # open the input Polygon data source
    ContourDS = driver.Open(InputPolySc, 0)
    if ContourDS is None:
        print('Could not open file')
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
        print('Could not open file')
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
    if os.path.exists(OutputSurveysSc):
        driver.DeleteDataSource(OutputSurveysSc)
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


def getInputPath(Title, FileTypes, Variable, Mode='r'):
    Variable.set(
        askopenfile(
            title=Title, 
            mode=Mode,
            filetypes=FileTypes).name
        )

def getOutputPath(Title, Extension, Variable):
    Variable.set(
        asksaveasfile(
            title=Title, 
            defaultextension=Extension).name
        )

if __name__ == '__main__':
    form = tkinter.Tk()
    form.wm_title('Points from Extent extractor')


    # Sections 
        # Sections fILE Details
    stepOne = tkinter.LabelFrame(form, text=" 1. Entrer les détails des fichiers: ")
    stepOne.grid(row=0, columnspan=7, sticky='WE' , \
                 padx=5, pady=5, ipadx=5, ipady=5)
        # Sections Validation
    stepTwo = tkinter.LabelFrame(form, text=" 2. Lancer le processus: ")
    stepTwo.grid(row=2, columnspan=7, sticky='WE' , \
                 padx=5, pady=5, ipadx=5, ipady=5)
        # Sections HELP
    helpLf = tkinter.LabelFrame(form, text=" Aide rapide")
    helpLf.grid(row=0, column=9, columnspan=2, rowspan=8, \
                sticky='NS', padx=5, pady=5)
    helpLbl = tkinter.Label(helpLf, text="Help will come - ask for it.")
    helpLbl.grid(row=0)


    # BUTTONS, LABELS, ENTRIES
        # fILE DETAIL SECTION
            # SELECT FILE
                # Surveys input
    InPathPt = tkinter.StringVar()
    SurveysTYPES = [("ESRI Shape", "*.shp"), ("Vector Virtual format", "*.vrt")]
    TextLabelPt = "Sélectionner la couche de points:"

    inFileLPt = tkinter.Label(stepOne, text=TextLabelPt)
    inFileLPt.grid(row=0, column=0, sticky='E', padx=5, pady=2)

    inFilePtTxt = tkinter.Entry(stepOne, textvariable=InPathPt)
    inFilePtTxt.grid(row=0, column=1, columnspan=7, sticky="WE", pady=3)

    inFilePtBtn = tkinter.Button(stepOne, text="Parcourir ...", command= lambda 
        T=TextLabelPt,
        F=SurveysTYPES,
        V=InPathPt: 
    getInputPath(Title=T, FileTypes=F, Variable=V))
    inFilePtBtn.grid(row=0, column=8, sticky='W', padx=5, pady=2)

                # Extent Input
    InPathAr = tkinter.StringVar()
    AreaTYPES = [("ESRI Shape", "*.shp")]
    TextLabelAr = "Sélectionner la couche de suface:"

    inFileLArbl = tkinter.Label(stepOne, text=TextLabelAr)
    inFileLArbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)

    inFileArTxt = tkinter.Entry(stepOne, textvariable=InPathAr)
    inFileArTxt.grid(row=1, column=1, columnspan=7, sticky="WE", pady=3)

    inFileArBtn = tkinter.Button(stepOne, text="Parcourir ...", command= lambda 
        T=TextLabelAr,
        F=AreaTYPES,
        V=InPathAr: 
    getInputPath(Title=T, FileTypes=F, Variable=V))
    inFileArBtn.grid(row=1, column=8, sticky='W', padx=5, pady=2)

            # Extracted Surveys Output
    Outpath = tkinter.StringVar()
    OutputExt = "shp"
    TextLabelOut = "Enregistrer sous:"

    outFileLbl = tkinter.Label(stepOne, text=TextLabelOut)
    outFileLbl.grid(row=2, column=0, sticky='E', padx=5, pady=2)

    outFileTxt = tkinter.Entry(stepOne, textvariable=Outpath)
    outFileTxt.grid(row=2, column=1, columnspan=7, sticky="WE", pady=2)

    outFileBtn = tkinter.Button(stepOne, text="Parcourir ...", command= lambda 
        T=TextLabelOut,
        E=OutputExt,
        V=Outpath: 
    getOutputPath(Title=T, Extension=E, Variable=V))
    outFileBtn.grid(row=2, column=8, sticky='W', padx=5, pady=2)



                    # Validation
    inFilePtBtn = tkinter.Button(stepTwo, text="Valider", command=GoOnProcess)
    inFilePtBtn.grid(row=3, column=8, sticky='ES', padx=5, pady=2)


    form.mainloop()