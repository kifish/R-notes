library(data.table)
library(plyr)
library(ggmap)
library(ggplot2)
library(ggiraph)
library(maptools)



setwd('F:/R-notes/plot_map/')
my_map<-readShapePoly("bou2_4p.shp")

x <- my_map@data
xs <- data.frame(x,id=seq(0:924)-1)

china_map = fortify(my_map)
china_map_data <- join(china_map, xs, type = "full") 
GOD_regions_df = data.frame(NAME = c("北京市",'江苏省'),Number = c(1,2))

# colnames(GOD_regions_df) = c("NAME", "Year", "Number")

china_data <- join(china_map_data, GOD_regions_df, type="full")

ggplot(china_data, aes(x=long, y=lat, group = group, fill=Number)) +
  geom_polygon(aes(fill = Number, group = group, tooltip = NAME, data_id = long)) +  geom_path(colour = "grey40") +
  scale_fill_gradient(low = "white", high = "red") +
  coord_map("polyconic") + theme_minimal() + labs(title="2013年肝癌发病率统计")+
  theme(panel.grid = element_blank(), panel.background = element_blank(), axis.line = element_blank(), 
        axis.text = element_blank(), axis.ticks = element_blank(), axis.title = element_blank(),plot.title = element_text(hjust = 0.5), 
        legend.position = c(0.1,0.3)) + ggsave("./test1.png",width=8, height=8,dpi=300)
