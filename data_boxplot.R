#Input data
setwd('/Users/dominicleung/OneDrive/Documents/FINA4390/industry/')

###Cleaned data
d2 = read.csv("4390_7th_cleaned.csv")
name = colnames(d2)

col_len = dim(d2)[2]
par(mfrow = c(1,4))
for (i in 3:col_len){
  boxplot(d2[i], main =name[i])
}



