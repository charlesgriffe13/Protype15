import exiftool
import pyexif
from exiftool import *
import subprocess

#  Fichier vidéo à tager
video = 'nash.mp4'

#  Créer liste des tags à inclure dans le MetaData
listTag = ['logiciel', 'keep it', 'tutoriel', 'électricité', 'Français']

#  Formater la liste pour l'inclure dans le métadata
aux = ''
for tag in listTag:
    aux += tag + ','
aux = aux[:-1]
# print(aux)

#  Enregistrer la liste des tags dans la rubrique choisie : -Comment
with exiftool.ExifTool("exiftool.exe") as et:
    et.execute(f'-Comment={aux}', video)

#  Récupération detoutes les rubriques dans le métaData
exe = "exiftool.exe"
process = subprocess.Popen([exe, video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
metaDict = {}
for e in process.stdout:
    line = e.strip().split(':')
    x = line[0].strip()
    y = line[1]
    metaDict[x] = y
    # print(f'{x} : {y}')

#  Récupération des tags dans la rubrique Comment du MétaData
try:
    tag_comment = metaDict.get('Comment').lstrip().split(',')
except:
    tag_comment = ''

print('************ SORTIE *****************************')
print(tag_comment)