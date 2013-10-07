Bumble is a blogging engine a bit similar to tumblr, but with the ability to create pages and sub-blogs within those pages. It is licensed under the GPLv2 licence. Other licencing terms available on request.

## Installation
### Requirements
A server with Apache, Python (and the ability to install Python packages) and a database. SQLite will do in a pinch. Git is a plus. We've done some installs on [Webfaction](https://www.webfaction.com/), but anyplace that satisfies the above requirements will do.
### Installation procedure
* Download or clone Bumble into a suitable location on the server
* [Set up mod_wsgi](http://ericholscher.com/blog/2008/jul/8/setting-django-and-mod_wsgi/) to point to the Bumble install.
* Using pip or easy_install, install the following python modules: [requests](http://docs.python-requests.org/en/latest/) and [markdown](https://pypi.python.org/pypi/Markdown/2.3.1).
* You may also want to install [south](http://south.aeracode.org/) to handle future DB migrations.
* Finally, edit settings.py and change the following things:
* Add your name and email address to ADMINS
* Fill in the DB connection details in DATABASES
* Set the appropriate timezone if you're not in Chicago
* Set MEDIA_URL to "/static/bumble/media/"
* Set STATIC_ROOT to <webroot-path>/static, eg /var/www/static/
* Change SECRET_KEY to something else - you can use [this tool](http://www.miniwebtool.com/django-secret-key-generator/) to make a valid new key
* Then, export the following environment variables:
* export DJANGO_SETTINGS_MODULE=bumble.settings
* export PYTHONPATH=$PYTHONPATH:<path-to-bumble-install>
* Run manage.py syncdb to create the database, entering an admin username and password when prompted
* Restart apache if needed

## Usage
### Front page setup
Once you have set things up correctly, you should be greeted by a 404 page. This is because you haven't defined a root page. Go to <your bumble install>/admin/ to log into the admin system with the username and password you've set. Once there, create a new Entry. Fill in the title of your site, but **leave the slug field blank**. Also fill in the lead field to contain whatever you want to appear at the top of the site. Once you've done that, hit save, and the 404 page should change to that front page on reload.

### Structure

### Editing options

### CSS

### Twitter cards
