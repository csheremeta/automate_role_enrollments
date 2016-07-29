#!/usr/bin/python
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
import re

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


# NOTE: the script currently fails at the following line, which has been the
# case since the transition on July 25, 2016. You will need to research why the
# script currently returns the following error:
#
#  [candace@firebolt Desktop]$ ./scrape_enrollments.py 
# ./scrape_enrollments.py:17: UserWarning: gzip transfer encoding is experimental!
#   br.set_handle_gzip(True)
# Traceback (most recent call last):
#   File "./scrape_enrollments.py", line 44, in <module>
#     for form in br.forms():
#   File "/usr/lib/python2.7/site-packages/mechanize/_mechanize.py", line 419, in forms
#     raise BrowserStateError("not viewing HTML")
# mechanize._mechanize.BrowserStateError: not viewing HTML
#
# The site we will navigate into, handling its session
br.open('https://role.rhu.redhat.com/rol-rhu/rhz/login')

# uncomment the following 2 lines to print list of links to choose from
for form in br.forms():
    print forms

# Select the 0th form (all indexes start at 0)
#br.select_form(nr=0)

# User credentials
#br.form['username'] = '' # change me!
#br.form['password'] = '' # change me!

# Login
#response = br.submit()

#for link in br.links():
#    print link

# Access dashboard (3rd link, or index 2)
#response = br.follow_link(nr=2)

# uncomment the following 2 lines to print list of links to choose from
#for link in br.links():
#    print link

# this accesses the "Enrollments" page of the ROLE Dashboard; in order to
# access and scrape some other page, you simply need to change the link number
# 
#response1 = br.follow_link(nr=15)

#new_file = open("/tmp/new_db.txt", "w")
#new_file.write(response1.read())
#new_file.close()

#lines = open('/tmp/new_db.txt').readlines()
# this removes the lines that aren't part of the table we're trying to access
# these numbers may change based on the page you are trying to scrape
#open('/tmp/curr_db.xls', 'w').writelines(lines[215:-71])
#print('The enrollment data can now be found in /tmp/curr_db.xls') 
