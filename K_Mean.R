###----------------------------------------
### Input Raw Data
###----------------------------------------
source <- "/Users/dominicleung/Documents/4390Local/Raw_Data/Business_Financial_Risk.csv"
raw <- read.csv(source)
col_len = dim(raw)[2]

###----------------------------------------
### Box plot for raw data
###----------------------------------------
name = colnames(raw)
par(mfrow = c(1,4))
for (i in 3:col_len){
  cl <- raw[!raw[,i]=='#N/A N/A',]
  boxplot(as.numeric(as.character(cl[,i])), main = name[i])
}
###----------------------------------------
### Input Cleaned Data
###----------------------------------------
source <- "/Users/dominicleung/Documents/4390Local/Business_Financial_Risk/Training/bf2.csv"
d <- read.csv(source)
head(d)
###----------------------------------------
### Box plot for all columns
###----------------------------------------
name = colnames(d);name
col_len = dim(d)[2];col_len
row_len = dim(d)[1];row_len

par(mfrow = c(1,4))
for (i in 3:col_len){
  boxplot(d[i], main =name[i])
}
###----------------------------------------
### Train the best KM model
###----------------------------------------
setwd("~/Documents/Repository/K_Mean_Fundamentals") #Set directory for the file
source("km_func.R")
d1 = d[3:col_len]
km.r = bestk(d1)
table(km.r$cluster)
d2 = scattermatrix(km.r, d, 4)

head(d2)
cluster = transform(d2)
table(cluster)
d2['km.r$cluster']<- NULL

###----------------------------------------
### Decide multiple columns that are representable
###----------------------------------------
sel = c(1:3)+2
head(d2[sel])
selected <- d2[sel]
selected <- data.frame(selected);head(selected)

library("nnet")
p0 <- data.frame(selected, cluster);head(p0)
mn1 = multinom(cluster ~ ., data = p0)
# (as.numeric(cluster) - as.numeric(pred))!=0
pred <- predict(mn1)
table(pred, cluster) #Evaluate transformed result
plot(selected, col = pred, main = "after")
# z <-summary(mn1)$coefficients/summary(mn1)$standard.errors;z
# p <- (1 - pnorm(abs(z), 0, 1))*2;p

###----------------------------------------
### Output the result
###----------------------------------------
output <- data.frame(d2[1], d2[2], selected, pred)
head(output)

write.csv(output, file = "/Users/dominicleung/Documents/4390Local/Business_Financial_Risk/bf6_pred.csv", row.names = FALSE)
###----------------------------------------
### Validation Dataset Result
###----------------------------------------
source <- "/Users/dominicleung/Documents/4390Local/Business_Financial_Risk/Validation/bf4.csv"
val <- read.csv(source)
len <-dim(val)[2]
v1 <- val[sel]
head(v1)
pred <-predict(mn1, v1)
table(pred)
output2 <- data.frame(val[1], val[2], v1, pred)
write.csv(output2, file = "/Users/dominicleung/Documents/4390Local/Business_Financial_Risk/bf4_val.csv", row.names = FALSE)

###----------------------------------------
### Random Forest
###----------------------------------------

library("rpart")
p0 <- data.frame(d1, cluster);head(p0)
tree <- rpart(cluster ~ ., data = p0, method = 'class')
plot(tree, asp = 3)
text(tree, use.n = T, cex = 0.8)
pred = predict(tree)
pred = colnames(pred)[max.col(pred)]

library(caret)
library(rattle)
library(randomForest)
library(ggplot2)
library(ggthemes)
library(dplyr)

model_rf <- randomForest(cluster ~ ., data = p0)
model_rf



