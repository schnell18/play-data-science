# Plot penguins bill length vs bill depth:

# Q1
ggplot(penguins, aes(y=species)) + 
  geom_bar(binwidth=200)

# Q2
ggplot(penguins, aes(x=species)) + 
  geom_bar(color="red")

ggplot(penguins, aes(x=species)) + 
  geom_bar(fill="red")

# Q3
ggplot(penguins, aes(x=body_mass_g)) + 
  geom_histogram(bins=25)

# Q4
ggplot(diamonds, aes(x=carat)) + 
  geom_histogram(binwidth=0.4)

