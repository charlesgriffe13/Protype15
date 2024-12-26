import exiftool
import pyexif
from exiftool import *
import subprocess

image = "malinois.MP4"

#  Création du metadata à partir du fichier image
metadata = pyexif.ExifEditor(image)

#  Modification des valeurs des tags
# aux = 'a,b,c,d,e,f'  #  transmettre une liste dans un tag
aux = ''
for i in range(0, 8):
    aux += str(i) + ','

aux = aux[:-1]
print(aux)

with exiftool.ExifTool("exiftool.exe") as et:
    et.execute("-YResolution=720", image)
    et.execute(f"-Comment={aux}", image)

#  Chargement de la liste des tags avec leur valeur dans metaDict
exe = "exiftool.exe"
process = subprocess.Popen([exe, image], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
metaDict = {}
for e in process.stdout:
    line = e.strip().split(':')
    x = line[0].strip()
    y = line[1]
    metaDict[x] = y
    print(f'{x}: {y}')

#  Affichage du tag Comment
#  Si le tag reçoit une valeur nulle ou vide -> erreur
try :
    tag_comment = metaDict.get('Comment').lstrip().split(',')
except:
    tag_comment = ""

print('\n***********  SORTIE ***********************************')
print(f'tag_comment -> {tag_comment}')