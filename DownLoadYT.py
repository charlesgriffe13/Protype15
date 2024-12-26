from pytube import YouTube

# Entrez l'URL de la vidéo YouTube que vous voulez télécharger
url = "www.youtube.com/watch?v=N-iSFCBW1Cw"

# Créez un objet YouTube en utilisant l'URL
yt = YouTube(url)

# Affichez les détails de la vidéo
print("Titre de la vidéo: ", yt.title)
print("Nombre de vues: ", yt.views)
print("Durée de la vidéo: ", yt.length, "secondes")
print("Description de la vidéo: ", yt.description)
print("Note moyenne de la vidéo: ", yt.rating)

# Choisissez la qualité vidéo souhaitée (la première disponible)
ys = yt.streams.get_highest_resolution()

# Téléchargez la vidéo
print("Téléchargement en cours...")
ys.download()
print("Téléchargement terminé!")