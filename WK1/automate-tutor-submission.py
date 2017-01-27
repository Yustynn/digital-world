from time import sleep
from os import environ
from splinter import Browser
from termcolor import colored, cprint

from evil_eval import get_answers

# SETUP
question_numbers = map(str, [1, 2, 6, 7])
browser = Browser()

def wait(seconds = 0.5):
    sleep(seconds)


# LOGIN
url = 'http://10.1.3.25/digitalworldtutor/login/'
browser.visit(url)
browser.fill('username', environ['TUTOR_USERNAME'])
browser.fill('password', environ['TUTOR_PASSWORD']) 
wait() # incase page doesn't load quickly enough

button = browser.find_by_css('input[type="submit"]')
button.click()
wait()

raw_input( colored("READY TO BEGIN. PRESS ENTER TO CONTINUE.", 'green') )

# FILL IN EACH QN
for question_number in question_numbers:
    ex = get_answers( 'ex' + question_number )
    
    print question_number
    # GO TO HOME -> WK 1 -> QN
    url = 'http://10.1.3.25/digitalworldtutor/tutor2/'
    browser.visit(url)
    button = browser.find_by_name('display-problems wk=1')
    button.click()

    button = browser.find_by_value( 'Wk.1.1.' + question_number )
    button.click()

    for (idx, qn) in enumerate( ex ):
        input_name = 'abox' + str(idx + 1).zfill(3)
        ans = str( qn['answer'] )
        # browser.fill(input_name, "hi") 
        browser.fill(input_name, ans) 
    
    raw_input( colored('PRESS ENTER TO CHECK ANSWERS', 'green') )

    button = browser.find_by_value("Check")
    button.click()

    for (idx, el) in enumerate( browser.find_by_css('ol li img' ) ):
        ex[idx]['is_correct'] = el['alt'] == 'WELL DONE'

    wrong_qns = filter(lambda qn: not qn['is_correct'], ex)
    if len(wrong_qns) > 0:
        cprint( "{0} auto-generated answers were wrong. Please correct before continuing.".format( len(wrong_qns) ), 'red'  )

        for qn in wrong_qns:
            cprint( qn['letter'], 'yellow' )
            cprint( qn['command'], 'blue' )
            cprint( qn['answer'], 'grey' )
            print '\n'

    raw_input( colored("PRESS ENTER TO SUBMIT ANSWERS", 'green') )
    button = browser.find_by_value("Submit")
    button.click()
    

cprint( "Questions submitted successfully!", 'green' )
