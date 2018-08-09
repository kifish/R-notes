library(maptools);
mapdata=readShapePoly('bou2_4p.shp')
plot(mapdata)

getColor=function(mapdata,provname,provcol,othercol){
  f = function(x,y) ifelse(x %in% y,which(y==x),0);
  colIndex=sapply(mapdata@data$NAME,f,provname);
  color_vec=c(othercol,provcol)[colIndex+1];
  return(color_vec);
}


#midchina=c("河南省","山西省","湖北省","安徽省","湖南省","江西省");
#plot(mapdata,col=getColor(mapdata,midchina,rep('blue',6),'white'),border="white",xlab="",ylab="")