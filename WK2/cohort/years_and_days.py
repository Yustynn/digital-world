def minutes_to_years_days(mins):
  from math import floor

  total_days = int( floor(mins / 24 / 60) )
  days = total_days % 365
  years = int( floor(total_days / 365) )

  return (years, days)
