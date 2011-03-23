
paper.pdf: paper.tex
	# first build extracts the references to paper.aux
	python gorefs.py paper.tex myrefs.bib
	rm -f paper.aux
	pdflatex paper
	bibtex paper
	pdflatex paper
	pdflatex paper

