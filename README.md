# SpectroFit : Logiciel de traitement de Spectre de l'association IPSA VEGA



## I. Présentation du logiciel :

Au lancement du logiciel, il se présente de la façon suivante : 

![image-20200916145112010](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916145112010.png)

### Import de fichier

pour importer un fichier, il faut aller dans l'onglet file et choisir le format que l'on souhaite importer : 

![image-20200916145215693](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916145215693.png)

3 formats sont disponibles:

- S : pour les fichiers de Narval
- CSV : pour les fichiers de Narval transformés à partir des fichiers S
- FITS : pour les fichiers de Neo Narval

### graph et ordre

Une fois que l'on a choisi le type de fichier que l'on veut, on peut afficher le spectre. Pour cela, il faut remplir la case ordre (en dessous de choisi ton ordre) ou bien cocher la case "full Spectrum". Une fois cela fait, il faut appuyer sur le bouton compute.

![image-20200916145519028](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916145519028.png)

### Fit

Plusieurs types de fits sont disponibles dans le logiciel : 

- Fit ordinaire : permet de fit un model préconçue aux données
- Fit mix : permet de faire la somme de modèle préconçu
- Fit interactif : l'utilisateur fit lui même ses données

Pour activer chacun des fits, il faut placer les deux bornes entre lesquelles on veut ajuster la courbe au données. Pour se faire, il faut clic droit à l'endroit où l'on veut placer une borne et ensuite sur "place fitting point" : 

![image-20200916150857442](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916150857442.png)

Une fois que deux points ont été placés, on peut accéder aux outils de fits : 

![image-20200916151005180](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916151005180.png)

pour l'accès au fix ordinaire ou mix, il faut appuyer sur Fits. Pour les fits interactifs, il faut appuyer sur Interactive Fit.Si l'on clique Sur Fit, cette fenêtre apparait : 

![image-20200916151159900](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916151159900.png)

#### Fit ordinaire

Sur la figure précédente, tous les boutons font références à un fit ordinaire excepté "mix" et "new model".

Le nom du model utilisé est celui du bouton. 

Attention à bien faire attention à cocher la case en haut si le spectre est un spectre en absorption.

Une fois cliquer sur le bouton, le fit se réalise automatiquement. Le résultat s'affiche. 

![image-20200916151421592](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916151421592.png)

Une courbe verte apparaît montrant la fonction obtenue. Une fenêtre popup montre aussi les informations sur le résultat. Juste après avoir fini le fit, un fenêtre d'enregistrement de votre OS apparaît, elle sert à enregistrer les résultats du fit dans un fichier texte.

#### Fit mix

Quand on clique sur Mix Fit, on obtient la fenêtre suivante : 

![image-20200916152140162](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916152140162.png)

Ici, il faut choisir à gauche les modèles que l'on veut : on peut choisir autant de modèle que l'onveut. Les modèles choisis seront alors ajoutés les uns aux autres pour former un modèle plus grand.

Attention à bien cocher la case si le spectre est un spectre d'émission

A droite, il faut cocher la méthode de fit à utiliser pour obtenir le résultat.

Voici un exemple : 

![image-20200916152356420](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916152356420.png)

Les résultats sont présentés dans la même forme que ci-dessus.

#### Fit interactif

Pour lancer l'application de fit interactif, il faut cliquer sur l'option "interactive Fit" du menu "Tools" dans la barre des tâches. 

![image-20200916152617491](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916152617491.png)

Une fenêtre s'affiche avec les données zoomé sur la zone encadré par les deux points de fit.

Dans l'onglet tools, on peut ajouter deux modèles de courbes : 

- gaussienne 
- lorentzienne

![image-20200916152850585](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916152850585.png)

Lorsque l'on ajoute des courbes, les fenêtres (à droite de l'image) apparaissent. Elles permettent de contrôler la valeur des paramètres. Lorsque l'on bouge un paramètre, la courbe correspondante se met à jour. 

Sur la figure, la courbe rouge est la somme de la courbe bleue et verte. Les courbes bleues sont des gaussiennes. Les courbes vertes sont des lorentziennes

Une fois que l'on a fait un fit correspondant aux données, on peut allez dans l'onglet report puis cliquer sur "Fit report" pour enregistrer tous les résultats

