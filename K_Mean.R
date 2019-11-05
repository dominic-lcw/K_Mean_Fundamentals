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
source <- "/Users/dominicleung/Documents/4390Local/Market_Related/Training/mr6.csv"
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
bestk <- function(d1){
  n = dim(d1)[1]
  min = floor(n/2)
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

  colour = c('red', 'blue','green','lightblue')  
  for (i in 1:length(max_index)){
    in_set[in_set['km.r$cluster']== max_index[i],]['km.r$cluster'] = colour[i]
  }
  total_set = rbind(out_set, in_set)
  n = as.numeric(dim(total_set)[2])
  plot(total_set[3:(n-1)], col = total_set[,n])
  return(total_set)
}
transform <- function(td){
  td[td['km.r$cluster']=='red',]['km.r$cluster'] = 1
  td[td['km.r$cluster']=='blue',]['km.r$cluster'] = 2
  td[td['km.r$cluster']=='green',]['km.r$cluster'] = 3
  td[td['km.r$cluster']=='lightblue',]['km.r$cluster'] = 4
  td[td['km.r$cluster']=='black',]['km.r$cluster'] = 5
  return(td[,as.numeric(dim(td)[2])])
}

d1 = d[3:col_len]
km.r = bestk(d1)
table(km.r$cluster)
d2 = scattermatrix(km.r, d)

head(d2)
cluster = transform(d2)
table(cluster)
d2['km.r$cluster']<- NULL

###----------------------------------------
### Decide multiple columns that are representable
###----------------------------------------
sel = c(1,2,4,6,7)+2

head(d2[sel])

selected <- d2[sel]
selected <- data.frame(selected)
par(mfrow = c(1,1))
plot(selected, col = cluster, main = "before")

library("nnet")
p0 <- data.frame(selected, cluster);head(p0)
mn1 = multinom(cluster ~ ., data = p0)

pred <- predict(mn1)
plot(selected, col = pred, main = "after")
table(pred) #Evaluate transformed result

###----------------------------------------
### Output the result
###----------------------------------------
output <- data.frame(d2[1], d2[2], selected, pred)
#output <- data.frame(d[1], d[2], selected, km.r$cluster)
head(output)
write.csv(output, file = "/Users/dominicleung/Documents/4390Local/Market_Related/mr6_pred.csv", row.names = FALSE)
###----------------------------------------
### Validation Dataset Result
###----------------------------------------
source <- "/Users/dominicleung/Documents/4390Local/Market_Related/Validation/mr6.csv"
val <- read.csv(source)
len <-dim(val)[2]
v1 <- val[sel]
head(v1)
v_pred <-predict(mn1, v1)
table(v_pred)
output2 <- data.frame(val[1], val[2], v1, v_pred)
write.csv(output2, file = "/Users/dominicleung/Documents/4390Local/Market_Related/mr6_val.csv", row.names = FALSE)


