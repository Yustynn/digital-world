import re

def get_answers(ex):
    file = open(ex + '.txt')
    answers = []
    
    for ln in file:
        qn = {
            'letter': re.match('\((.)\)', ln).group(1),
            'command': re.split('\(.\) ', ln)[1].replace('print ',
                '').replace('\n', '')
        }

        try:
            qn['answer'] = eval(qn['command'])
        except:
            qn['answer'] = 'Error'

        answers.append(qn)

    return answers

