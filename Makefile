PELICAN       = pelican
PELICANOPTS   =
INPUTDIR      = content
OUTPUTDIR     = output
CONFFILE      = pelicanconf.py
PUBLISHCONF   = publishconf.py

help:
	@echo 'Makefile for a Pelican Web Site'
	@echo ''
	@echo 'Usage:'
	@echo '  make html          (re)generate the site'
	@echo '  make clean         remove the generated files'
	@echo '  make serve         serve the site locally on port 8000'
	@echo '  make devserver     auto-reload on changes (port 8000)'
	@echo '  make github        deploy to GitHub Pages (gh-pages branch)'

html:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

serve:
	cd $(OUTPUTDIR) && python3 -m http.server 8000

devserver:
	$(PELICAN) --listen --autoreload $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE)

github: html
	ghp-import -m "Publish site" -b gh-pages $(OUTPUTDIR)
	git push origin gh-pages

.PHONY: html clean serve devserver github
