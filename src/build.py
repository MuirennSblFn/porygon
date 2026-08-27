"""
Assemble index.html (le jeu, en un seul fichier autonome) a partir de :
    - template.html            (structure + logique du jeu, avec des marqueurs)
    - three.global.wrapped.js  (three.js r169, converti en script classique)
    - asset_data.json          (geometrie + textures de Porygon, encodees en base64)

Usage :
    python3 build.py
Ecrit ../index.html (a la racine du depot), pret pour GitHub Pages.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)


def main():
    with open(os.path.join(BASE_DIR, 'template.html'), encoding='utf-8') as f:
        template = f.read()
    with open(os.path.join(BASE_DIR, 'three.global.wrapped.js'), encoding='utf-8') as f:
        three_js = f.read()
    with open(os.path.join(BASE_DIR, 'asset_data.json'), encoding='utf-8') as f:
        asset_json = f.read()

    out = template.replace('__THREE_GLOBAL_JS__', three_js).replace('__ASSET_JSON__', asset_json)

    out_path = os.path.join(REPO_ROOT, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(out)
    print('index.html genere :', os.path.getsize(out_path), 'octets ->', out_path)


if __name__ == '__main__':
    main()
