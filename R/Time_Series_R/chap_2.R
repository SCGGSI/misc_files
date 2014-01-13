# Solutions for Introductory Time Series with R
# Chapter 2
# Jacob Carey
# 12-16-12

# Prepare data

# Problem 1 data
www1 <- "http://elena.aut.ac.nz/~pcowpert/ts/varnish.dat"
www2 <- "http://elena.aut.ac.nz/~pcowpert/ts/guesswhat.dat"

varnish <- read.table(www1, header=T)
guesswhat <- read.table(www2, header=T)

# Problem 2 data
wine.mat <- matrix(c(39, 35, 16, 18, 7, 22, 13, 18, 20, 9, -12, 
              -11, -19, -9, -2, 16, 47, -26, 42, -10, 27, 
              -8, 16, 6, -1, 25, 11, 1, 25, 7, -5, 3), ncol=2)

wine <- as.data.frame(wine.mat)
colnames(wine) <- c("SS", "CC")

# Problem 3
www <- "http://elena.aut.ac.nz/~pcowpert/ts/global.dat"
Global <- scan(www)
Global.ts <- ts(Global, st=1856, fr=12)

# Problem 4
www <- "http://elena.aut.ac.nz/~pcowpert/ts/Fontdsdt.dat"
Font <- read.table(www, header=T)
Font.ts <- ts(Global, st=1909, fr=12)

# PDF of plots
pdf(file="~/R/Time_Series_R/chap_2.pdf")

# 1
plot(y~x, data=varnish, main="Plot of Varnish Data")
var_cor <- cor(varnish$y, varnish$x)
print(var_cor)

plot(y~x, data=guesswhat, main="Plot of guesswhat Data")
gw_cor <- cor(guesswhat$y, guesswhat$x)
print(gw_cor)

# 2
CC.ts <- ts(wine$CC)
SS.ts <- ts(wine$SS)

plot(CC.ts, ylab="Relative Wine Content", main="Cagey Chardonnay")
plot(SS.ts, ylab="Relative Wine Content", main="Serendipity Shiraz")

acf(CC.ts)
acf(SS.ts)

# 3
Global.decom <- decompose(Global.ts)
plot(Global.decom)
sd(Global.ts)
sd(Global.ts-Global.decom$seasonal)
Trend <- Global.decom$trend
Seasonal <- Global.decom$seasonal
Random <- Global.decom$random

ts.plot(cbind(Trend, Trend+Seasonal), lty=1:2)
acf(Random[7:1794])
dev.off()