import tkinter as Tkinter

if __name__ == '__main__':
    form = Tkinter.Tk()

    getFld = Tkinter.IntVar()

    form.wm_title('File Parser')


    # Sections 
    	# Sections fILE Details
    stepOne = Tkinter.LabelFrame(form, text=" 1. Enter File Details: ")
    stepOne.grid(row=0, columnspan=7, sticky='WE' , \
                 padx=5, pady=5, ipadx=5, ipady=5)
    	# Sections TABLE Details
    stepTwo = Tkinter.LabelFrame(form, text=" 2. Enter Table Details: ")
    stepTwo.grid(row=2, columnspan=7, sticky='WE' , \
                 padx=5, pady=5, ipadx=5, ipady=5)
    	# Sections SET UP
    stepThree = Tkinter.LabelFrame(form, text=" 3. Configure: ")
    stepThree.grid(row=3, columnspan=7, sticky='WE' , \
                   padx=5, pady=5, ipadx=5, ipady=5)
    	# Sections HELP
    helpLf = Tkinter.LabelFrame(form, text=" Quick Help ")
    helpLf.grid(row=0, column=9, columnspan=2, rowspan=8, \
                sticky='NS', padx=5, pady=5)
    helpLbl = Tkinter.Label(helpLf, text="Help will come - ask for it.")
    helpLbl.grid(row=0)


    # BUTTONS, LABELS, ENTRIES
    	# fILE DETAIL SECTION
	    	# SELECT FILE
    inFileLbl = Tkinter.Label(stepOne, text="Select the File:")
    inFileLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

    inFileTxt = Tkinter.Entry(stepOne)
    inFileTxt.grid(row=0, column=1, columnspan=7, sticky="WE", pady=3)

    inFileBtn = Tkinter.Button(stepOne, text="Browse ...")
    inFileBtn.grid(row=0, column=8, sticky='W', padx=5, pady=2)
	    	# SELECT OUTPUTS
    outFileLbl = Tkinter.Label(stepOne, text="Save File to:")
    outFileLbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)

    outFileTxt = Tkinter.Entry(stepOne)
    outFileTxt.grid(row=1, column=1, columnspan=7, sticky="WE", pady=2)

    outFileBtn = Tkinter.Button(stepOne, text="Browse ...")
    outFileBtn.grid(row=1, column=8, sticky='W', padx=5, pady=2)
	    	# Sections ENCODING INPUT
    inEncLbl = Tkinter.Label(stepOne, text="Input File Encoding:")
    inEncLbl.grid(row=2, column=0, sticky='E', padx=5, pady=2)

    inEncTxt = Tkinter.Entry(stepOne)
    inEncTxt.grid(row=2, column=1, sticky='E', pady=2)
	    	# Sections ENCODING OUTPUT
    outEncLbl = Tkinter.Label(stepOne, text="Output File Encoding:")
    outEncLbl.grid(row=2, column=5, padx=5, pady=2)

    outEncTxt = Tkinter.Entry(stepOne)
    outEncTxt.grid(row=2, column=7, pady=2)

    	# TABLE DETAIL SECTION;;;
    outTblLbl = Tkinter.Label(stepTwo, \
          text="Enter the name of the table to be used in the statements:")
    outTblLbl.grid(row=3, column=0, sticky='W', padx=5, pady=2)

    outTblTxt = Tkinter.Entry(stepTwo)
    outTblTxt.grid(row=3, column=1, columnspan=3, pady=2, sticky='WE')

    fldLbl = Tkinter.Label(stepTwo, \
                           text="Enter the field (column) names of the table:")
    fldLbl.grid(row=4, column=0, padx=5, pady=2, sticky='W')

    getFldChk = Tkinter.Checkbutton(stepTwo, \
                           text="Get fields automatically from input file",\
                           onvalue=1, offvalue=0)
    getFldChk.grid(row=4, column=1, columnspan=3, pady=2, sticky='WE')

    fldRowTxt = Tkinter.Entry(stepTwo)
    fldRowTxt.grid(row=5, columnspan=5, padx=5, pady=2, sticky='WE')

    	# SET UP DETAIL SECTION;;;
    transChk = Tkinter.Checkbutton(stepThree, \
               text="Enable Transaction", onvalue=1, offvalue=0)
    transChk.grid(row=6, sticky='W', padx=5, pady=2)

    transRwLbl = Tkinter.Label(stepThree, \
                 text=" => Specify number of rows per transaction:")
    transRwLbl.grid(row=6, column=2, columnspan=2, \
                    sticky='W', padx=5, pady=2)

    transRwTxt = Tkinter.Entry(stepThree)
    transRwTxt.grid(row=6, column=4, sticky='WE')

    form.mainloop()