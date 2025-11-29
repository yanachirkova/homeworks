library(dplyr)
print(packageVersion("dplyr"))

sample_metadata <- read.csv("/home/data/sample_metadata.csv")
mass_spec_results <- read.csv("/home/data/mass_spec_results.csv")

# left anti join
left_anti_join_results <- anti_join(sample_metadata, mass_spec_results, by = "sample_id")
cat("left anti join\n")
cat("Было:", nrow(sample_metadata), "samples -> Стало:", nrow(left_anti_join_results), "samples\n")

# right anti join
right_anti_join_results <- anti_join(mass_spec_results, sample_metadata, by = "sample_id")
cat("right anti join\n")
cat("Было:", nrow(mass_spec_results), "samples -> Стало:", nrow(right_anti_join_results), "samples\n")

# anti outer join
anti_outer_join_results <- bind_rows(
  anti_join(sample_metadata, mass_spec_results, by = "sample_id"),
  anti_join(mass_spec_results, sample_metadata, by = "sample_id")
)
cat("anti outer join\n")
cat("Было:", nrow(mass_spec_results)+nrow(sample_metadata), "samples -> Стало:", nrow(anti_outer_join_results), "samples\n")

write.csv(left_anti_join_results, "/home/data/left_anti_join_results.csv", row.names = FALSE)
write.csv(right_anti_join_results, "/home/data/right_anti_join_results.csv", row.names = FALSE)
write.csv(anti_outer_join_results, "/home/data/anti_outer_join_results.csv", row.names = FALSE)