### Signal Processing

Lorsqu'un spectre est chargé et affiché, on peut effectuer des opérations de traitement numérique du signal dessus. Pour ce faire, il faut cliquer sur Signal Processing Toolbox dans l'onglet Tools. Cette fenêtre apparaît : 

![image-20200916160725190](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916160725190.png)

Elle permet de faire une décomposition en wavelet du spectre. Pour le moment c'est la seule fonctionnalité implémentée : l'onglet fourier transform est vide.

Pour ce faire, il faut choisir un ordre de décomposition et un méthode. Pour choisir correctement, il faut avoir vu la théorie sur les wavelets qui n'est pas expliquées ici.

exemple d'utilisation : 

![image-20200916162349289](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916162349289.png)

on obtient : 

![](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916162528275.png)

Voici la décomposition en wavelet. On peut donc enlever le bruit et garder l'information.

Pour garder une courbe, il faut cocher la case correspondante. Dans le texte qui est joint à la case, on peut rentrer un nombre entre 0 et 1. C'est le pourcentage de l'information que l'on veut garder sur la courbe. Si la case est cochée mais que le champs n'est pas rempli, alors il est considéré comme étant 1.

![image-20200916162811742](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916162811742.png)

On obtient un spectre dont le bruit est partiellement partie. Ici je n'ai retiré qu'une petite fraction du bruit car j'ai voulu garder le maximum d'information.

### Attribution des raies

Le logiciel permet aussi d'attribuer les raies d'un spectre à un élément. Pour cela, il faut aller dans tools puis dans Trouver une raie. Sur la fenêtre qui apparaît, il faut cliquer sur periodic table : 

![image-20200916163037812](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916163037812.png)

Il faut cliquer sur l'élément de votre choix, par exemple l'hydrogène, et il apparaît sur le graphique.

![image-20200916163411941](C:\Users\Administrateur.UTILISA-D5U7HV7\AppData\Roaming\Typora\typora-user-images\image-20200916163411941.png)

On peut supprimé l'affichage en réappuyant sur le bouton de l'hydrogène. 

Il est possible grâce à cela d'attribuer les raies et de calculer un shift grâce à l'outil distance. Pour cela il faut place deux points sur le graph avec un clic droit. Dans le menu cliquer sur "place distance point". Une fois que deux points sont placés, dans tools, cliquer sur distance. Le calcul apparaît dans une fenêtre.

## II. Description de l'organisation des fichiers :

### Racine

Dans la racine du repo sur github on a les fichiers : 

- *.s et *.csv : données des spectres
- delimitation_ordre.csv : limites des ordres pour NARVAL
- lineident_to_json.py : code permettant de transformer lineident.csv en un fichier json
- setup.py : code permettant de créer un exécutable (ne fonctionne pas pour le moment)
- spectrofit.py : fichier principal à lancer pour lancer le programme
- periodicTable.py : exemple de tableau périodique en python

Dans le dossier racine, on trouve les dossiers suivant : 

### spectrofit

Dans le dossier spectrofit on a  :

#### core

- CSVfile (deprecated)
- QTimportFile : gère tout ce qui concerne l'import des fichiers dans spectrofit
- compude_delim.py : gère le calcul de découpe du spectre en fonction de l'ordre
- plots.py : création des figures
- lineident.json : données sur tous les éléments physiques connus

#### math

- Fits.py : gère tout le module de fit
- UserFit.py : gère le mix fit
- mathfunction : toutes les fonctions mathématiques

#### tools

- Interactive_Fit.py : gère le fit interactif avec ajout de courbes
- Signal_processing_toolbox : outil de traitements du signal
- elements_table.py : gère l'affichage des éléments connues

#### ui

- DoubleSlider : gère le double slider utilisé pour les fits interactifs
- PainterCanvas : Canvas pour afficher les figures dans le logiciel
- QtApp.py : launch app
- QTmainframe.py : ui + programme principal
- Slider*.py : slider pour chaque fonction de fit interactif
- app.py & mainFrame.py : deprecated

### test

Tests des fonctionnalités indépendamment du logiciel (à ne pas toucher)

### .idea

build python, à ne pas toucher



Développé par Yoann AUDET. Tous droits réservés.







