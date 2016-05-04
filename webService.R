#! /usr/bin/Rscript

source("/home/luis/Documents/Presidencia/Rick/upload_adela/ultimate.R")

filter_data <- dplyr::select(all_data, one_of("dep", "slug", "conj","rec","rec_des","rec_url"))
filter_data <- dplyr::filter(filter_data, slug != "NA")
write.csv(filter_data, "./filter_data.csv", row.names = FALSE)
