# Q1:
flights |> filter(arr_delay >= 120)
flights |> filter(dest == "IAH" | dest == "HOU")
flights |> filter(carrier %in% c("UA", "AA", "DL"))
flights |> filter(month %in% c(7, 8, 9))
flights |> filter(arr_delay >= 120 & dep_delay == 0)
flights |> filter(dep_delay >= 60 & arr_delay <= 30)

# Q2:
flights |> arrange(desc(dep_delay))
flights |> arrange(dep_time)

# Q3:
flights |> arrange(arr_time-dep_time)

# Q4:
flights |>
  count(flight, year, month, day, sort=T) |>
  count(year, flight) |>
  filter(n >= 365)

# Q5:
flights |>
  distinct(flight, distance) |>
  arrange(desc(distance))
flights |>
  distinct(flight, distance) |>
  arrange(distance)

# Q6:
# Yes, filter() first then arrange() so that there are less records to sort
