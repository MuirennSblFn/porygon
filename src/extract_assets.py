"""
Extraction des assets 3D de Porygon depuis le fichier COLLADA (.DAE) et des
textures PNG, vers un unique fichier JSON (asset_data.json) consomme par le
jeu (voir template.html + build.py).

Usage :
    pip install pycollada numpy --break-system-packages
    python3 extract_assets.py

Le script lit :
    ./Porygon_ColladaMax.DAE
    ./textures/normal/{Body1,BodyNor,Eye1,EyeNor}.png
    ./textures/shiny/{Body1,BodyNor,Eye1,EyeNor}.png
et ecrit :
    ./asset_data.json
"""
import os
import collada
import numpy as np
import base64
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DAE_PATH = os.path.join(BASE_DIR, 'Porygon_ColladaMax.DAE')
OUT_PATH = os.path.join(BASE_DIR, 'asset_data.json')


def zup_to_yup(arr):
    # COLLADA (Z-up) -> three.js (Y-up) : (x, y, z) -> (x, z, -y)
    out = np.empty_like(arr)
    out[:, 0] = arr[:, 0]
    out[:, 1] = arr[:, 2]
    out[:, 2] = -arr[:, 1]
    return out


def extract_prim(p):
    vidx = p.vertex_index
    nidx = p.normal_index
    tidx = p.texcoord_indexset[0]
    pos = p.vertex
    nor = p.normal
    uv = p.texcoordset[0]

    verts = pos[vidx.reshape(-1)].astype(np.float32)
    norms = nor[nidx.reshape(-1)].astype(np.float32)
    uvs = uv[tidx.reshape(-1)].astype(np.float32).copy()
    # convention pixel verifiee empiriquement : pixel_y = (1 - v) * hauteur
    uvs[:, 1] = 1.0 - uvs[:, 1]
    return verts, norms, uvs, vidx.shape[0] * 3


def b64(arr):
    return base64.b64encode(arr.astype(np.float32).tobytes()).decode('ascii')


def img_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')


def tex_path(variant, name):
    return os.path.join(BASE_DIR, 'textures', variant, 'pm0137_00_' + name + '.png')


def main():
    c = collada.Collada(DAE_PATH)
    geom = c.geometries[0]
    body_prim, eye_prim = geom.primitives[0], geom.primitives[1]

    bverts, bnorms, buvs, bcount = extract_prim(body_prim)
    everts, enorms, euvs, ecount = extract_prim(eye_prim)

    bverts = zup_to_yup(bverts)
    bnorms = zup_to_yup(bnorms)
    everts = zup_to_yup(everts)
    enorms = zup_to_yup(enorms)

    all_pos = np.concatenate([bverts, everts], axis=0)
    center = (all_pos.max(axis=0) + all_pos.min(axis=0)) / 2.0
    scale = 2.2 / (all_pos.max(axis=0) - all_pos.min(axis=0)).max()

    bverts_n = (bverts - center) * scale
    everts_n = (everts - center) * scale

    data = {
        "body": {"pos": b64(bverts_n), "nor": b64(bnorms), "uv": b64(buvs), "count": bcount},
        "eye": {"pos": b64(everts_n), "nor": b64(enorms), "uv": b64(euvs), "count": ecount},
        "textures": {
            "normal": {
                "body": img_b64(tex_path('normal', 'Body1')),
                "bodyNor": img_b64(tex_path('normal', 'BodyNor')),
                "eye": img_b64(tex_path('normal', 'Eye1')),
                "eyeNor": img_b64(tex_path('normal', 'EyeNor')),
            },
            "shiny": {
                "body": img_b64(tex_path('shiny', 'Body1')),
                "bodyNor": img_b64(tex_path('shiny', 'BodyNor')),
                "eye": img_b64(tex_path('shiny', 'Eye1')),
                "eyeNor": img_b64(tex_path('shiny', 'EyeNor')),
            },
        },
    }

    with open(OUT_PATH, 'w') as f:
        json.dump(data, f)
    print('asset_data.json genere :', os.path.getsize(OUT_PATH), 'octets')


if __name__ == '__main__':
    main()
