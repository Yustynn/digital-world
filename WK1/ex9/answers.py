def avgMarks(*marks):
    return sum(marks) / len(marks)

# QUESTION (a)

def printInfo(name, sid, *marks):
    marks = avgMarks(*marks)

    print "NAME: {0}".format(name)
    print "STUDENT ID: {0}".format(sid)
    print "AVG MARKS: {0}".format(marks)

printInfo("Yustynn!! Panicker", "1002011", 50, 120, 30)

# QUESTION (b)

def printPassFail(*marks):
    print ("TRUE" if avgMarks(*marks) >= 50 else "FAIL")

printPassFail(50, 30, 20, 100) # should print "TRUE"
printPassFail(10, 30, 20, 100) # should print "FALSE"

# QUESTION (c)

def printGrade(*marks):
    marks = avgMarks(*marks)

    if   marks < 60: print "F"
    elif marks < 70: print "D"
    elif marks < 80: print "C"
    elif marks < 90: print "B"
    else:            print "A"

printGrade(50, 30, 90, 100) # should print "D"

