# coding: utf-8
get_ipython().magic(u'pinfo matplotlib')
A = np.array([[4, 2, 0], [9, 3, 7], [1, 2, 1]], float)
A
np.linalg.det(A)
vals, vecs = np.linalg.eig(A)
vals
vecs
get_ipython().magic(u'pinfo np.linalg.eig')
A
A = np.array([[1, 3, 4], [5, 2, 3]], float) 
A
np.linalg.svd
get_ipython().magic(u'pinfo np.linalg.svd')
np.linalg.matrix_rank(A)
U, s Vh = np.linalg.svd(A)
U, s, Vh = np.linalg.svd(A)
U
s
Vh
A
1 - (11 * 1) + 9  + 110 - 10
1 - 11 + 9 + 11 - 10
np.roots([1, 4, -2, 3])
poly = np.array([1, -11, 9, 11, -10])
poly
np.polyval(poly, 1)
np.polyval(poly, -1)
np.polyval(poly, 10)
x = [1, 2, 3, 4, 5, 6, 7, 8]
y = [0, 2, 1, 3, 7, 10, 11, 19] 
poly = np.polyfit(x, y, 2)
np.polyval(poly, 1)
np.polyval(poly, 2)
np.polyval(poly, 3)
np.polyval(poly, 4)
for val in x:
    print val
    
for val in x:
    ret = np.polyval(poly, val)
    print 0
    
for i, val in enumerate(x):
    ret = np.polyval(poly, val)
    print y[i], ret, y[i] - ret
    
a = np.array([[1, 2, 1, 3], [5, 3, 1, 8]], float) 
A = np.array([[1, 2, 1, 3], [5, 3, 1, 8]], float) 
A
np.corrcoef(A)
np.cov(A)
get_ipython().magic(u'pinfo concatenate')
get_ipython().magic(u'pinfo array')
get_ipython().magic(u'pinfo linalg')
a = arange(4)
a
b = arange(4, 10)
b
r_[a, b]
[a, b]
r_(a, b)
get_ipython().magic(u'pinfo r_')
p = poly1d([3, 4, 5])
p
print p
print p * p
p * p
get_ipython().set_next_input(u'p,integ');get_ipython().magic(u'pinfo integ')
get_ipython().magic(u'pinfo integ')
p.integ(k = 6)
print p.integ(k = 6)
print p
print p.integ
print p.integ()
p.deriv()
polyval(p.integ(), 1)
p(3)
p(4)
p.integ()(1)
p.integ(1)
from scipy import *
from scipy.special import jn, jn_zeros
def drumhead_height(n, k, distance, angle, t):
    nth_zero = jn_zeros(n, k)
    return cos(t) * cos(n * angle) * jn(n, distance * nth_zero)
theta = r_[0:2 * pi:50j]
theta
radius = r_[0:1:50j]
x = array([r * cos(theta) for r in radius])
y = array([r * sin(theta) for r in radius])
z = array([drumhead_height(1, 1, r, theta, 0.5) for r in radius])
import pylab
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
fig = pylab.figure()
ax = Axes3D(fig)
ax.plot_surface(x, y, z, rstride = 1, cstride = 1, cmap = cm.jet)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
pylab.show()
get_ipython().magic(u'help')
get_ipython().magic(u'quickref')
get_ipython().magic(u'save')
get_ipython().system(u'dir /on ')
get_ipython().magic(u'pwd ')
get_ipython().magic(u'cd ..')
get_ipython().magic(u'cd ..')
get_ipython().magic(u'cd ..')
get_ipython().magic(u'cd Code')
