library(httr)
library(jsonlite)
# задание 11
requestURL <- paste("https://www.ebi.ac.uk/proteins/api/features?accession=", 
                    paste('P04637', 'P05067', 'P10636', 'A0A023HJ61','A0A023HN28', 'A0A023I7F4', 'A0A023I7H2', 'A0A023I7H5', 'Q8WZ42', 'P00533', sep=","),
                    sep="")
ids <- c('P04637', 'P05067', 'P10636', 'A0A023HJ61','A0A023HN28', 'A0A023I7F4', 'A0A023I7H2', 'A0A023I7H5', 'Q8WZ42', 'P00533')
r <- GET(requestURL, accept("application/json"))

stop_for_status(r)

json <- toJSON(content(r))

data <- fromJSON(json)
lens <- nchar(data$sequence)
barplot(lens, width=0.5, names.arg=ids, las = 2, cex.names = 1)

# задание 14

get_protein_fasta <- function(accession_id, output_file = NULL) {
  # Формируем URL для FASTA формата
  url <- paste0("https://www.ebi.ac.uk/proteins/api/proteins/", accession_id)
  
  # Делаем запрос с заголовком для FASTA
  response <- GET(
    url,
    add_headers(Accept = "text/x-fasta")
  )
  
  # Проверяем статус ответа
  if (status_code(response) == 200) {
    fasta_content <- content(response, "text", encoding = "UTF-8")
    
    # Если указан файл для сохранения
    if (!is.null(output_file)) {
      writeLines(fasta_content, output_file)
    }
    
    return(fasta_content)
    
  } 
  else {
    stop("Ошибка API: ", status_code(response))
  }
}

# Использование
fasta_data <- get_protein_fasta("P01308", "insulin.fasta")
