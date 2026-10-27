#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère les PDF finaux (CV et lettres) à partir des fichiers Markdown.

Sortie : PDF A4 prêts à téléverser sur les plateformes de recrutement.

Usage :  python3 generer_pdf.py
Dépendances : reportlab
"""

import re
import sys
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        HRFlowable,
        KeepTogether,
        PageTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )
except ImportError:
    sys.exit("reportlab manquant : pip install reportlab")

RACINE = Path(__file__).resolve().parent.parent

NAVY = colors.HexColor("#1F3B57")
GOLD = colors.HexColor("#C9A227")
GRIS = colors.HexColor("#4A5560")
GRIS_CLAIR = colors.HexColor("#7A8794")
FILET = colors.HexColor("#C8CFD6")


# --------------------------------------------------------------------------- #
# Styles
# --------------------------------------------------------------------------- #
def styles_cv():
    base = getSampleStyleSheet()
    return {
        "nom": ParagraphStyle("nom", fontName="Helvetica-Bold", fontSize=19,
                              leading=22, textColor=NAVY, spaceAfter=2),
        "accroche": ParagraphStyle("accroche", fontName="Helvetica", fontSize=10.5,
                                   leading=13.5, textColor=GOLD, spaceAfter=3),
        "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=8.6,
                                  leading=11, textColor=GRIS, spaceAfter=1),
        "section": ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10.2,
                                  leading=12, textColor=NAVY, spaceBefore=9, spaceAfter=1),
        "sous": ParagraphStyle("sous", fontName="Helvetica-Bold", fontSize=9.6,
                               leading=12, textColor=colors.HexColor("#1A2733"),
                               spaceBefore=5, spaceAfter=1),
        "corps": ParagraphStyle("corps", fontName="Helvetica", fontSize=8.9,
                                leading=11.6, textColor=colors.HexColor("#26313B"),
                                spaceAfter=2.5, alignment=TA_LEFT),
        "ital": ParagraphStyle("ital", fontName="Helvetica-Oblique", fontSize=8.5,
                               leading=10.8, textColor=GRIS, spaceAfter=1),
        "puce": ParagraphStyle("puce", fontName="Helvetica", fontSize=8.9,
                               leading=11.4, textColor=colors.HexColor("#26313B"),
                               leftIndent=9, bulletIndent=1, spaceAfter=1.2),
        "note": ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=8,
                               leading=10.4, textColor=GRIS_CLAIR, spaceBefore=4),
    }


def styles_lettre():
    return {
        "nom": ParagraphStyle("nom", fontName="Helvetica", fontSize=9.5, leading=12.5,
                              textColor=colors.black, spaceAfter=0),
        "accroche": ParagraphStyle("accroche", fontName="Helvetica", fontSize=9.5,
                                   leading=12.5, textColor=colors.black),
        "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=9.5,
                                  leading=12.5, textColor=colors.black, spaceAfter=0),
        "section": ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=9,
                                  leading=12, textColor=GRIS_CLAIR, spaceBefore=4,
                                  spaceAfter=4),
        "sous": ParagraphStyle("sous", fontName="Helvetica-Bold", fontSize=10,
                               leading=13, textColor=colors.black, spaceBefore=6,
                               spaceAfter=3),
        "corps": ParagraphStyle("corps", fontName="Helvetica", fontSize=10,
                                leading=14.4, textColor=colors.black,
                                spaceAfter=7, alignment=TA_JUSTIFY),
        "ital": ParagraphStyle("ital", fontName="Helvetica-Oblique", fontSize=9.2,
                               leading=12.5, textColor=GRIS, spaceAfter=2),
        "puce": ParagraphStyle("puce", fontName="Helvetica", fontSize=10, leading=14,
                               leftIndent=12, bulletIndent=2, spaceAfter=3,
                               alignment=TA_JUSTIFY),
        "note": ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=8,
                               leading=10.4, textColor=GRIS_CLAIR),
        "compact": ParagraphStyle("compact", fontName="Helvetica", fontSize=9.6,
                                  leading=12.2, textColor=colors.black, spaceAfter=0),
        "compactgras": ParagraphStyle("compactgras", fontName="Helvetica-Bold",
                                      fontSize=9.6, leading=12.2, textColor=colors.black,
                                      spaceAfter=0),
    }


# --------------------------------------------------------------------------- #
# Conversion du balisage Markdown en balises ReportLab
# --------------------------------------------------------------------------- #
def echapper(texte):
    texte = texte.replace("&", "&amp;")
    texte = texte.replace("<", "&lt;").replace(">", "&gt;")
    return texte


def en_ligne(texte):
    """**gras** -> <b>, *italique* -> <i>, en échappant le reste."""
    morceaux = re.split(r"(\*\*.+?\*\*|\*[^*]+?\*)", texte)
    sortie = []
    for morceau in morceaux:
        if not morceau:
            continue
        if morceau.startswith("**") and morceau.endswith("**") and len(morceau) > 4:
            sortie.append(f"<b>{echapper(morceau[2:-2])}</b>")
        elif morceau.startswith("*") and morceau.endswith("*") and len(morceau) > 2:
            sortie.append(f"<i>{echapper(morceau[1:-1])}</i>")
        else:
            sortie.append(echapper(morceau))
    return "".join(sortie)


def construire_flux(md_path: Path, st, mode="cv"):
    lignes = md_path.read_text(encoding="utf-8").splitlines()
    flux = []
    i = 0

    while i < len(lignes):
        brut = lignes[i]
        ligne = brut.strip()

        if not ligne:
            i += 1
            continue

        # Bloc compact (en-tête d'adresse)
        if ligne == ":::compact":
            i += 1
            while i < len(lignes) and lignes[i].strip() != ":::":
                contenu = lignes[i].strip()
                if contenu:
                    style = (st["compactgras"] if contenu.startswith("**")
                             else st["compact"])
                    flux.append(Paragraph(en_ligne(contenu), style))
                i += 1
            i += 1
            flux.append(Spacer(1, 5 * mm))
            continue

        # Citation : on ignore les notes internes, on garde les autres en petit
        if ligne.startswith(">"):
            contenu = ligne.lstrip("> ").strip()
            if contenu and "note interne" not in contenu.lower():
                flux.append(Paragraph(en_ligne(contenu), st["note"]))
            i += 1
            continue

        # Séparateur
        if re.fullmatch(r"-{3,}", ligne):
            if mode == "cv":
                flux.append(Spacer(1, 2))
            else:
                flux.append(HRFlowable(width="100%", thickness=0.6, color=FILET,
                                       spaceBefore=6, spaceAfter=8))
            i += 1
            continue

        # Tableau
        if ligne.startswith("|"):
            bloc = []
            while i < len(lignes) and lignes[i].strip().startswith("|"):
                bloc.append(lignes[i].strip())
                i += 1
            rendu = [
                [c.strip() for c in b.strip("|").split("|")]
                for b in bloc
                if not re.fullmatch(r"\|[\s:\-|]+\|", b)
            ]
            if rendu:
                largeur_dispo = 170 * mm if mode == "cv" else 160 * mm
                n = len(rendu[0])
                ratios = {2: [0.36, 0.48, 0.16], 3: [0.40, 0.44, 0.16]}.get(n)
                if ratios:
                    largeurs = [largeur_dispo * r for r in ratios]
                else:
                    largeurs = [largeur_dispo / n] * n
                donnees = []
                for r, cellules in enumerate(rendu):
                    ligne_cells = []
                    for valeur in cellules[:n]:
                        style = ParagraphStyle(
                            "cell", fontName="Helvetica-Bold" if r == 0 else "Helvetica",
                            fontSize=8.3 if mode == "cv" else 9,
                            leading=10.4 if mode == "cv" else 11.6,
                            textColor=NAVY if r == 0 else GRIS,
                        )
                        ligne_cells.append(Paragraph(en_ligne(valeur), style))
                    donnees.append(ligne_cells)
                t = Table(donnees, colWidths=largeurs)
                t.setStyle(TableStyle([
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1.6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("LINEBELOW", (0, 0), (-1, 0), 0.5, FILET),
                    ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#E8EBEE")),
                ]))
                flux.append(t)
                flux.append(Spacer(1, 3))
            continue

        # Titre 1 — nom (CV) ou intitulé (lettre)
        if ligne.startswith("# "):
            texte = ligne[2:].strip()
            if mode == "cv":
                flux.append(Paragraph(en_ligne(texte), st["nom"]))
            else:
                flux.append(Paragraph(
                    f'<font color="#7A8794" size="8">{echapper(texte.upper())}</font>',
                    st["section"]))
            i += 1
            continue

        # Titre 2 — section
        if ligne.startswith("## "):
            texte = ligne[3:].strip()
            if mode == "cv":
                flux.append(Paragraph(en_ligne(texte.upper()), st["section"]))
                flux.append(HRFlowable(width="100%", thickness=1.1, color=GOLD,
                                       spaceBefore=1, spaceAfter=4))
            else:
                flux.append(Paragraph(en_ligne(texte.title()), st["sous"]))
            i += 1
            continue

        # Titre 3
        if ligne.startswith("### "):
            flux.append(Paragraph(en_ligne(ligne[4:].strip()), st["sous"]))
            i += 1
            continue

        # Puce
        if ligne.startswith(("- ", "* ")):
            flux.append(Paragraph(en_ligne(ligne[2:].strip()), st["puce"],
                                  bulletText="•"))
            i += 1
            continue

        # Paragraphe normal — une ligne italique seule devient une légende
        if re.fullmatch(r"\*[^*].*\*", ligne):
            flux.append(Paragraph(en_ligne(ligne), st["ital"]))
            i += 1
            continue

        flux.append(Paragraph(en_ligne(ligne), st["corps"]))
        i += 1

    return flux


# --------------------------------------------------------------------------- #
# Gabarit de document
# --------------------------------------------------------------------------- #
def generer(md_path: Path, pdf_path: Path, mode="cv", auteur=""):
    st = styles_cv() if mode == "cv" else styles_lettre()
    marge_haut = 13 * mm if mode == "cv" else 20 * mm
    marge_lat = 20 * mm if mode == "cv" else 25 * mm
    marge_bas = 13 * mm if mode == "cv" else 18 * mm

    def pied(canvas, doc):
        canvas.saveState()
        if mode == "cv":
            canvas.setFont("Helvetica", 7)
            canvas.setFillColor(GRIS_CLAIR)
            canvas.drawRightString(A4[0] - marge_lat, 8 * mm,
                                   f"GNACADJA Marie Edith — page {doc.page}")
        canvas.restoreState()

    doc = BaseDocTemplate(
        str(pdf_path), pagesize=A4,
        leftMargin=marge_lat, rightMargin=marge_lat,
        topMargin=marge_haut, bottomMargin=marge_bas,
        title=pdf_path.stem, author=auteur,
    )
    cadre = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="corps")
    doc.addPageTemplates([PageTemplate(id="page", frames=[cadre], onPage=pied)])
    doc.build(construire_flux(md_path, st, mode))
    return pdf_path


CIBLES = [
    ("02_Dossiers/01_PAM_Communication_Assistant_Cotonou/CV_PAM_Communication_Assistant.md",
     "02_Dossiers/01_PAM_Communication_Assistant_Cotonou/CV_GNACADJA_Marie_Edith_Communication_Assistant_PAM.pdf",
     "cv"),
    ("02_Dossiers/01_PAM_Communication_Assistant_Cotonou/Lettre_Motivation_PAM_Communication_Assistant.md",
     "02_Dossiers/01_PAM_Communication_Assistant_Cotonou/Lettre_Motivation_GNACADJA_PAM_Communication_Assistant.pdf",
     "lettre"),
    ("02_Dossiers/02_FAO_Stage_Volontariat_Afrique/CV_FAO_Nutrition_Securite_Alimentaire.md",
     "02_Dossiers/02_FAO_Stage_Volontariat_Afrique/CV_GNACADJA_Marie_Edith_FAO_Nutrition.pdf",
     "cv"),
    ("02_Dossiers/02_FAO_Stage_Volontariat_Afrique/Lettre_Motivation_FAO_Stage_Afrique.md",
     "02_Dossiers/02_FAO_Stage_Volontariat_Afrique/Lettre_Motivation_GNACADJA_FAO.pdf",
     "lettre"),
]

if __name__ == "__main__":
    for source, cible, mode in CIBLES:
        src = RACINE / source
        if not src.exists():
            print(f"absent : {source}")
            continue
        generer(src, RACINE / cible, mode=mode, auteur="GNACADJA Marie Edith R. A. M.")
        print(f"généré : {cible}")
