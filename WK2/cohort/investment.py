def compound_value_sixth_months(amt, rate):
  val = 0
  rate /=12

  for i in xrange(0, 6):
    val += amt
    val *= 1 + rate

  return val

print compound_value_sixth_months(100,0.05)
