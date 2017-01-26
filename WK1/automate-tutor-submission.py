from time import sleep
from os import environ
from splinter import Browser
from evil_eval import get_answers

ex1 = get_answers('ex1')

with Browser() as browser:
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
    
    button = browser.find_by_name('display-problems wk=1')
    button.click()
    
    # Question selection page
    # note: can swap out Q1 for Q(number)
    button = browser.find_by_value('Wk.1.1.1')
    button.click()

    for (idx, qn) in enumerate( ex1 ):
        input_name = 'abox' + str(idx + 1).zfill(3)
        ans = str( qn['answer'] )
        # browser.fill(input_name, "hi") 
        browser.fill(input_name, ans) 
        print browser.find_by_name(input_name)['size']
    
    button = browser.find_by_value("Check")

    raw_input('ENTER ANYTHING TO CONTINUE')

    button.click()

    for (idx, el) in enumerate( browser.find_by_css('ol li img' ) ):
        ex1[idx]['is_correct'] = el['alt'] == 'WELL DONE'

    wrong_qns = filter(lambda qn: not qn['is_correct'], ex1)

    for qn in wrong_qns:
        print qn['letter']
        print qn['command']
        print qn['answer']
        print '\n'

    sleep(5000)

