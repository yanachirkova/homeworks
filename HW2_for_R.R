library(readxl)
patients <- read_excel("./common/Пациенты.xlsx")
View(patients)

str(patients$Возраст)
str(patients$глюкоза)

patients$Пол <- tolower(patients$Пол)
patients$Пол <- factor(patients$Пол, levels = c("м", "ж"))
levels(patients$Пол)

patients$возраст_группа <- cut(patients$Возраст, 
                               breaks = c(30, 60, 90),
                               labels = c("Молодые", "Старшие"),
                               include.lowest = TRUE)

patients[patients$Возраст > 75,]
summary(patients$лейкоциты)
summary(patients$глюкоза)
head(patients$лейкоциты)
head(patients$глюкоза)

aggregate(глюкоза ~ Пол, data = patients, FUN = mean)


stats <- function(x) {
  mean = mean(x)
  sd = sd(x)
  n = length(x)
  c(mean, sd, n)
}

result <- aggregate(глюкоза ~ Пол, data = patients, FUN = stats)
result <- do.call(data.frame, result)
names(result) <- c("Пол", "Среднее", "СКО", "Количество")
result

boxplot(глюкоза~Пол, data=patients, main="Ящик с усами")

# H0 - средний уровень лейкоцитов у мужчин и женщин не отличается
# H1 - в среднем уровне лейкоцитов у мужчин и женщин есть статистически значимые
# отличичя
t.test(лейкоциты ~ Пол, data = patients)
# p-value = 0.09424 что больше 0.05 поэтому нет статистических оснований 
# отвергнуть нулевую гипотезу

patients_na <- patients
patients_na$глюкоза[c(3, 15, 45)] <- NA

sum(is.na(patients_na))

which(is.na(patients_na$глюкоза))

patients_no_na <- na.omit(patients_na)
dim(patients_no_na)
dim(patients)

patients_na$глюкоза[is.na(patients_na$глюкоза)] <- median(patients_na$глюкоза, na.rm = TRUE)

patients_na$глюкоза[c(3, 15, 45)] <- NA
aggregate(лейкоциты ~ Пол, data = patients_na, FUN = mean, na.rm = TRUE)
aggregate(лейкоциты ~ Пол, data = patients_no_na, FUN = mean, na.rm = TRUE)
View(patients_na)
# Результат среднего отличается только у женщин, так как пропущенные значения 
# были добавлены только у них

mean_and_std <- function(x) {
  mean = mean(x)
  sd = sd(x)
  c(mean, sd)
}

final_result <- aggregate(гемоглобин ~ возраст_группа, data = patients, FUN = mean_and_std)
final_result <- do.call(data.frame, final_result)
names(final_result) <- c("Возрастная группа", "Среднее", "СКО")

write.csv(final_result, "./homeworks/анализ_гемоглобина.csv")

