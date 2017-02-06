def minutes_to_years_days(mins):
  from math import floor

  total_days = int( floor(mins / 24 / 60) )
  days = total_days % 365
  years = int( floor(total_days / 365) )

  return (years, days)


mins = int( raw_input("Enter the number of minutes: ") )

years, days = minutes_to_years_days(mins)
print "{0} minutes is approximately {1} years and {2} days.".format(mins, years, days)
