library(readxl)
patients <- read_excel("/home/resources/Пациенты.xlsx")
print("Файл 'Пациенты' прочитан!")

patients$Пол <- tolower(patients$Пол)
patients$Пол <- factor(patients$Пол, levels = c("м", "ж"))

patients$возраст_группа <- cut(patients$Возраст, 
                               breaks = c(30, 60, 90),
                               labels = c("Молодые", "Старшие"),
                               include.lowest = TRUE)
str(patients)

mean_and_std <- function(x) {
  mean = mean(x)
  sd = sd(x)
  c(mean, sd)
}

final_result <- aggregate(гемоглобин ~ возраст_группа, data = patients, FUN = mean_and_std)
final_result <- do.call(data.frame, final_result)
names(final_result) <- c("Возрастная группа", "Среднее", "СКО")

write.csv(final_result, "/home/results/анализ_гемоглобина.csv")
print(paste("Файл сохранен как", "/home/results/анализ_гемоглобина.csv"))