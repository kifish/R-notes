library(maptools);
mapdata=readShapePoly('bou2_4p.shp')
plot(mapdata)

getColor=function(mapdata,provname,provcol,othercol){
  f = function(x,y) ifelse(x %in% y,which(y==x),0);
  colIndex=sapply(mapdata@data$NAME,f,provname);
  color_vec=c(othercol,provcol)[colIndex+1];
  return(color_vec);
}


provname=c("北京市","天津市","上海市","重庆市");
provcol=c("red","green","yellow","purple");
plot(mapdata,col=getColor(x,provname,provcol,"white"))
