Bumble is a blogging engine a bit similar to tumblr, but with the ability to create pages and sub-blogs within those pages. It is licensed under the GPLv2 licence. Other licencing terms available on request.

# Documentation
First off, these docs are almost certainly not as complete and helpful as they could me. Feel free to [drop me a line](mailto:david.stark@zarkonnen.com) if you are struggling with setup or have suggestions for improving the docs.

This version of Bumble was developed against Python 3.5 and Django 1.11.

## Installation
### Requirements
A server with Apache, Python 3 (and the ability to install Python packages) and a database. SQLite will do in a pinch. Git is a plus. We've done some installs on [Webfaction](https://www.webfaction.com/), but anyplace that satisfies the above requirements will do.

### Development installation
* Download or clone Bumble
* Initialise and activate a virtual environment: `python3 -m venv venv && source venv/bin/activate`
* Make sure your version of pip is at least 9.0.1
* Install the required packages using pip: `pip install -r requirements.txt`
* Then, export the following environment variables:
* `export DJANGO_SETTINGS_MODULE=bumble.local_settings`
* `export PYTHONPATH=$PYTHONPATH:<path-to-bumble-install>`
* Run `django-admin migrate` to create the database
* Run `django-admin createsuperuser` to create the admin, entering a username and password when prompted
* Run `django-admin runserver` to start the server

### Deployment
* Download or clone Bumble into a suitable location on the server.
* Make sure your version of pip is at least 9.0.1.
* Install the required packages using pip: `pip install -r requirements.txt`.
* [Set up mod_wsgi](http://ericholscher.com/blog/2008/jul/8/setting-django-and-mod_wsgi/) to point to the Bumble install.
* Edit local_settings.py and change the following things:
    * Add your name and email address to ADMINS
    * Fill in the DB connection details in DATABASES
    * Set the appropriate timezone.
    * Set STATIC_ROOT to `"<webroot-path>/static/"`, e.g `"/var/www/static/"`
    * Set MEDIA_ROOT to `"<webroot-path>/static/media/"`, e.g `"/var/www/static/media/"`
    * Change SECRET_KEY to something else - you can use [this tool](http://www.miniwebtool.com/django-secret-key-generator/) to make a valid new key
    * Add your domain names to ALLOWED_HOSTS
    * If you need email, uncomment and configure the email settings
* Follow the instructions in bumbl/settings.py to set up the recaptcha
* Then, export the following environment variables:
* `export DJANGO_SETTINGS_MODULE=bumble.local_settings`
* `export PYTHONPATH=$PYTHONPATH:<path-to-bumble-install>`
* Run `django-admin migrate` to create the database
* Run `django-admin createsuperuser` to create the admin, entering a username and password when prompted
* Restart apache if needed

## Usage
### Front page setup
Once you have set things up correctly, you should be greeted by a 404 page. This is because you haven't defined a root page. In your browser, visit `<your bumble install>/admin/` to log into the admin system with the username and password you've set. Once there, create a new Entry. Fill in the title of your site, but **leave the slug field blank**. Also fill in the lead field to contain whatever you want to appear at the top of the site. Once you've done that, hit save, and the 404 page should change to that front page on reload.

### A second entry
You can now make a second entry, for example a blog post saying "I just set up Bumble!". To do this, create another Entry in the admin system. This time, the entry **must** have a slug, and its parent must be the front page entry you just created - otherwise it won't show up. **All entries except the front page must have a slug and a parent, and the front page must have neither.**

### Structure
Bumble sites are a tree of Entries. An entry can be a blog post or a whole sub-site with sub-entries. Each entry has a *slug* which is its part of the URL. For example, an entry `kittens` in `animals_i_like` would have the URL of `<your bumble install>/animals_i_like/kittens`.

Since the site is a tree structure, all entries except for the front page have a parent. Top-level entries have the front page as a parent.

Each entry is displayed as a number of sections:
* Title
* Lead
* Content
* Ancestors' section content
* Comment form (if comments are turned on)
* List of comments
* List of descendant entries (with automatic loading of more entries)

The descendant entries are each listed with their title and lead. Note that this means that sub-sub and sub-sub-...-sub entries of an entry are also displayed in this list. So the front page gives an account of everything that's happening on the site, whereas a sub-page will only show the sub-site news.

### Editing options
You can write Bumble content in HTML or in markdown, or a mixture of the two. HTML is the default, and you can enclose any markdown in triple asterisks `***`.

### CSS
Each entry has a CSS section which is included both in the entry and in its descendants. This means that if you want to create a sub-site out of an entry, you can radically change the styling of that entry and all entries below it will have the same styling.

There is also a "Local CSS" field for CSS that pertains only to this entry and should not percolate down.

### Section content
In addition, there is a "section content" field, which contains HTML / markdown that you want included in all descendant pages. This is useful especially for Javascript snippets like Google Analytics.

### Files
You can upload files to Bumble by creating Files in the admin interface. To refer to a file in HTML or markdown, use the syntax `{{f:name_of_file}}`, which is automatically substituted with the full path of the file. So you can upload a file called "kittens.jpg" as "kittens" and use `<img src="{{f:kittens}}">` to display it.

### Tags
You can create tags and add entries to them, allowing people to browse your site by tags. In HTML or markdown, use the syntax `{{tagslist}}` to insert a list of tags sorted by popularity.

### RSS
Each bumble entry and tag page links to an appropriate RSS feed to follow that topic.

### Twitter cards
Finally, Bumble also has (somewhat rudimentary) Twitter card support. To activate this, use the [Twitter Card Validator](https://dev.twitter.com/docs/cards/validation/validator). (Note that this activation is not instantaneous nor retroactive - earlier tweets to Bumble links will not acquire Twitter cards.)
