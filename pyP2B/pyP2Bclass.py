#!/usr/bin/python
"""
Retrieve PubMed reference from its PMID given in function
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
import codecs
import xpath
import os
import sys
import urllib2
from xml.dom.minidom import parse

class pyP2B:

    def getPubmedReference(self, pubmedUID):
    
        def striplastdot(s):
            """ Small function to strip last dot in string (along with leading and trailing spaces) """
            l = len(s)
            if l > 1: # at least 1 letter (dot!)
                s.strip()
                if s.endswith('.'):
                    s = s[0:l-1]
            return s

        def stripelref(s):
            """ Small function to strip electronic reference in Journal title (if exists) """
            l = len(s)
            if l > 22: # at least 22 letters
                if s.endswith(" [electronic resource]"):
                    s = s[0:l-22]
            return s
        
        correctRef = False
        tmpFileName = 'pyP2Btmp.xml'
        deftab = 2
	qsStart = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" +\
	          "&db=pubmed&id="
        qsEnd = "&retmode=xml&rettype=medline"

        """ get a PubMed ID and returns a string with ref in BibTex format """
        # Building complete query string
        queryString = qsStart + str(pubmedUID) + qsEnd
        
        # Getting something from PubMed ...
        result = urllib2.urlopen(queryString)

        # Processing file (because it was plain HTML, not.firstChild.wholeText)
        f = open(tmpFileName, 'w')

        for line in result:
#            line = line.replace('<pre>', '')
#            line = line.replace('</pre>', '')
#            line = line.replace('&lt;', '<')
#            line = line.replace('&gt;', '>')
#            line = line.replace('\n', '')
#            line = line.replace('&quot;', '"')
            f.write(line)
        f.close()

        # Verification if it's a correct reference ...
        f = open(tmpFileName, 'r')
        for line in f:
            if line.rstrip().endswith('</PubmedArticleSet>'):
                correctRef = True
        f.close()

        if(correctRef == True):
            # Opening it with lxml and XPath

            doc = parse(tmpFileName)

            # get authors
            authors = u""
            authl = xpath.find('/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/AuthorList/Author/LastName', doc)
            authi = xpath.find('/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/AuthorList/Author/Initials', doc)
            for i in range(len(authl)):
                lastname = unicode((authl[i].firstChild.wholeText))
                initials = ""
                for j in range(len(authi[i].firstChild.wholeText)):
                    initials = initials + unicode(authi[i].firstChild.wholeText)[j]
                    initials = initials + "."
                if i > 0:
                    authors = u"%s and %s, %s" % (authors, lastname, initials)
                else: #i = 0
                    authors = u"%s, %s" % (lastname, initials)

            # get title
            title = xpath.find('/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/ArticleTitle', doc)
            title = striplastdot(title[0].firstChild.wholeText)

            # get year
            year = xpath.find('/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/PubDate/Year', doc)
            year = year[0].firstChild.wholeText

            # build id (first author's last name + two last year digit)
            bibtexId = authl[0].firstChild.wholeText.lower() + year[len(year)-2:len(year)]

            # get journal
            # journal = xpath.find('/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Journal/Title', doc)
            journal = xpath.find('/PubmedArticleSet/PubmedArticle/MedlineCitation/MedlineJournalInfo/MedlineTA', doc)
            journal = stripelref(striplastdot(journal[0].firstChild.wholeText))
		
            # get volume
            volume = xpath.find('/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/Volume', doc)
            volume = volume[0].firstChild.wholeText

            # get issue (if exists)
            issue = xpath.find('/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/Issue', doc)
            if len(issue) > 0:
                issue = issue[0].firstChild.wholeText
            else:
                issue = "0"

            # get pages
            pages = xpath.find('/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Pagination/MedlinePgn', doc)
            pages = pages[0].firstChild.wholeText
            pages = pages.replace("-", "--")

            # get PMID
            pmid = xpath.find('/PubmedArticleSet/PubmedArticle/MedlineCitation/PMID', doc)
            pmid = pmid[0].firstChild.wholeText

            # get doi (if exists)
            idlist = xpath.find('/PubmedArticleSet/PubmedArticle/PubmedData/ArticleIdList/ArticleId', doc)
            doi = "0"
            if len(idlist) > 0:
                for i in range(len(idlist)):
                    if str(idlist[i].attributes['IdType'])== 'doi':
                        doi = idlist[i].firstChild.wholeText

            f.close()

            # Now write output (to include in a pipe)
            result = u""
            # result = result + "@article{%s,\n" % (bibtexId)
            result = result + u"@article{pmid%s,\n" % (pmid)
            result = result + u"\tauthor = {%s},\n" % (authors)
            result = result + u"\ttitle = {%s},\n" % (title)
            result = result + u"\tyear = %s,\n" % (year)
            result = result + u"\tjournal = {%s},\n" % (journal)
            result = result + u"\tvolume = {%s},\n" % (volume)
            if issue != "0":
                result = result + u"\tnumber = %s,\n" % (issue)
            result = result + u"\tpages = {%s},\n" % (pages)
            result = result + u"\tpmid = %s,\n" % (pmid)
            if doi != "0":
                result = result + u"\tdoi = {%s},\n" % (doi)
            result = result + u"\tkeywords = {}\n"
            result = result + u"}"

            # Clean up things ...
            os.remove(tmpFileName)
        else:
            result = "Reference %s not found. Aborting" % str(pubmedUID)
            
        return(result)
