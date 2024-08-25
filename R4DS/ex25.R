# Q1
# my_variable <- 10
# my_varıable ı is not i, i w/o dot is not i


# Q2

# libary(todyverse)
# 
# ggplot(dTA = mpg) + 
#   geom_point(maping = aes(x = displ y = hwy)) +
#   geom_smooth(method = "lm)

# fix

ggplot(data = mpg, mapping = aes(x = displ, y = hwy)) + 
  geom_point() +
  geom_smooth(method = "lm")

# Q3
# Option + Shift + K is to popup the keyboard shortcut
# From menu "Tools->Keyboard Shortcuts Help"

# Q4
# the first plot which shows car count by class
# The ggsave function specifies the first plot, my_bar_plot, to save
