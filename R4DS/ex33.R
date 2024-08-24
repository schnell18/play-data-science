# Q2:
flights |>
  select(dep_time, dep_delay, arr_time, arr_delay)
flights |>
  select(ends_with("_time") | ends_with("_delay")) |>
  select(!starts_with("sched_") & !starts_with("air_"))


# Q3: ignored
flights |> select(dep_time, dep_time)

# Q4:
vars <- c("year", "month", "day", "dep_delay", "arr_delay")
flights |> select(!any_of(vars))

# Q5:
flights |> select(contains("TIME", ignore.case=F))

# Q6:
flights |>
  rename(air_time_min=air_time) |>
  relocate(air_time_min, .before = 1)

# Q7: Only the tailnum is retained when the tibble is fed to the arrange() 

