# Le script de l'automatisation filmant une liste de vocabulaire
-----------------------
Quand vous vous promenez sur Youtube, vous pouvez voir beaucoup de vidéos qui vous aident d'apprendre par coeur des vocabulaires. Pour la plupart, cettes mêmes vidéos sont produites de la manière selon laquelle seul son contenu varie sous la même forme avec long temps, mais ce sera trop fatigant si vous travaillez sur une vidéo en tapant un par un ou enregistrant TTS à votre main. Ainsi, ce repositoire fournit la solution simple qui soulage votre fatigue qui résulte d'une production de vidéo qui nécessite de pas mal de travails.

## Les bibliothèques requises
Veuillez s'installer aux bibliothèques suivantes au travers de pip.
* pip install pillow (PIL)
* pip install moviepy
* pip install gtts
* pip install pydub

## Paramètres
C'est simple. Il suffit de mettre les variables suivantes en console pour produire une vidéo.
> filmer.py (langue_du_départ) (chemin_de_fichier_de_vocabulaires) (chemin_de_fichier_de_photo)

#### langue_du_départ
ex. fr, en, de ...
#### chemin_de_fichier_de_vocabulaires
Le délimiteur est 'I'. La gauche est un terme et le droit est sa signification. À présent, c'est optimisé que la langue du départ est français et celle de l'arrivée est coréen. (C'est ma propre manière d'utiliser Quizlet et d'y exporter des vocabulaires.)

ex. words.txt
#### chemin_de_fichier_de_photo
Background. Utilisez black.png en dossier. C'est à la fois simple et efficace.

ex. photo.png

----------------------------
*Vous pouvez à part customiser le font ou sa taille en révisant directement le script.*
