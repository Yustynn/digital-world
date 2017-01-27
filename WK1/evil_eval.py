import re

def get_answers(ex):
    file = open(ex + '.txt')
    answers = []
    
    for ln in file:
        qn = {
            'letter': re.match('\((.)\)', ln).group(1),
            'command': re.split('\(.\) ', ln)[1].replace('\n', '')
        }

        try:
            qn['answer'] = eval( qn['command'].replace('print ', '') )
        except:
            qn['answer'] = 'Error'

        answers.append(qn)

    return answers

