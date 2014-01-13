# Solutions for Introductory Time Series with R
# Chapter 1
# Jacob Carey
# 12-13-12

# Prepare data

# Problem 1 data
www <- "http://elena.aut.ac.nz/~pcowpert/ts/cbe.dat"
CBE <- read.table(www, header=T)
Beer.ts <- ts(CBE[,2], start=1958, freq=12)

# Problem 2, 3 data
Auto <- matrix(c(0.33, 18000, 0.5, 20000, 2000, 0.8, 1500, 1.6,
                 40, 40, 20, 60, 3, 80, 2, 120, 2, 200, 1, 360), 
               byrow=T, nrow=5)

Auto.df <- data.frame(Auto, row.names=c("car", "petrol", "servicing", 
                                        "tyre", "clutch"))

colnames(Auto.df) <- c("quantity.00", "unit.price.00", 
                       "quantity.04", "unit.price.04")

# PDF of plots
pdf(file="~/R/Time_Series_R/chap_1.pdf")

# 1a
# Time plot of data
Beer.year <- aggregate(Beer.ts, FUN=sum)

plot(Beer.ts, xlab="Year", ylab="Beer (Ml)", main="Austrialian Beer Production")
plot(Beer.year, xlab="Year", ylab="Beer (Ml)", main="Australian Beer Production (Annual)")
boxplot(Beer.ts~cycle(Beer.ts), xlab="Month", ylab="Beer (Ml)", main="Monthly Production of Austrial Beer", xaxt="n")
axis(1, 1:12, month.abb[1:12])

# 1b
Beer.decompose <- decompose(Beer.ts, "multi")
Trend <- Beer.decompose$trend
Seasonal <- Beer.decompose$seasonal

plot(Beer.decompose, xlab="Year")
ts.plot(cbind(Trend, Trend*Seasonal), lty=1:2, xlab="Year", ylab="Beer (Ml)", main="Australian Beer Production Time Series Model\nSuperimposed over Production Trend")

# Problem 2
# 2
LI_t <- sum(Auto.df$quantity.00*Auto.df$unit.price.04)/
  sum(Auto.df$quantity.00*Auto.df$unit.price.00)
cat(sprintf("The Laspeyre Price Index for this data is %.2f", 
              LI_t))
cat("\n")

# Problem 3

# 3a
PI_t <- sum(Auto.df$quantity.04*Auto.df$unit.price.04)/
  sum(Auto.df$quantity.04*Auto.df$unit.price.00)
cat(sprintf("The Paasche Price Index for this data is %.2f", 
              PI_t))
cat("\n")

# 3b
cat("People tend to buy fewer of things as the prices increase, and since the quantity used in this calculation comes from step t instead of step 0,\nthe quantity for items that have increased in price is typically lower")
cat("\n")

# 3c
cat(sprintf("The Irving-Fisher Price Index for this data is %.2f", 
              sqrt(LI_t * PI_t)))
cat("\n")

invisible(dev.off())