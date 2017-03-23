LX = xelatex
MI = makeindex
BX = bibtex

FILEN = schaefer-egbd
TEXFLAGS =
#TEXFLAGS = -interaction=nonstopmode
PREFLAGS = -no-pdf

once:
	cp $(FILEN).ind.edited $(FILEN).ind
	cp $(FILEN).toc.edited $(FILEN).toc
	-$(LX) $(TEXFLAGS) $(FILEN) # | grep 'Warning'

quick:
	-$(LX) $(TEXFLAGS) $(PREFLAGS) $(FILEN)
	printf "\033c"
	@echo
	@echo " === LAST RUN === "
	@echo
	cp $(FILEN).toc.edited $(FILEN).toc
	cp $(FILEN).ind.edited $(FILEN).ind
	-$(LX) $(TEXFLAGS) $(FILEN) | grep 'Warning'

clean:
	\rm *.adx *.and *.aux *.bbl *.blg *.idx *.ilg *.ldx *.lnd *.log *.out *.pdf *.rdx *.run.xml *.sdx *.snd *.toc *.wdx *.xdv
	\rm chapters/*.aux

all:
	-$(LX) $(TEXFLAGS) $(PREFLAGS) $(FILEN)
	-$(BX) $(FILEN)
	-$(LX) $(TEXFLAGS) $(PREFLAGS) $(FILEN)
	texindy --german schaefer-egbd.idx
	-$(LX) $(TEXFLAGS) $(PREFLAGS) $(FILEN)
	printf "\033c"
	@echo
	@echo " === LAST RUN === "
	@echo
	cp $(FILEN).ind.edited $(FILEN).ind
	cp $(FILEN).toc.edited $(FILEN).toc
	-$(LX) $(TEXFLAGS) $(FILEN) # | grep 'Warning'


view:
	/Applications/Skim.app/Contents/MacOS/Skim $(FILEN).pdf & 

edit:
#	mvim -c ':set spell spelllang=de' -c ':nnoremap <F12> ]s' -c ':nnoremap <F11> [s' -c ':nnoremap <F10> zg' chapters/*.tex schaefer-egbd.tex local*.sty
	mvim -c ':set spell spelllang=de' -c ':nnoremap <F15> ]s' -c ':nnoremap <F14> [s' chapters/*.tex schaefer-egbd.tex local*.sty
