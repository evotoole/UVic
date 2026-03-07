get_openai_key <- function() {
  system("security find-generic-password -a openai_user -s openai_api_key -w", intern = TRUE)
}