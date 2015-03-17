# create virtual environment
.env:
	virtualenv .env

# install all needed for development
develop: .env
	.env/bin/python bootstrap.py
	.env/bin/pip install -e . tox
	bin/buildout

# clean the development envrironment
clean:
	-rm -rf .env
