# Solutions for Introductory Time Series with R
# Chapter 3
# Jacob Carey
# 12-18-13

w <- 1:100
for (k in c(1, 10, 100)) {
  x <- w+k*rnorm(100)
  y <- w+k*rnorm(100)
  print(k)
  print(cor(x, y))
  ccf(x, y)
}

Time <- 1:370
x <- sin(2*pi*Time/37)
y <- sin(2*pi*(Time+4)/37)

print(cor(x, y))
ccf(x, y)