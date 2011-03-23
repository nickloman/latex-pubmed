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
import sys

myref = pyP2B()
print myref.getPubmedReference(sys.argv[len(sys.argv)-1])
