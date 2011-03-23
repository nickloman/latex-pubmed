#!/usr/bin/python
"""
Retrieve PubMed reference from its PMID given as last argument
Copyright (C) 2006-2007 Jean-Etienne Poirrier

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

WARNING: no check for duplicate references (just add the ref)
TODO: all exception handling
INFOS: http://www.poirrier.be/~jean-etienne/software/pyp2b/
E-MAIL: jepoirrier@gmail.com
"""

from pyP2Bclass import pyP2B
from ScrolledText import *
from Tkinter import *

class App:

    def __init__(self, master):

        def saisie():
            myref = pyP2B()
            resultBox.insert('end', myref.getPubmedReference(valeur.get()))

        valeur = StringVar()
        
        frame = Frame(master)
        frame.pack()

        queryFrame = Frame(frame)
        queryFrame.pack(fill=X)
        
        label = Label(queryFrame, text="PMID: ")
        label.pack(side=LEFT)
        
        entry = Entry(queryFrame, textvariable=valeur, text='        ')
        entry.pack(side=LEFT)
        
        okButton = Button(queryFrame, text="OK", command=saisie)
        okButton.pack(side=LEFT)

        resultFrame = Frame(frame)
        resultFrame.pack(fill=X)

        resultBox = ScrolledText(resultFrame)
        resultBox.pack(side=LEFT)

root = Tk()
root.title('pyP2B GUI')
app = App(root)

root.mainloop()
