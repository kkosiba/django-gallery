# django-gallery
Responsive Bootstrap gallery with Django backend

Features
--------

1. Authorisation.
3. Facebook comments
4. Tags
5. Search, sort pictures by album or tags.


Main requirements
------------

1. `python` 3.5+
2. `Django` 2.1

This project also uses a few external packages (see `requirements.txt` for details). Processing images is done via [Pillow](https://github.com/python-pillow/Pillow) and tags via [django-taggit](https://github.com/alex/django-taggit).


Usage
-----

1. Create a new directory and change to it:

`mkdir django-gallery && cd django-gallery`

2. Clone the repository:

`git clone https://github.com/ncunx/django-gallery.git .`

3. Set up a virtual environment and activate it:

`python3 -m venv <preferred_name> && source <preferred_name>/bin/activate`

4. Install required packages:

`pip3 install -r requirements.txt`

The project is all set up. Run a local server with

`python3 manage.py runserver`

The gallery should be available at `localhost:8000`.


Credits
-------
Sample data for the gallery by courtesy of [Unsplash](https://unsplash.com/)