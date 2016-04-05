#! /usr/bin/python

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import codecs
import time
import string

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

## Read MAT
mat = codecs.open("/home/luis/Documents/Presidencia/Rick/upload_adela/MAT.csv")
c   = mat.read()

printable = set(string.printable)
c         = filter(lambda x: x in printable, c)

## Upload file
title = "mat_" + time.strftime("%Y-%m-%dT%H:%M:%S")+".csv"
drive = GoogleDrive(gauth)
file1 = drive.CreateFile({'title': title,
                          'shareable':True,
                          'userPermission':[{'kind':'drive#permission',
                                             'type':'anyone',
                                             'value':'anyone',
                                             'role':'reader'}],
                          'mimeType':'text/csv',
                          "parents":[{"kind":"drive#fileLink","id":"0B5p8KkRjjG4HYzBTbEIxWFdqZnM"}]
                      })
file1.SetContentString(c)
file1.Upload()

##------------------------------------------------

## Read resumen
resumen = codecs.open("/home/luis/Documents/Presidencia/Rick/upload_adela/datosgob_resum.csv")
c       = resumen.read()

printable = set(string.printable)
c         = filter(lambda x: x in printable, c)

## Upload file
## title = "resumen_" + time.strftime("%Y-%m-%dT%H:%M:%S")+".csv"
## file1 = drive.CreateFile({'title': "dgm_analytics.csv",
   ##                       'shareable':True,
     ##                     'userPermission':[{'kind':'drive#permission',
       ##                                      'type':'anyone',
         ##                                    'value':'anyone',
           ##                                  'role':'reader'}],
             ##             'mimeType':'text/csv',
               ##           "parents":[{"kind":"drive#fileLink","id":"0B5p8KkRjjG4HcFNOdXFsNDFvSEk"}]
                 ##     })
## file1.SetContentString(c)
## file1.Upload()

## Update
file2 = drive.CreateFile({'id':'0B5p8KkRjjG4HcTdUTEF6dnpZTWc'})
content = file2.GetContentString()
file2.SetContentString(content.replace(content, c))
file2.Upload()

## Download
## https://drive.google.com/uc?export=download&id=0B5p8KkRjjG4HcTdUTEF6dnpZTWc
