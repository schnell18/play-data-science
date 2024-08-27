library(rgl)

x <- 1:5/10
y <- 1:5
z <- x %o% y
z <- z + .2*z*runif(25) - .1*z

rgl::open3d()
persp3d(x, y, z, col="skyblue")
rgl.snapshot("rgl.png")
#rgl.postscript("rgl.pdf", fmt="pdf")
rgl::close3d()
