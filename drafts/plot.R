
#install.packages('arules')
#install.packages('arulesViz')
#install.packages('visNetwork')
#install.packages('igraph')



library(arules)
library(arulesViz)
library(visNetwork)
library(igraph)

data_matrix = read.table('F:/myproject/output/data.txt', head = FALSE,sep = ',',fill = TRUE); #其中head=TRUE表示含有属性的标题，head=FALSE表示不含属性的标题
print(data_matrix)
rules <- apriori(data_matrix, parameter=list(support=0.05, confidence=0.6))


subrules2 <- head(sort(rules, by="lift"), 10)
ig <- plot( subrules2, method="graph", control=list(type="items") )

# saveAsGraph seems to render bad DOT for this case
tf <- tempfile( )
saveAsGraph( subrules2, file = tf, format = "dot" )
# clean up temp file if desired
#unlink(tf)

# let's bypass saveAsGraph and just use our igraph
ig_df <- get.data.frame( ig, what = "both" )
visNetwork(
  nodes = data.frame(
    id = ig_df$vertices$name
    ,value = ig_df$vertices$support # could change to lift or confidence
    ,title = ifelse(ig_df$vertices$label == "",ig_df$vertices$name, ig_df$vertices$label)
    ,ig_df$vertices
  )
  , edges = ig_df$edges
) %>%
  visEdges( style = "arrow" ) %>%
  visOptions( highlightNearest = T )
# 上面的缩进不能动

