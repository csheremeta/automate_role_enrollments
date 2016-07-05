#!/usr/bin/python

# So far, this script will log into the ROLE system, assuming you update lines
# 51 and 52 with your username and password. From there, the script will then
# navigate to the "Enrollments" page and will scrape all of the data from that
# page, saving it as a .xls which can be imported into a DB. However, we will
# be changing that part of the script to automate enrollments. See "TO-DO"
# section at bottom of this file. This script ignores HTTPS certificates, but 
# you must be on RH VPN to access the ROLE site.

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

# The site we will navigate into, handling its session
br.open('https://role.rhu.redhat.com/rol/')

# Select the first (index zero) form
br.select_form(nr=0)

# User credentials
br.form['username'] = '' # change me!
br.form['password'] = '' # change me!

# Login
response = br.submit()

# Access dashboard (3rd link, or index 2)
# You could access the "Admin" page by using link 1 instead of 2 (to search for
# users, etc)
response = br.follow_link(nr=2)

# uncomment the following 2 lines to print list of links to choose from once you
# are at the dashboard page (or any other page you want to get to). this will
# help you determine where you want to go next.
#
#for link in br.links():
#    print link

# for example, if I want to go to the enrollments page...
response1 = br.follow_link(nr=15)

# everything from here down scrapes the data off that page and saves it as a
# .xls file. we probably will not need this code, but I'm leaving it here in
# case we find some use for it.
new_file = open("/tmp/new_db.txt", "w")
new_file.write(response1.read())
new_file.close()

lines = open('/tmp/new_db.txt').readlines()
open('/tmp/curr_db.xls', 'w').writelines(lines[215:-71]) #this removes the lines that aren't part of the table we're trying to access

# TO-DO:
#	- use CSV script we made with Dave at beginning of internship to get
#	  list of enrollments needing to be processed (we will need to edit this
#	  a little more in order to determine which enrollment was last
#	  processed, so the script knows where to start)
#	- for each row in enrollment spreadsheet:
#	- instead of navigating to enrollment page, navigate to user page and
#	  look for username based on email
#	- if username not found on that page, navigate to Enrollments page and
#	  search for username there
#	- if username not found there either, print a statement saying we need
#	  to email user@redhat.com regarding course_num (region)
#	- if username is found somewhere, save username and emails as variables,
#	  and navigate to the Classes page
#	- find correct course based on class requested, region, and country
#	  (APAC will be difficult, here, as well as courses that do not have a
#	  specific section for a given region)
#	- when correct section is found, check to see if that username/email is
#	  already enrolled in that section. if so, update enrollment to add 90
#	  days
#	- if user is not already enrolled in course, enroll the user and send
#	  automated email from ROLE system welcoming the user
#	- continue to next row in spreadsheet
