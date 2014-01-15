import mpmath as mpm
import numpy as np

# set max digits
mpm.mp.dps = 1000

e = str(mpm.exp(1))[2:]
start_digit = 0
end_digit = 10


