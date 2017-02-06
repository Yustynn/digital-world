def compound_value_sixth_months(amt, rate):
  val = 0
  rate /=12

  for i in xrange(0, 6):
    val += amt
    val *= 1 + rate

  return round(val, 2)

amt = int( raw_input("Enter the monthly saving amount: ") )
rate = float( raw_input("Enter annual interest rate: ") )

print "After the sixth month, the account value is {0}".format(compound_value_sixth_months(amt, rate))
