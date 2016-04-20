#! /usr/bin/Rscript

######################################################################
## This script creates the general dataset of presidencia
######################################################################


###################################
## Libraries
###################################
suppressPackageStartupMessages(library(stringr))
suppressPackageStartupMessages(library(RGA))
suppressPackageStartupMessages(library(plyr))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(data.table))
suppressPackageStartupMessages(library(RCurl))
suppressPackageStartupMessages(library(RJSONIO))
suppressPackageStartupMessages(library(RGoogleAnalytics))

###################################
## Read data
###################################
mat    <- read.csv("MAT.csv",
                  stringsAsFactors = FALSE)
invent <- mat[str_detect(mat$conj,
                        "(I|i)nventario (I|i)nstitucional de (D|d)atos .*"),
               c(2, 6)]
plans <- mat[str_detect(mat$conj,
                       "(P|p)lan de (A|a)pertura (I|i)nstitucional .*"),
             c(2, 6)]

###################################
## Filter data
###################################
all      <- mat
mat      <- dplyr::filter(mat, !is.na(slug))
mat.dc   <- data.table(mat)
mat.conj <- data.table(all)

###################################
## N rec, conj
###################################
rec    <- mat.dc[, .N, by = "slug"]
conj   <- mat.dc[, plyr::count(conj), by = "slug"]
conj.f <- conj[, .N, by = "slug"]
all_conj  <- mat.conj[, plyr::count(conj), by = "slug"]
all_conj.f <- all_conj[, .N, by = "slug"]

###################################
## fecha
###################################
dates <- mat.dc[, max(rec_fecha), by = "slug"]

###################################
## Put it all together
###################################
entities            <- data.frame(apply(
    mat[, c(1, 2)],
    2,
    unique))
entities$tiene_inv  <- entities$slug %in% invent$slug
entities$tiene_plan <- entities$slug %in% plans$slug
ent_rec             <- merge(entities, rec, by = "slug")
ent_rec_conj        <- merge(ent_rec, conj.f, by = "slug")
names(ent_rec_conj) <- c("slug",
                        "dep",
                        "tiene_inventario",
                        "tiene_plan",
                        "recursos",
                        "conjuntos")
ent_rec_conj <- merge(ent_rec_conj, dates, by = "slug")
names(ent_rec_conj) <- c("slug",
                        "dep",
                        "tiene_inventario",
                        "tiene_plan",
                        "recursos",
                        "conjuntos",
                        "fecha")
ent_rec_conj$fecha <- as.Date(ent_rec_conj$fecha)
write.csv(ent_rec_conj, "dirty_adela.csv", row.names = FALSE)

###################################
## Refinements
###################################
ent_rec_conj$tiene_inventario[
    ent_rec_conj$tiene_inventario == TRUE
] <-"Si"
ent_rec_conj$tiene_inventario[
    ent_rec_conj$tiene_inventario == FALSE
] <- "No"
ent_rec_conj$tiene_plan[
    ent_rec_conj$tiene_plan == TRUE] <- "Si"
ent_rec_conj$tiene_plan[
    ent_rec_conj$tiene_plan == FALSE] <- "No"

final_data <- ent_rec_conj
final_data <- final_data[,-1]
final_data[,c(4,5)] <- final_data[,c(5,4)]
names(final_data) <- c("Nombre de la dependencia",
                      "¿Cuenta con Inventario de Datos?",
                      "¿Cuenta con Plan de Apertura?",
                      "Número de conjuntos de datos publicados",
                      "Número de recursos de datos publicados",
                      "Última fecha de actualización")

###################################
## Agregar datos sin recursos
###################################
new_data  <- data.frame("dep"   = c("AGN","CENSIDA","PF"),
                       "inv"   = rep("Si", 3),
                       "plan"  = rep("Si", 3),
                       "conj"  = rep(0,3),
                       "rec"   = rep(0,3),
                       "fecha" = rep(NA, 3))
names(new_data) <- names(final_data)
final_data      <- rbind(final_data, new_data)
write.csv(final_data,
          "dataset_presidencia.csv",
          row.names = FALSE)

