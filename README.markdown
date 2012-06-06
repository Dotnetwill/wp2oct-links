#wp2oct-links#

A small python script that to inspect an exported wordpress XML file and generate nginx rewrite rules for old urls to the default octopress style.  It creates the rewrites as permanent redirects.

It outputs the rules to stdout so you can copy/paste or whatever into the relevant nginx conf.

##Usage##
    python wp2oct-link.py /path/to/workpress-export.xml

##Installation##
This app requires lxml and slugify.  You can install them manually or do:

    pip install -r requirements.txt

##Feedback##
Please refer to http://github.com/dotnetwill/wp2oct-links
