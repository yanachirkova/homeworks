motifs2 <- matrix(c(
  "a", "C", "g", "G", "T", "A", "A", "t", "t", "C", "a", "G",
  "t", "G", "G", "G", "C", "A", "A", "T", "t", "C", "C", "a",
  "A", "C", "G", "t", "t", "A", "A", "t", "t", "C", "G", "G",
  "T", "G", "C", "G", "G", "G", "A", "t", "t", "C", "C", "C",
  "t", "C", "G", "a", "A", "A", "A", "t", "t", "C", "a", "G",
  "A", "C", "G", "G", "C", "G", "A", "a", "t", "T", "C", "C",
  "T", "C", "G", "t", "G", "A", "A", "t", "t", "a", "C", "G",
  "t", "C", "G", "G", "G", "A", "A", "t", "t", "C", "a", "C",
  "A", "G", "G", "G", "T", "A", "A", "t", "t", "C", "C", "G",
  "t", "C", "G", "G", "A", "A", "A", "a", "t", "C", "a", "C"
), nrow = 10, byrow = TRUE)

motifs2 <- apply(motifs2, 2, toupper)

count_matrix <- apply(motifs2, 2, function(col) table(factor(col, levels = c("A", "C", "G", "T"))))
count_matrix
profile <- apply(count_matrix, 2, function(x) x/sum(x))
profile


scoreMotifs <- function(motifs) {
  sum(apply(motifs, 2, function(col) length(col) - max(table(col))))
}

score <- scoreMotifs(motifs2)
score

getConsensus <- function(profile) {
  nucleotides <- c("A", "C", "G", "T")
  consensus <- apply(profile, 2, function(col) nucleotides[which.max(col)])
  paste(consensus, collapse = "")
}

consensus_string <- getConsensus(profile)
consensus_string

barplot(count_matrix[,1], col="skyblue", main="Частоты нуклеотидов в 1-м столбце")