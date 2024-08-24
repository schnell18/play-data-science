# Q1:
flights |>
  group_by(carrier) |>
  summarize(avg_delay = mean(dep_delay, na.rm = TRUE)) |>
  arrange(desc(avg_delay))

flights |>
  group_by(carrier, dest) |>
  summarize(avg_delay = mean(dep_delay, na.rm = TRUE), n=n()) |>
  arrange(desc(avg_delay))

# Q2:
flights |>
  group_by(flight) |>
  slice_max(dep_delay, n = 1)

# Q3:
flights |>
  filter(dep_delay > 0) |>
  mutate(hour = dep_time %/% 100) |>
  group_by(hour) |>
  summarize(n = n()) |>
  ggplot(aes(x=hour, y=n)) +
    geom_line()

