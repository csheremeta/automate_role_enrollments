#!/usr/bin/python
# This file is meant to open a Selenium webdriver with Python, which
# you can then use to automate the rest of steps required to process
# new enrollments (the ones that involve interacting with ROLE).
#
# The "mechanize" module is used in 
# https://github.com/csheremeta/automate_role_enrollments/scrape_enrollments.py
# to automate a different part of the ROLE sys admin process. See notes in
# that file for other automation ideas. Thanks!
#
# Candace Sheremeta (candace.aleea@gmail.com)
import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

binary = FirefoxBinary('/opt/firefox-43/firefox')

def init_driver():
    driver = webdriver.Firefox(firefox_binary=binary)
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, query):
    driver.get("http://www.google.com")
    try:
        box = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "q")))
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.NAME, "btnK")))
        box.send_keys(query)
        button.click()
    except TimeoutException:
        print("Box or Button not found in google.com")
 
 
if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, "Selenium")
    time.sleep(5)
    driver.quit()

