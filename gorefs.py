from pyP2B.pyP2Bclass import pyP2B
import sys
import re
from accents import latexAccents

def utf_to_latex(text):
    for search, replace in latexAccents:
         text = text.replace(search, replace)
    return text

tex = open(sys.argv[1]).read()

fh = open(sys.argv[2], "w")

for m in re.findall("cite\{pmid(\d+)\}", tex):
    myref = pyP2B()

    utf_text = myref.getPubmedReference(m)
    print >>fh, utf_to_latex(utf_text)

