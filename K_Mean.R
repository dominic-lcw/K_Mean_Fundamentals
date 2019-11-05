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
source <- "/Users/dominicleung/Documents/4390Local/Market_Related/Training/mr1.csv"
d <- read.csv(source)
head(d)
###----------------------------------------
### Box plot for all columns
###----------------------------------------
name = colnames(d);name
col_len = dim(d)[2]
row_len = dim(d)[1];row_len

par(mfrow = c(1,4))
for (i in 3:col_len){
  boxplot(d[i], main =name[i])
}

###----------------------------------------
### Train the best KM model
###----------------------------------------
bestk <- function(d1){
  n = dim(d1)[1]
  min = floor(n/3)
  while(min > 200){
    for (i in 3:20){
      set.seed(8)
      km <- kmeans(d1, i, nstart = 50, iter.max = 100, algorithm="MacQueen")
      if (sort(table(km$cluster), decreasing = TRUE)[2]>min){
        km.out <- km; cat("K=",i)
        table(km.out$cluster) #Evaluate Distribution
        return(km.out)
      }
    }
    min = min - 100
  }
  cat("FAILED")
  return(NULL)
}

scattermatrix <- function(km.r, df){
  group = as.numeric(names(sort(table(km.r$cluster), decreasing = TRUE)))
  max_index = group[1:4]

  largest = cbind(df, km.r$cluster)
  in_set = subset(largest, (km.r$cluster %in% max_index))
  out_set = subset(largest, !(km.r$cluster %in% max_index))
  out_set['km.r$cluster'] = 'black'

  colour = c('red', 'blue','green','lightblue','purple', 'orange')  
  for (i in 1:length(max_index)){
    in_set[in_set['km.r$cluster']== max_index[i],]['km.r$cluster'] = colour[i]
  }
  total_set = rbind(out_set, in_set)
  n = as.numeric(dim(total_set)[2])
  plot(total_set[1:(n-1)], col = total_set[,n])
}

scattermatrix(km.r, d1)

###----------------------------------------
### Decide multiple columns that are representable
###----------------------------------------
sel = c(1,2,4)
selected = d1[sel]
x1 <- data.frame(selected)
par(mfrow = c(1,1))
plot(x1, col = km.r$cluster, main = "before")
legend(x = 1.5,y = 2, legend = c('1','2','3','4','5','6','7','8','9'),lwd = 1, col = c(1:9), cex = 0.4)

library("nnet")
p0 <- data.frame(selected, km.r$cluster) 
mn1 = multinom(km.r.cluster ~ ., data = p0)

pred <- predict(mn1)
plot(x1, col = pred, main = "after")

table(pred) #Evaluate transformed result

###----------------------------------------
### Output the result
###----------------------------------------
output <- data.frame(d[1], d[2], selected, pred)
#output <- data.frame(d[1], d[2], selected, km.r$cluster)
head(output)
write.csv(output, file = "/Users/dominicleung/Documents/4390Local/Operating_Profitability/op2_pred.csv", row.names = FALSE)

###----------------------------------------
### Validation Dataset Result
###----------------------------------------
source <- "/Users/dominicleung/Documents/4390Local/Operating_Profitability/Validation/op2.csv"
val <- read.csv(source)
len <-dim(val)[2]
v1 <- val[c(3:len)][sel]
v_pred <-predict(mn1, v1)
table(v_pred)
output2 <- data.frame(val[1], val[2], v1, v_pred)
write.csv(output2, file = "/Users/dominicleung/Documents/4390Local/Operating_Profitability/op2_val.csv", row.names = FALSE)
