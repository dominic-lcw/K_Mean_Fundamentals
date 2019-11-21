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
scattermatrix <- function(km.r, df, max){
  group = as.numeric(names(sort(table(km.r$cluster), decreasing = TRUE)))
  max_index = group[1:max]

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