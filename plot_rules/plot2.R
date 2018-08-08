# install.packages('arules')
# install.packages('igraph')
# install.packages('visNetwork')
# install.packages('arulesViz')



library(arules)
library(visNetwork)
library(igraph)
library(arulesViz)

setwd('F:/R-notes/drafts')
# rawdata=read.csv("data.csv") # qfs

#rawdata=read.csv("data_dfgd.csv")

rawdata=read.csv("data_fdzsy.csv")

#rawdata=read.csv("data_njgl.csv")

raw_list=sapply(as.character(rawdata[,1]),strsplit,split=",")
data_matrix <- raw_list
rules <- apriori(data_matrix, parameter=list(support=0.06, confidence=0.75))


subrules2 <- head(sort(rules, by="lift"), 10)
ig <- plot(subrules2, method="graph", control=list(type="items"))
# saveAsGraph seems to render bad DOT for this case
tf <- tempfile( )
saveAsGraph(subrules2, file = tf, format = "dot")
# clean up temp file if desired
#unlink(tf)

# let's bypass saveAsGraph and just use our igraph
ig_df <- get.data.frame( ig, what = "both" )
visNetwork(
  nodes = data.frame(
    id = ig_df$vertices$name
    ,value = ifelse(is.na(ig_df$vertices$confidence),0,ig_df$vertices$confidence) # could change to lift or confidence or support
    ,title = ifelse(ig_df$vertices$label == "",ig_df$vertices$name, ig_df$vertices$label)
    ,ig_df$vertices
  ),
  width = 1600,
  height = 1200,
  , edges = ig_df$edges
) %>%
  visEdges( arrows = "to" ) %>%
  visOptions( highlightNearest = T )




