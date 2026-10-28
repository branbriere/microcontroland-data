"""Étude Shannon : empreintes SHA-256 de tous les fichiers du protocole, pour le pré-enregistrement.

Écrit EMPREINTES-SHA256.txt (format de « sha256sum », vérifiable avec « sha256sum -c ») à la racine de la section
shannon/, pour les dossiers protocole/, scenarios/ et scripts/. Le fichier est déposé sur Zenodo avec l'archive
du protocole, avant toute collecte confirmatoire ; toute différence ultérieure est une déviation à déclarer.

  python3 empreintes.py

Licence MIT. Version 0.1, 28 octobre 2026.
"""
import hashlib, os

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DOSSIERS = ["protocole", "scenarios", "scripts"]


def main():
    lignes = []
    for d in DOSSIERS:
        for base, sous, fichiers in os.walk(os.path.join(RACINE, d)):
            sous[:] = sorted(s for s in sous if s != "__pycache__")
            for nom in sorted(fichiers):
                chemin = os.path.join(base, nom)
                with open(chemin, "rb") as f:
                    h = hashlib.sha256(f.read()).hexdigest()
                lignes.append(f"{h}  {os.path.relpath(chemin, RACINE).replace(os.sep, '/')}")
    with open(os.path.join(RACINE, "EMPREINTES-SHA256.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print(len(lignes), "fichiers")


if __name__ == "__main__":
    main()
