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

##------------------------------------------------
## PUBLIC RESOURCES
##------------------------------------------------

## Read in data
mat = codecs.open("/home/luis/Documents/Presidencia/Rick/upload_adela/MAT.csv")
c   = mat.read()
## Encoding
printable = set(string.printable)
c         = filter(lambda x: x in printable, c)
## Print result
print("URL Descarga, Nombre")

## -------------
## XLSX
## -------------
date  = time.strftime("%Y-%m-%dT%H:%M:%S")
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
