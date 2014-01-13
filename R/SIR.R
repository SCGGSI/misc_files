## Main code for the SIR model example
library(deSolve) # Load the library to solve the ode

## Set initial parameter values
Bi <- 0.75
Bw <- 0.75
e <- 0.01
k <- 1/89193.18

data <- c(113, 60, 70, 140, 385, 2900, 4600, 5400, 5300, 6350, 5350, 4400, 3570, 2300, 1900, 2200, 1700, 1170, 830, 750, 770, 520, 550, 380)
tspan <- c(0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161)

## Combine parameters into a vector
params <- c(Bi, Bw, e, k)
names(params) <- c('Bi', 'Bw', 'e', 'k')

# Make a function for running the ODE
SIRode <- function(t, x, params){
  S <- x[1]
  I <- x[2]
  W <- x[3]
  R <- x[4]
  
  Bi <- params[1]
  Bw <- params[2]
  e <- params[3]
  k <- params[4]
  
  dS <- -Bi*S*I - Bw*S*W
  dI <- Bi*S*I + Bw*S*W - 0.25*I
  dW <- e*(I - W)
  dR <- 0.25*I
  
  output <- c(dS, dI, dW, dR)
  list(output)
}

# Set initial conditions
I0 <- data[1]*k
R0 <- 0
S0 <- (1-I0)
W0 <- 0

initCond <- c(S0, I0, W0, R0)

# Simulate the model using our initial parameter guesses
initSim <- ode(initCond, tspan, SIRode, params, method='ode45')

plot(tspan, initSim[,3]/k, type='l')
points(tspan, data)

# Make a function for optimzation of the parameters
LLode <- function(params){
  
  k <- params[4]
  
  I0 <- data[1]*k
  R0 <- 0
  S0 <- 1 - I0
  W0 <- 0
  
  initCond <- c(S0, I0, W0, R0)
  
  # Run the ODE
  odeOut <- ode(initCond, tspan, SIRode, params, method='ode45')
  
  # Measurement variable
  y <- odeOut[,3]/k
  
  diff <- (y - data)
  LL <- t(diff) %*% diff
  
  return(LL)
}

# Run the optimization procedure
MLresults <- optim(params, LLode, method='Nelder-Mead')
