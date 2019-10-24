###----------------------------------------
### Input Raw Data
###----------------------------------------
source <- "/Users/dominicleung/Documents/4390Local/Business_Financial_Risk.csv"
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
source <- "/Users/dominicleung/Documents/4390Local/Training/TBusiness_Financial_Risk.csv"
d <- read.csv(source)
###----------------------------------------
### Box plot for all columns
###----------------------------------------
name = colnames(d)
col_len = dim(d)[2]
row_len = dim(d)[1]
par(mfrow = c(1,4))

for (i in 3:col_len){
  boxplot(d[i], main =name[i])
}

###----------------------------------------
### Train the best KM model
###----------------------------------------
bestk <- function(d1, min){
  for (i in 3:10){
    set.seed(8)
    km <- kmeans(d1, i, nstart = 50)
    if (sort(table(km$cluster), decreasing = TRUE)[2]>min){
      km.out <- km; cat("K=",i)
      break
    }
  }
  km.out
}

d1 = d[3:col_len]
km.r <- bestk(d1,200)
plot(d1, col = km.r$cluster)
table(km.r$cluster) #Evaluate Distribution
legend(x = 1.5,y = 2, legend = c('1','2','3','4','5','6','7','8'),lwd = 1, col = c(1:8), cex = 0.4)

###----------------------------------------
### Decide multiple columns that are representable
###----------------------------------------
x1 <- data.frame(d1[c(2,4)])
par(mfrow = c(1,1))
plot(x1, col = km.r$cluster, main = "before")


library("nnet")
p0 <- data.frame(d1[c(2,4)], km.r$cluster) 
mn1 = multinom(km.r.cluster ~ ., data = p0)

pred <- predict(mn1)
plot(x1, col = pred, main = "after")

table(pred) #Evaluate transformed result

###----------------------------------------
### Output the result
###----------------------------------------
output <- data.frame(d[1], d[2], d1[c(2,4)], pred)
head(output)
write.csv(output, file = "BFR_2columns.csv", row.names = FALSE)

###----------------------------------------
### Validation Dataset Result
###----------------------------------------
source <- "/Users/dominicleung/Documents/4390Local/Validation/VBusiness_Financial_Risk.csv"
val <- read.csv(source)
len <-dim(val)[2]
v1 <- val[c(3:len)][c(2,4)]
v_pred <-predict(mn1, v1)
table(v_pred)
write.csv(output, file = "/Users/dominicleung/Documents/4390Local/Validation/BFR_val_2columns.csv")