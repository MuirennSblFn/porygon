# Console de soin Porygon

Un petit jeu de soin virtuel (a la Nintendogs) pour Porygon, en 3D dans le
navigateur avec Three.js. Nourrir, jouer, nettoyer, faire progresser et
recalibrer un Porygon qui respire, cligne des yeux et reagit a l'heure qu'il
est — le tout dans un unique fichier HTML autonome, sans backend ni
dependance externe a charger.

## Fonctionnalites

- **Rendu 3D** du modele Porygon (forme normale + chromatique), avec
  eclairage et couleurs calibres pour matcher l'art officiel.
- **Soin de base** : Nourrir / Jouer / Nettoyer, avec trois jauges (faim,
  bonheur, proprete) qui se degradent dans le temps et se sauvegardent
  localement (`localStorage`).
- **Progression** : XP, niveaux, et deux paliers d'"evolution simulee"
  (Porygon2, Porygon-Z) avec un effet visuel dedie.
- **Cycle jour/nuit** : mode veille base sur l'heure reelle de l'appareil
  (animation ralentie, yeux mi-clos, decroissance des stats reduite), et
  evenements aleatoires (jour/nuit).
- **4 mini-jeux**, regroupes dans un hub dedie, chacun avec 3 charges/jour et
  une difficulte qui augmente avec le niveau :
  - *Recalibrage du signal* — stabiliser un marqueur oscillant dans une zone.
  - *Memoire de signal* — memoriser et reproduire une sequence de 6 signaux.
  - *Capture de donnees* — toucher des fragments avant qu'ils disparaissent,
    en evitant les leurres (a partir du niveau 3).
  - *Puzzle de circuit* — faire pivoter des segments pour relier un circuit,
    sur un chemin qui s'allonge avec le niveau.
- **Compatible mobile/tablette** (safe-area, cibles tactiles, sans
  debordement horizontal) et respecte `prefers-reduced-motion`.

## Lancer le jeu

Le jeu tient dans un seul fichier : `index.html`, a la racine du depot.
Aucune installation, aucun serveur requis :

```bash
# n'importe lequel des deux suffit
open index.html                 # macOS
xdg-open index.html             # Linux
# ou glisser-deposer index.html dans un navigateur
```

## Deployer sur GitHub Pages

1. Creer un depot GitHub et y pousser le contenu de ce dossier :

   ```bash
   git init
   git add .
   git commit -m "Console de soin Porygon"
   git branch -M main
   git remote add origin https://github.com/<votre-compte>/<votre-depot>.git
   git push -u origin main
   ```

2. Dans les parametres du depot GitHub : **Settings -> Pages**, choisir la
   branche `main` et le dossier `/ (root)`, puis enregistrer.
3. Le jeu sera servi a l'adresse
   `https://<votre-compte>.github.io/<votre-depot>/` (peut prendre une
   minute ou deux apres l'activation).

Comme `index.html` est totalement autonome (three.js et les assets sont
integres en base64 a l'interieur du fichier), c'est tout ce qu'il faut :
pas de build step cote GitHub Pages.

## Reconstruire index.html depuis les sources

Le dossier `src/` contient tout ce qu'il faut pour regenerer `index.html`
ou modifier le jeu :

```
src/
├── Porygon_ColladaMax.DAE     # modele 3D source (geometrie + UV)
├── textures/
│   ├── normal/                # textures forme normale (deja recolorees)
│   ├── shiny/                 # textures forme chromatique (deja recolorees)
│   ├── normal_pristine/       # texture de corps d'origine, avant retouche
│   └── shiny_pristine/        # idem, forme chromatique
├── extract_assets.py          # DAE + textures -> asset_data.json
├── asset_data.json            # geometrie + textures encodees en base64
├── three.global.wrapped.js    # three.js r169, converti en script classique
├── template.html              # structure HTML/CSS/JS du jeu (avec marqueurs)
└── build.py                   # assemble template + three.js + assets -> index.html
```

Pour tout regenerer depuis zero (utile si vous modifiez une texture ou le
modele) :

```bash
cd src
pip install pycollada numpy --break-system-packages
python3 extract_assets.py   # regenere asset_data.json depuis le DAE + textures
python3 build.py            # regenere ../index.html
```

Pour ne modifier que le code du jeu (UI, logique, mini-jeux) sans toucher
aux assets 3D, il suffit d'editer `src/template.html` puis de relancer
`python3 build.py`.

### Note sur les textures

Les dossiers `*_pristine/` conservent la texture de corps (`Body1.png`)
telle qu'extraite a l'origine, avant recoloration. Les textures dans
`normal/` et `shiny/` ont ete retouchees (tete et pieds recolores) pour
faire correspondre le placement des couleurs a l'art officiel du Porygon
classique ; tout le reste (nageoire, grille du poitrail, queue) est resté
identique a l'original.

## Credits & mentions legales

- **Three.js** — moteur de rendu 3D, licence MIT.
  https://threejs.org
- **Porygon et l'ensemble des assets 3D/textures** appartiennent a
  Nintendo, Game Freak et Creatures Inc. Ce projet est un fan-project non
  officiel et non commercial ; les modeles/textures ont ete extraits d'un
  fichier fourni par l'utilisateur, pas crees pour ce projet.

**A savoir avant de publier ce depot publiquement :** comme il contient des
assets 3D et des textures tires directement d'un jeu Pokemon, un depot
public (et une GitHub Pages qui les sert publiquement) peut faire l'objet
d'une demande de retrait (DMCA) de la part de l'ayant droit — GitHub honore
ce type de demandes. Si vous voulez eviter ce risque, gardez le depot
**prive** (les Pages d'un depot prive necessitent GitHub Pro/Team/Enterprise
pour etre servies) ou hebergez-le uniquement pour un usage personnel/local.

Le code du jeu proprement dit (HTML/CSS/JS ecrit pour ce projet, scripts
Python) peut etre considere comme sous licence MIT — voir `LICENSE`. Cette
licence ne couvre pas les assets Pokemon (modele, textures) presents dans
`src/textures/` et `src/Porygon_ColladaMax.DAE`, ni `asset_data.json` et
`index.html` qui les embarquent.
