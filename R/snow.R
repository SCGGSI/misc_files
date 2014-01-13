library(snow)

n <- 2e7
set.seed(2013)
df <- data.frame(id = sample(20, n, replace = TRUE), x = rnorm(n), y = runif(n), z = rpois(n, 1))

sst <- proc.time()
df_test <- data.frame(lapply(split(df[-1], df[1]), colMeans))
set <- proc.time()-sst
rm(df_test)

mst <- proc.time()
cl <- makeCluster(2, type = "SOCK")
df_test <- data.frame(parLapply(cl, split(df[-1], df[1]), colMeans))
stopCluster(cl)
met <- proc.time()-mst
rm(df_test)

cat("Single core\n")
print(set)

cat("Multi core\n")
print(met)