#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit le portfolio PDF de GNACADJA Marie Edith à partir des réalisations
graphiques du dépôt.

- Anonymise les noms de tiers sur les attestations nominatives
- Compose un PDF A4 paysage : couverture, une page par projet, page compétences

Usage :  python3 construire_portfolio.py
Dépendances : Pillow, reportlab
"""

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE
SOURCES = SORTIE / "sources"
PREPAREES = SORTIE / "preparees"
ZIPS = SOURCES  # les visuels sélectionnés sont dans 04_Portfolio/sources

# Mettre à False pour retirer la série de visuels d'inspiration religieuse du portfolio
INCLURE_SERIE_FOI = True

NAVY = HexColor("#1F3B57")
GOLD = HexColor("#C9A227")
GRIS = HexColor("#5A6672")
LIGHT = HexColor("#F4F6F8")


# --------------------------------------------------------------------------- #
# 1. Anonymisation
# --------------------------------------------------------------------------- #
def masquer(image: Image.Image, zones_ratio):
    """Couvre des rectangles (ratios) par un aplat clair et une mention de masquage."""
    largeur, hauteur = image.size
    draw = ImageDraw.Draw(image, "RGBA")
    try:
        police = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
            max(11, int(hauteur * 0.017)),
        )
    except OSError:
        police = ImageFont.load_default()

    for x0, y0, x1, y1 in zones_ratio:
        boite = (
            int(x0 * largeur),
            int(y0 * hauteur),
            int(x1 * largeur),
            int(y1 * hauteur),
        )
        # Échantillonner la couleur de fond autour de la zone pour rester discret
        draw.rectangle(boite, fill=(252, 252, 252, 255))

        texte = "Nom masqué — donnée personnelle"
        try:
            bbox = draw.textbbox((0, 0), texte, font=police)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        except Exception:
            tw, th = 220, 16
        cx = boite[0] + ((boite[2] - boite[0]) - tw) / 2
        cy = boite[1] + ((boite[3] - boite[1]) - th) / 2
        draw.text((cx, cy), texte, fill=(150, 158, 168, 255), font=police)
    return image


# (fichier source, fichier de sortie, zones à flouter ou None)
PLAN_IMAGES = [
    ("Benin_science_leadership_program/1.png", "01_logo_bslp.png", None),
    ("Copie_de_BSLP/1.png", "02_attestation_participation.png", [(0.16, 0.42, 0.80, 0.58)]),
    ("Copie_de_BSLP/10.png", "03_attestation_formateur.png", None),
    ("Copie_de_BSLP/15.png", "04_tableau_axes.png", None),
    ("ETIQUETTES/1.png", "05_polffree.png", None),
    ("ET_SI_TU_MOURRAIS/1.png", "06_serie_social_1.png", None),
    ("ET_SI_TU_MOURRAIS/3.png", "07_serie_social_2.png", None),
]


def preparer_images():
    SOURCES.mkdir(parents=True, exist_ok=True)
    PREPAREES.mkdir(parents=True, exist_ok=True)
    for source, cible, zones in PLAN_IMAGES:
        src = ZIPS / cible if (ZIPS / cible).exists() else ZIPS / source
        if not src.exists():
            print(f"  ! absent : {src}")
            continue
        image = Image.open(src).convert("RGB")
        if zones:
            image = masquer(image, zones)
        # Limite raisonnable pour un PDF léger et net
        image.thumbnail((1800, 1800), Image.LANCZOS)
        image.save(PREPAREES / cible, "PNG", optimize=True)
        print(f"  préparée : {cible}  {image.size}")


# --------------------------------------------------------------------------- #
# 2. Mise en page du PDF
# --------------------------------------------------------------------------- #
LARGEUR, HAUTEUR = landscape(A4)
MARGE = 18 * mm


def fond(c, couleur=white):
    c.setFillColor(couleur)
    c.rect(0, 0, LARGEUR, HAUTEUR, fill=1, stroke=0)


def filet(c, y, couleur=GOLD, epaisseur=2.2):
    c.setStrokeColor(couleur)
    c.setLineWidth(epaisseur)
    c.line(MARGE, y, LARGEUR - MARGE, y)


def titre_section(c, texte, y):
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGE, y, texte)
    filet(c, y - 5 * mm)


def pied(c, numero):
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 8)
    c.drawString(MARGE, 10 * mm, "GNACADJA Marie Edith R. A. M. — Portfolio graphisme & communication santé")
    c.drawRightString(LARGEUR - MARGE, 10 * mm, str(numero))


def image_centree(c, chemin, zone, cadrage=True):
    """Place une image dans une zone (x, y, largeur, hauteur) en conservant son ratio."""
    img = Image.open(chemin)
    iw, ih = img.size
    zx, zy, zw, zh = zone
    ratio = min(zw / iw, zh / ih)
    w, h = iw * ratio, ih * ratio
    x = zx + (zw - w) / 2
    y = zy + (zh - h) / 2
    c.drawImage(ImageReader(chemin), x, y, w, h, mask="auto")


def legende(c, texte, y, taille=9.5, couleur=GRIS, largeur=None):
    c.setFillColor(couleur)
    c.setFont("Helvetica", taille)
    c.drawString(MARGE, y, texte)


def paragraphe(c, texte, x, y, largeur, taille=9.8, interligne=4.9 * mm, couleur=GRIS):
    """Rendu de paragraphe simple avec retour à la ligne manuel."""
    c.setFillColor(couleur)
    c.setFont("Helvetica", taille)
    largeur_car = largeur / (taille * 0.50)
    for ligne in decouper(texte, int(largeur_car)):
        c.drawString(x, y, ligne)
        y -= interligne
    return y


def decouper(texte, largeur_car):
    mots, lignes, courante = texte.split(), [], ""
    for mot in mots:
        essai = f"{courante} {mot}".strip()
        if len(essai) <= largeur_car:
            courante = essai
        else:
            lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes


def page_couverture(c):
    fond(c)
    c.setFillColor(NAVY)
    c.rect(0, HAUTEUR - 62 * mm, LARGEUR, 62 * mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, HAUTEUR - 66 * mm, LARGEUR, 4 * mm, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(MARGE + 4 * mm, HAUTEUR - 32 * mm, "GNACADJA Marie Edith R. A. M.")
    c.setFont("Helvetica", 16)
    c.drawString(MARGE + 4 * mm, HAUTEUR - 43 * mm, "Nutritionniste de santé publique  ·  Graphiste")

    c.setFont("Helvetica", 10.5)
    c.drawString(MARGE + 4 * mm, HAUTEUR - 54 * mm,
                 "Portfolio — supports de communication, identité visuelle et édition scientifique")

    y = HAUTEUR - 90 * mm
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGE, y, "Réalisations présentées")
    filet(c, y - 4 * mm, NAVY, 1.2)

    items = [
        ("01", "Identité visuelle — Benin Science Leadership Program (BSLP)"),
        ("02", "Série d'attestations — programme scientifique financé par l'Union européenne"),
        ("03", "Édition scientifique — tableau de formation pédagogique"),
        ("04", "Étiquette produit — charbon actif PolFFree-AC (URMAPHA)"),
        ("05", "Série de visuels pour réseaux sociaux — campagne de sensibilisation"),
    ]
    y -= 12 * mm
    for num, texte in items:
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGE, y, num)
        c.setFillColor(HexColor("#2C3E50"))
        c.setFont("Helvetica", 11)
        c.drawString(MARGE + 12 * mm, y, texte)
        y -= 8.5 * mm

    y = 34 * mm
    filet(c, y + 8 * mm, GOLD, 1.2)
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 9.5)
    c.drawString(MARGE, y, "Womey, Abomey-Calavi, Bénin  ·  +229 62 07 56 06  ·  edithgnaca1@gmail.com")
    c.drawString(MARGE, y - 5 * mm,
                 "Master Nutrition et santé des populations (IRSP Ouidah)  ·  DU Éducation nutritionnelle (Université Senghor)  ·  Formation en graphisme (EIGB)")

    pied(c, 1)
    c.showPage()


def page_projet(c, numero, titre, sous_titre, images, description, role, outils, numeros):
    fond(c)

    # Bandeau de titre
    c.setFillColor(NAVY)
    c.rect(0, HAUTEUR - 26 * mm, LARGEUR, 26 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(MARGE, HAUTEUR - 13 * mm, titre)
    c.setFont("Helvetica", 9.5)
    c.drawString(MARGE, HAUTEUR - 20 * mm, sous_titre)

    # Colonne d'images à gauche, texte à droite
    colonne_img_w = LARGEUR * 0.60 - MARGE
    colonne_texte_x = MARGE + colonne_img_w + 10 * mm
    colonne_texte_w = LARGEUR - colonne_texte_x - MARGE

    zone_y = 22 * mm
    zone_h = HAUTEUR - 26 * mm - zone_y - 8 * mm
    n = len(images)
    if n == 1:
        image_centree(c, images[0], (MARGE, zone_y, colonne_img_w, zone_h))
    elif n == 2:
        h = (zone_h - 6 * mm) / 2
        image_centree(c, images[0], (MARGE, zone_y + h + 6 * mm, colonne_img_w, h))
        image_centree(c, images[1], (MARGE, zone_y, colonne_img_w, h))
    else:
        h = (zone_h - 2 * 6 * mm) / 3
        for i, img in enumerate(images[:3]):
            image_centree(
                c, img, (MARGE, zone_y + (2 - i) * (h + 6 * mm), colonne_img_w, h)
            )

    y = HAUTEUR - 40 * mm
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(colonne_texte_x, y, "LE TRAVAIL")
    y -= 6 * mm
    y = paragraphe(c, description, colonne_texte_x, y, colonne_texte_w)

    y -= 4 * mm
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(colonne_texte_x, y, "MON RÔLE")
    y -= 6 * mm
    y = paragraphe(c, role, colonne_texte_x, y, colonne_texte_w)

    y -= 4 * mm
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(colonne_texte_x, y, "OUTILS")
    y -= 6 * mm
    paragraphe(c, outils, colonne_texte_x, y, colonne_texte_w)

    pied(c, numeros)
    c.showPage()


def page_competences(c, numero):
    fond(c)
    titre_section(c, "Compétences et profil", HAUTEUR - 28 * mm)

    y = HAUTEUR - 52 * mm
    blocs = [
        ("Graphisme et production de supports",
         "Identité visuelle et déclinaison de marque · mise en page d'attestations, de certificats "
         "et de documents institutionnels · étiquettes et visuels produit · visuels pour réseaux sociaux · "
         "hiérarchie typographique et charte de couleurs"),
        ("Communication pour la santé",
         "Conception de supports d'éducation et de sensibilisation · vulgarisation de contenus scientifiques · "
         "adaptation des messages aux publics communautaires · éducation nutritionnelle"),
        ("Nutrition et santé publique",
         "Master Nutrition et santé des populations (IRSP Ouidah) · DU Éducation nutritionnelle pour l'Afrique "
         "francophone (Université Senghor) · analyse de situation sanitaire · KoboCollect, Epi Info, Stata"),
        ("Outils",
         "Canva · Microsoft Word (mise en forme avancée) · PowerPoint · Excel · KoboCollect · Epi Info · Stata"),
        ("Langues",
         "Français courant · anglais intermédiaire (lecture de documents scientifiques) · "
         "fon et mina : notions"),
    ]
    for titre, contenu in blocs:
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(MARGE, y, titre)
        y -= 6.5 * mm
        y = paragraphe(c, contenu, MARGE, y, LARGEUR - 2 * MARGE, taille=10)
        y -= 5 * mm

    filet(c, y + 2 * mm, GOLD, 1.2)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGE, y - 6 * mm, "Marie Edith R. A. M. GNACADJA")
    c.setFillColor(GRIS)
    c.setFont("Helvetica", 9.5)
    c.drawString(MARGE, y - 12 * mm,
                 "+229 62 07 56 06  ·  edithgnaca1@gmail.com  ·  Womey, Abomey-Calavi, Bénin")

    pied(c, numero)
    c.showPage()


PROJETS = [
    dict(
        titre="Identité visuelle — Benin Science Leadership Program",
        sous_titre="Logo · programme de leadership scientifique, Université d'Abomey-Calavi",
        images=["01_logo_bslp.png"],
        description=(
            "Création du logo du Benin Science Leadership Program (B-SLP). La silhouette du Bénin est "
            "construite en pointillés à partir de structures moléculaires — le langage visuel de la "
            "recherche scientifique — et associée à une cible, symbole d'objectif et de trajectoire. "
            "Le lettrage BSLP et son déploiement assurent la lisibilité en petit format."
        ),
        role=(
            "Conception graphique complète : recherche de concept, construction de la silhouette, "
            "traitement des motifs moléculaires, typographie et déclinaison."
        ),
        outils="Vectorisation, mise en page, déclinaison d'identité",
    ),
    dict(
        titre="Série d'attestations — programme scientifique financé par l'UE",
        sous_titre="BSLP / projet MINNAGAN · Union européenne, Erasmus+ · avril 2024",
        images=["02_attestation_participation.png", "03_attestation_formateur.png"],
        description=(
            "Conception d'une famille cohérente d'attestations pour le programme de leadership "
            "scientifique au Bénin : participation, supervision d'enquête, formateur d'agent enquêteur "
            "et formation pédagogique du projet MINNAGAN. Un même système graphique — bandeaux vert et or, "
            "angles dorés, bandeau de logos partenaires — est décliné sur chaque type de document afin de "
            "garantir l'unité visuelle et la crédibilité institutionnelle."
        ),
        role=(
            "Conception graphique et mise en page de la série. Les noms des bénéficiaires ont été masqués "
            "dans ce portfolio (données personnelles)."
        ),
        outils="Mise en page A4 paysage, déclinaison d'un système graphique, intégration de logos partenaires",
    ),
    dict(
        titre="Édition scientifique — tableau de formation pédagogique",
        sous_titre="URMAPHA / EPAC · Université d'Abomey-Calavi",
        images=["04_tableau_axes.png"],
        description=(
            "Mise en forme d'un tableau de synthèse des dix axes thématiques d'une formation pédagogique "
            "destinée aux enseignants du supérieur. Travail sur la lisibilité : alternance de bandes de "
            "couleur, hiérarchie des colonnes, encadrement et cohérence avec la charte des documents du programme."
        ),
        role="Conception graphique et mise en page du document.",
        outils="Mise en page, traitement de tableau, charte couleur",
    ),
    dict(
        titre="Étiquette produit — charbon actif PolFFree-AC",
        sous_titre="URMAPHA, Université d'Abomey-Calavi · santé environnementale et accès à l'eau",
        images=["05_polffree.png"],
        description=(
            "Création du visuel de présentation d'un charbon actif en poudre mis au point par l'URMAPHA "
            "pour éliminer les polluants organiques de l'eau. La composition associe la matière première "
            "(balle de riz), le produit fini, la mention « 100 % écologique », le mode d'emploi et "
            "l'identification du laboratoire. Un exercice d'équilibre entre rigueur informative et attractivité produit."
        ),
        role=(
            "Conception graphique du visuel et de la mise en page informative. "
            "Document produit pour un laboratoire de recherche en santé."
        ),
        outils="Composition visuelle, retouche d'image, hiérarchie de l'information",
    ),
    dict(
        titre="Série de visuels pour réseaux sociaux",
        sous_titre="Campagne de sensibilisation · format carré 1080 × 1080",
        images=["06_serie_social_1.png", "07_serie_social_2.png"],
        description=(
            "Conception d'une série de visuels destinés aux réseaux sociaux, construite sur une palette "
            "ocre et brun, une typographie à empattements et des motifs organiques. Le principe de série — "
            "une accroche, une citation, une réponse — maintient l'attention sur plusieurs publications "
            "tout en conservant une identité reconnaissable."
        ),
        role=(
            "Conception graphique de la série : palette, typographie, gabarits et déclinaison "
            "sur l'ensemble des visuels."
        ),
        outils="Gabarits réutilisables, déclinaison de série, composition typographique",
    ),
]


def construire():
    preparer_images()

    pdf = SORTIE / "Portfolio_GNACADJA_Marie_Edith.pdf"
    c = canvas.Canvas(str(pdf), pagesize=(LARGEUR, HAUTEUR))
    c.setTitle("Portfolio — GNACADJA Marie Edith")
    c.setAuthor("GNACADJA Marie Edith R. A. M.")

    page_couverture(c)
    numero = 2
    for projet in PROJETS:
        if projet["titre"].startswith("Série de visuels") and not INCLURE_SERIE_FOI:
            continue
        chemins = [PREPAREES / nom for nom in projet["images"]]
        chemins = [p for p in chemins if p.exists()]
        if not chemins:
            continue
        page_projet(
            c,
            numero,
            projet["titre"],
            projet["sous_titre"],
            chemins,
            projet["description"],
            projet["role"],
            projet["outils"],
            numero,
        )
        numero += 1

    page_competences(c, numero)
    c.save()
    print(f"\nPDF généré : {pdf}")
    return pdf


if __name__ == "__main__":
    construire()
