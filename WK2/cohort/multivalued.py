def position_velocity(v, t):
  g = 9.81
  y = v*t - 0.5 * g * t**2
  y_prime = v - g*t

  return (y, y_prime)
