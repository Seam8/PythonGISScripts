import sys, os
from cx_Freeze import setup, Executable


os.environ['TCL_LIBRARY'] = 'C:/ProgramData/Anaconda3/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = 'C:/ProgramData/Anaconda3/tcl/tk8.6'

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = dict(
	packages = ["os","osr","ogr","sys","tkinter"], 
	include_files=['C:/ProgramData/Anaconda3/DLLs/tcl86t.dll', 'C:/ProgramData/Anaconda3/DLLs/tk86t.dll'])

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "PointFromShapeGraphic",
        version = "0.2",
        description = "Graphical version",
        options = {"build_exe": build_exe_options},
        executables = [Executable("PointFromShapeGraphic.py", base=base)])