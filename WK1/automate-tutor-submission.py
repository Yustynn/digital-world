from time import sleep
from os import environ
from splinter import Browser
from termcolor import cprint

from evil_eval import get_answers

browser = Browser()

# Visit Login Page
url = 'http://10.1.3.25/digitalworldtutor/login/'
browser.visit(url)
browser.fill('username', environ['TUTOR_USERNAME'])
browser.fill('password', environ['TUTOR_PASSWORD']) 
# Find and click the 'search' button
sleep(0.5)
button = browser.find_by_css('input[type="submit"]')
# Interact with elements
button.click()

while True:
    question_number = raw_input("Enter question number (1, 2, 4, 6, 7 available): ")
    ex = get_answers('ex' + question_number)

    url = 'http://10.1.3.25/digitalworldtutor/tutor2/'
    browser.visit(url)
    button = browser.find_by_name('display-problems wk=1')
    button.click()

    # Question Selection Page
    button = browser.find_by_value('Wk.1.1.' + question_number)
    button.click()

    for (idx, qn) in enumerate( ex ):
        input_name = 'abox' + str(idx + 1).zfill(3)
        ans = str( qn['answer'] )
        # browser.fill(input_name, "hi") 
        browser.fill(input_name, ans) 
        print browser.find_by_name(input_name)['size']

    button = browser.find_by_value("Check")

    raw_input('ENTER ANYTHING TO CONTINUE')

    button.click()

    for (idx, el) in enumerate( browser.find_by_css('ol li img' ) ):
        ex[idx]['is_correct'] = el['alt'] == 'WELL DONE'

    wrong_qns = filter(lambda qn: not qn['is_correct'], ex)

    for qn in wrong_qns:
        cprint( qn['letter'], 'yellow' )
        cprint( qn['command'], 'blue' )
        cprint( qn['answer'], 'red' )
        print '\n'

    sleep(5000)

