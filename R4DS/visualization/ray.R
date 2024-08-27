library(rayshader)
library(ggplot2)
library(tidyverse)

#Data from Social Security administration
death = read_csv("https://www.tylermw.com/data/death.csv", skip = 1)
meltdeath = reshape2::melt(death, id.vars = "Year")

meltdeath$age = as.numeric(meltdeath$variable)

deathgg = ggplot(meltdeath) +
  geom_raster(aes(x=Year,y=age,fill=value)) +
  scale_x_continuous("Year",expand=c(0,0),breaks=seq(1900,2010,10)) +
  scale_y_continuous("Age",expand=c(0,0),breaks=seq(0,100,10),limits=c(0,100)) +
  scale_fill_viridis_b("Death\nProbability\nPer Year",trans = "log10",breaks=c(1,0.1,0.01,0.001,0.0001), labels = c("1","1/10","1/100","1/1000","1/10000")) +
  ggtitle("Death Probability vs Age and Year for the USA") +
  labs(caption = "Data Source: US Dept. of Social Security")

plot_gg(deathgg, multicore=TRUE,height=5,width=6,scale=500)



mtcars_gg = ggplot(mtcars) + 
  geom_point(aes(x=mpg,color=cyl,y=disp),size=2) +
  scale_color_continuous(limits=c(0,8)) +
  ggtitle("mtcars: Displacement vs mpg vs # of cylinders") +
  theme(title = element_text(size=8),
        text = element_text(size=12)) 

plot_gg(mtcars_gg, height=3, width=3.5, multicore=TRUE, pointcontract = 0.7, soliddepth=-200)