###################################
## Google Analytics
###################################
## Profiles
##        id              name
## 1 88225771 All Web Site Data
## 2 91319629 All Web Site Data DESCARGAS 2014/10/01 - today
## 3 91863615 All Web Site Data VISITAS   2014/10/01 - today

## token <- Auth("497323299158-elgh4c5t1o57dd8qfvakr99ge6d2qge3.apps.googleusercontent.com",
##              "I7wDgHvwULRHkB7bjt_JrrJt")
## save(token, file="oauth_token")
## load("oauth_token")
## Validate Token
## ValidateToken(token)
authorize()
## -----------------------------
## Queries
## -----------------------------
yesterday <- today() - 1

## Downloads
id <- 91319629
query.downloads <- get_ga(id, start.date   = "2014-10-01",
                   end.date    = yesterday,
                   dimensions  = "ga:date, ga:pagePath, ga:hour, ga:medium",
                   metrics     = "ga:sessions",
                   sort        = "-ga:date")
analytic_downloads <- sum(query.downloads$sessions)

## top 5
filter_resources <- data.table(query.downloads[str_detect(query.downloads$pagePath, "resourc"), ])
top <- filter_resources[,sum(sessions), by = "pagePath"]
head(top[order(top$V1, decreasing = TRUE), ])

## Resource downloads
## resource_download <- query.downloads[,c(2,5)] %>%
   ## filter(str_detect(pagePath, "/resource/"))
## filter_rec <- laply(resource_download$pagePath, function(t) t <- str_split(t, "/resource/")[[1]][2])
## rec_id <- laply(filter_rec, function(t) t <- str_extract(t, "([[:alnum:]]{4,}-?){4,}[[:alnum:]]{5,}"))

## Count downloads
## resource_download$rec_id <- rec_id
## rec_table      <- data.table(resource_download)
## download_count <- rec_table[,sum(sessions), by = "rec_id"]
## names(download_count) <- c("rec_id", "n_downloads")
## full_mat              <- merge(mat, download_count, by = "rec_id", all.x = TRUE)

## Visites
id <- 91863615
query.visits <- get_ga(id, start.date   = "2014-10-01",
                      end.date    = yesterday,
                      dimensions  = "ga:date, ga:pagePath, ga:hour, ga:medium",
                      metrics     = "ga:sessions,ga:pageviews,ga:bounces",
                      sort        = "-ga:date")
analytic_visits  <- sum(query.visits$sessions)
analytic_bounces <- sum(query.visits$bounces)



###################################
## Add data
###################################
conj.dep.hack <- RJSONIO::fromJSON(getURL("http://catalogo.datos.gob.mx/api/3/action/package_search?q=&rows=10&sort=dcat_modified+desc&start=0"))$result[[1]]
conj.non.dep  <- conj.dep.hack - length(unique(all$conj[is.na(all$slug)]))
data_summ <- data.frame("Concepto" = c(
                           "Recursos de datos publicados",
                           "Conjuntos de datos total publicados",
                           "Conjuntos de datos de dependencias publicados",
                           "Dependencias publicando",
                           "Dependencias con Inventario",
                           "Dependencias con Plan",
                           "Visitas",
                           "Descargas",
                           "Periodo"
                       ), "Total" = c(
                              nrow(all),
                              conj.dep.hack,
                              conj.non.dep,
                              nrow(final_data) - 3,
                              sum(ent_rec_conj$tiene_inventario == "Si"),
                              sum(ent_rec_conj$tiene_plan == "Si"),
                              analytic_visits,
                              analytic_downloads,
                              paste("2014-10-10", yesterday, sep = " / ")
                          ))
write.csv(data_summ,
          "datosgob_resum.csv",
          row.names = FALSE)

###################################
## Public data
###################################
public_data <- all[,c(1, 2, 3, 4, 5)]
public_data$clave <- paste0(public_data$dep,
                           public_data$conj)
public_data <- filter(public_data,
                     !duplicated(clave))
public_data <- public_data[order(public_data$slug),]
write.csv(public_data, "public_data.csv",
          row.names = FALSE)

###################################
## Eraser
###################################
system("rm  filter_data.csv")
