import numpy as np
from mpmath import mpi, mp

# Set decimal precision
mp.dps = 4

# ---------------------------------------------------------
# PLACEHOLDERS: Define your variable bounds here using mpi(min, max)
# ---------------------------------------------------------
sigma     = mpi(2.0e6, 2.5e6)     # Locked down to premium silicon steel conductivity
thickness = mpi(0.0002, 0.0005)   # somewhere in this range
B_max     = mpi(1.1, 1.4)         # Standard operating magnetic sweep
volume    = mpi(2.17e-5, 2.45e-5) # Restricted to 40% - 45% real iron fill factor
poles     = 24

# ---------------------------------------------------------
# EQUATION: Evaluated using interval arithmetic
# ---------------------------------------------------------
# Note: Using np.pi ** 2 directly
pi_sq = np.pi ** 2

k_e = pi_sq * sigma * (thickness ** 2) * (B_max ** 2) * volume * ((poles / 120.0) ** 2) / 6.0

# ---------------------------------------------------------
# OUTPUT: Extracted minimum and maximum bounds
# ---------------------------------------------------------
print(f"The lower bound of k_e is: {k_e.a}")
print(f"The upper bound of k_e is: {k_e.b}")
print(f"The full bounded interval is: {k_e}")


# ------------------------------------------------------------------------------------------------


# ---------------------------------------------------------
# PLACEHOLDERS: Define your variable bounds here using mpi(min, max)
# ---------------------------------------------------------
eta    = mpi(35, 45)            # Steinmetz hysteresis coefficient
beta   = mpi(1.05, 1.15)          # Empirical correction factor
n      = mpi(1.6, 1.6)          # Steinmetz exponent for standard sillicon steel used in agri motors
poles  = 24                     # Number of motor poles

# ---------------------------------------------------------
# EQUATION: Calculate the constant multiplier factor (C)
# ---------------------------------------------------------
# C = neta * beta * (Bmax^n) * Volume * (poles / 120)
constant_factor = eta * beta * (B_max ** n) * volume * (poles / 120.0)

# ---------------------------------------------------------
# OUTPUT: Extracted minimum and maximum bounds
# ---------------------------------------------------------
print(f"Lower bound for the constant k_h: {constant_factor.a}")
print(f"Upper bound for the constant k_h: {constant_factor.b}")
print(f"P_h range = [{constant_factor.a} * RPM, {constant_factor.b} * RPM]")
