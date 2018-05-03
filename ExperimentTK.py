import tkinter
import tkinter.filedialog

window = tkinter.Tk()
window.withdraw()
SurveysTYPES = [("ESRI Shape", "*.shp"), ("Vector Virtual format", "*.vrt")]


path1 = tkinter.filedialog.askopenfile(title="Extent Layer", mode='r', filetypes=SurveysTYPES).name
path2 = tkinter.filedialog.askopenfile(title="Surveys Layer", mode='r', filetypes=SurveysTYPES).name
path3 = tkinter.filedialog.asksaveasfilename(title='Recorded Surveys',defaultextension = 'shp')
window.mainloop()


print(type(path1)) # <- Not actually in the code, but I've included it to show the type
print(path3) 