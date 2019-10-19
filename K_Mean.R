#Input data
setwd('/Users/dominicleung/OneDrive/Documents/FINA4390/industry/')
source <- "4390_7th_cleaned.csv"
d <- read.csv(source)
d1 <- d[c(3:10)]

###----------------------------------------
### Box plot for all columns
###----------------------------------------
name = colnames(d1)
col_len = dim(d1)[2]
par(mfrow = c(1,4))
for (i in 3:col_len){
  boxplot(d1[i], main =name[i])
}

###----------------------------------------
### Train the best KM model
###----------------------------------------
bestk <- function(d1){
    for (i in 3:10){
    	set.seed(8)
        km <- kmeans(d1, i, nstart = 50)
        if (sort(table(km$cluster), decreasing = TRUE)[2]>100){
            km.out <- km; cat("K=",i)
            break
        }
    }
    km.out
}

km.r <- bestk(d1)
plot(d1, col = km.r$cluster)

###----------------------------------------
### Decide multiple columns that are representable
###----------------------------------------
x1 <- data.frame(d1[1], d1[8])
x2 <- data.frame(d1[1], d1[4])

par(mfrow = c(1,2))
plot(x1, col = km.r$cluster)
plot(x2, col = km.r$cluster)
legend(x = 1.5,y = 2, legend = c('1','2','3','4','5','6','7','8'),lwd = 1, col = c(1:8), cex = 0.4)

km.r$cluster
table(km.r$cluster) #Evaluate Distribution

library("nnet")
p0 <- data.frame(d1[c(1,4,8)], km.r$cluster) 
mn1 = multinom(km.r.cluster ~ ., data = p0)

pred <- predict(mn1)
par(mfrow = c(1,2))
plot(x1, col = pred, main = "before")
plot(x1, col = km.r$cluster, main = "after")
plot(x2, col = km.r$cluster, main = "before")
plot(x2, col = pred, main = "after")
table(pred) #Evaluate transformed result

###----------------------------------------
### Output the result
###----------------------------------------
output <- data.frame(d[1], d[2], d1[c(1,4,8)], pred)
head(output)
write.csv(output, file = "INV_NBD_PE.csv", row.names = FALSE)
