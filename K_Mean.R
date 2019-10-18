#Input data
set.seed(888)
setwd('/Users/dominicleung/OneDrive/Documents/FINA4390/industry/')
source <- "4390_7th_cleaned.csv"
d <- read.csv(source)
d1 <- d[c(3:10)]
head(d1)
d1

km <- kmeans(d1, 3)
plot(d1, col = km$cluster)

sum(km$cluster==1)
sum(km$cluster==2)
sum(km$cluster==3)

x <- data.frame(d1[1], d1[8])
par(mfrow = c(1,1))
plot(x, col = km$cluster)

library("nnet")
reg_data <- data.frame(d1[1], d1[8], km$cluster) 
mn1 = multinom(km.cluster ~ ., data = reg_data)

pred <- predict(mn1)
plot(x, col = pred)

output <- data.frame(d[1], d[2], d1[1], d1[8], pred)
head(output)
write.csv(output, file = "INV_PE.csv", row.names = FALSE)
head(output)
d[1]
