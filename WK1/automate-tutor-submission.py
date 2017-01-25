from time import sleep
from os import environ
from splinter import Browser

with Browser() as browser:
    # Visit Login Page
    url = 'http://10.1.3.25/digitalworldtutor/login/'
    browser.visit(url)
    browser.fill('username', environ['TUTOR_USERNAME'])
    browser.fill('password', environ['TUTOR_PASSWORD']) 
    # Find and click the 'search' button
    button = browser.find_by_css('input[type="submit"]')
    # Interact with elements
    button.click()
    
    button = browser.find_by_name('display-problems wk=1')
    button.click()
    sleep(5000)

