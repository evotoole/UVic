source("get_key.R")
library(httr)
library(jsonlite)

chat_gpt <- function(prompt, model = "gpt-3.5-turbo") {
  api_key <- get_openai_key()
  
  res <- httr::POST(
    url = "https://api.openai.com/v1/chat/completions",
    httr::add_headers(
      Authorization = paste("Bearer", api_key),
      `Content-Type` = "application/json"
    ),
    body = jsonlite::toJSON(list(
      model = model,
      messages = list(
        list(role = "user", content = prompt)
      )
    ), auto_unbox = TRUE)
  )
  
  # Check for API success
  status <- httr::status_code(res)
  if (status != 200) {
    cat("❌ API Error! Status:", status, "\n")
    cat("Message:\n", httr::content(res, as = "text"), "\n")
    return(NULL)
  }
  
  # Get and parse the API response
  response_content <- httr::content(res, as = "text", encoding = "UTF-8")
  parsed <- jsonlite::fromJSON(response_content)
  
  # Return only the content of the message (the final output)
  return(parsed$choices$message$content[1])
}



