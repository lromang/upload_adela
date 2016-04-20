#! /usr/bin/python

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import codecs
import time
import string

##------------------------------------------------
## AOUTH
##------------------------------------------------

gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    ## Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    ## Refresh them if expired
    gauth.Refresh()
else:
    ## Initialize the saved creds
    gauth.Authorize()
## Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")
## Drive
drive = GoogleDrive(gauth)
## globals
printable = set(string.printable)
date  = time.strftime("%Y-%m-%dT%H:%M:%S")

##------------------------------------------------
## PUBLIC RESOURCES
##------------------------------------------------

## Read in data
mat = codecs.open("/home/luis/Documents/Presidencia/Rick/upload_adela/MAT.csv")
c   = mat.read()
## Encoding
c         = filter(lambda x: x in printable, c)
## Print result
print("URL Descarga, Nombre")

## -------------
## XLSX
## -------------
title = "recursos_" + date +".xlsx"
file1 = drive.CreateFile({'title': title,
                          'shareable':True,
                          'userPermission':[{'kind':'drive#permission',
                                             'type':'anyone',
                                             'value':'anyone',
                                             'role':'reader'}],
                          'mimeType':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                          "parents":[{"kind":"drive#fileLink","id":"0Bw1YBQEbBwzDWWVkNmd1Wm9zb1E"}]
                      })
file1.SetContentString(c)
file1.Upload()

## Print results
print("https://drive.google.com/uc?export=download&id=" +
      file1['id'] +
      ", Recursos de datos" +
      date +
      "_xlsx.xslx")

## -------------
## CSV
## -------------
title = "recursos_" + date +".csv"
file1 = drive.CreateFile({'title': title,
                          'shareable':True,
                          'userPermission':[{'kind':'drive#permission',
                                             'type':'anyone',
                                             'value':'anyone',
                                             'role':'reader'}],
                          'mimeType':'text/csv',
                          "parents":[{"kind":"drive#fileLink","id":"0Bw1YBQEbBwzDWWVkNmd1Wm9zb1E"}]
                      })
file1.SetContentString(c)
file1.Upload()

## Print results
print("https://drive.google.com/uc?export=download&id=" +
      file1['id'] +
      ", Recursos de datos" +
      date +
      "_csv.csv")

##------------------------------------------------
## CONJUNTOS PUBLIC
##------------------------------------------------

## Lectura de datos
public_data  = codecs.open("/home/luis/Documents/Presidencia/Rick/upload_adela/public_data.csv")
c            = public_data.read()
c            = filter(lambda x: x in printable, c)

## -------------
## CSV
## -------------
tittle = "conjunto_datos" + date +".csv"
file1 = drive.CreateFile({'title': tittle,
                          'shareable':True,
                          'userPermission':[{'kind':'drive#permission',
                                             'type':'anyone',
                                             'value':'anyone',
                                             'role':'reader'}],
                          'mimeType':'text/csv',
                          "parents":[{"kind":"drive#fileLink","id":"0Bw1YBQEbBwzDWWVkNmd1Wm9zb1E"}]
                      })
file1.SetContentString(c)
file1.Upload()

## Print results
print("https://drive.google.com/uc?export=download&id=" +
      file1['id'] +
      ", Conjuntos de datos" +
      date +
      "_csv.csv")


## -------------
## XLSX
## -------------
tittle = "conjunto_datos" + date +".xlsx"
file1 = drive.CreateFile({'title': tittle,
                          'shareable':True,
                          'userPermission':[{'kind':'drive#permission',
                                             'type':'anyone',
                                             'value':'anyone',
                                             'role':'reader'}],
                          'mimeType':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                          "parents":[{"kind":"drive#fileLink","id":"0Bw1YBQEbBwzDWWVkNmd1Wm9zb1E"}]
                      })
file1.SetContentString(c)
file1.Upload()

## Print results
print("https://drive.google.com/uc?export=download&id=" +
      file1['id'] +
      ", Conjuntos de datos" +
      date +
      "_xlsx.xlsx")

##------------------------------------------------
## ANALYTICS PUBLIC
##------------------------------------------------

## Lectura de datos
resumen = codecs.open("/home/luis/Documents/Presidencia/Rick/upload_adela/datosgob_resum.csv")
c       = resumen.read()
c       = filter(lambda x: x in printable, c)

## -------------
## CSV
## -------------
file2   = drive.CreateFile({'id':'0B5p8KkRjjG4HOHhwTHhwenBIUk0'})
content = file2.GetContentString()
file2.SetContentString(content.replace(content, c))
file2.Upload()

## Print results
print("https://drive.google.com/uc?export=download&id=" +
      file2['id'] +
      ", Feed de analytics DGM" +
      date +
      "_csv.csv")


## -------------
## XLSX
## -------------
tittle = "dgm_anlytics" + ".xlsx"
file2 = drive.CreateFile({'id':'0B5p8KkRjjG4HSE5qUmhrV3MtTk0'})
file2.SetContentString(c)
file2.Upload()

## Print results
print("https://drive.google.com/uc?export=download&id=" +
      file2['id'] +
      ", Feed de analytics DGM" +
      date +
      "_xlsx.xlsx")

##------------------------------------------------
## CONJUNTOS PUBLIC
##------------------------------------------------

## Lectura de datos
public_data  = codecs.open("/home/luis/Documents/Presidencia/Rick/atencion_ciudadana/201603.csv")
c            = public_data.read()
c            = filter(lambda x: x in printable, c)

## -------------
## CSV
## -------------
tittle = "atencion_ciudadana_datos" + date +".csv"
file1 = drive.CreateFile({'title': tittle,
                          'shareable':True,
                          'userPermission':[{'kind':'drive#permission',
                                             'type':'anyone',
                                             'value':'anyone',
                                             'role':'reader'}],
                          'mimeType':'text/csv',
                          "parents":[{"kind":"drive#fileLink","id":"0Bw1YBQEbBwzDWWVkNmd1Wm9zb1E"}]
                      })
file1.SetContentString(c)
file1.Upload()

## Print results
print("https://drive.google.com/uc?export=download&id=" +
      file1['id'] +
      ", Concentrado de peticiones al C. Presidente - " +
      date +
      "_csv.csv")


## -------------
## XLSX
## -------------
tittle = "atencion_ciudadana_datos" + date +".xlsx"
file1 = drive.CreateFile({'title': tittle,
                          'shareable':True,
                          'userPermission':[{'kind':'drive#permission',
                                             'type':'anyone',
                                             'value':'anyone',
                                             'role':'reader'}],
                          'mimeType':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                          "parents":[{"kind":"drive#fileLink","id":"0Bw1YBQEbBwzDWWVkNmd1Wm9zb1E"}]
                      })
file1.SetContentString(c)
file1.Upload()

## Print results
print("https://drive.google.com/uc?export=download&id=" +
      file1['id'] +
      ", Concentrado de peticiones al C. Presidente - " +
      date +
      "_xlsx.xlsx")
