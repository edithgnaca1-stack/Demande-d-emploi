# CANDIDATURES — MODE D'EMPLOI

Dossier de recherche d'emploi de **Marie Edith R. A. M. GNACADJA** — nutrition, santé publique, communication.
Établi le **27 octobre 2026** à partir du CV du dépôt (`Marie Edith  (1).pdf`) et d'une vérification des offres sur les sites officiels.

---

## Par où commencer

**1. Lisez `00_Tableau_de_bord.md`** — c'est le document central : les offres examinées, leur statut réel, et les 3 à traiter en priorité.

**1 bis. Pour le fichier `Offres d'emploi.docx` :** `03_Veille/INVENTAIRE_COMPLET_DU_FICHIER_OFFRES.md` reprend **les 85 opportunités qu'il contient, une par une**, avec un verdict et un motif pour chacune.

**2. Répondez à `01_Profil/A_CONFIRMER_AVANT_ENVOI.md`** — 12 questions. Quatre d'entre elles sont bloquantes (titre du diplôme, obtention du Master 2, statut des fonctions URMAPHA, pièces administratives). Sans ces réponses, certaines candidatures ne doivent pas partir.

**3. Utilisez les dossiers de `02_Dossiers/`** — chacun contient un CV, une lettre et une fiche d'offre.

---

## Structure

```
candidatures/
├── README.md                                  ← ce fichier
├── 00_Tableau_de_bord.md                      ← tableau récapitulatif + priorités + plan sur 3 mois
├── 01_Profil/
│   ├── PROFIL_SOURCE_DE_VERITE.md             ← tout ce que le CV prouve… et ce qu'il ne prouve pas
│   └── A_CONFIRMER_AVANT_ENVOI.md             ← points confirmés et décisions restantes
├── 02_Dossiers/
│   ├── 01_PAM_Communication_Assistant_Cotonou/    🔴 clôture 5 nov. 2026
│   │   └── PRET_A_DEPOSER_CE_SOIR.md              ← pas à pas du dépôt Workday
│   ├── 02_FAO_Stage_Volontariat_Afrique/          🟠 clôture 31 déc. 2026
│   │   ├── REMPLIR_L_EXPERIENCE_FAO.md           ← les 4 expériences à saisir sur le portail
│   │   └── TEXTES_A_COPIER_FAO.txt               ← mêmes textes, en clair, pour copier-coller
│   └── 03_PAM_VNU_Communautaire_Urgent/           ⚫ analyse d'inéligibilité (28 oct. 2026)
├── 03_Veille/
│   ├── SOURCES_OFFICIELLES_ET_PLAN_DE_VEILLE.md  ← 9 sources + routine du lundi
│   ├── INVENTAIRE_COMPLET_DU_FICHIER_OFFRES.md   ← les 85 opportunités du fichier, une par une, avec verdict
│   └── OPTIONS_A_COUT_ZERO_ET_MOBILITE.md        ← affectation non rémunérée : coûts réels et alternatives
└── 04_Portfolio/
    ├── Portfolio_GNACADJA_Marie_Edith.pdf        ← 7 pages, à joindre aux candidatures communication
    ├── README.md                                 ← 2 points à valider avant envoi
    ├── sources/                                  ← les visuels sélectionnés
    └── outils/construire_portfolio.py            ← régénère le PDF
```

---

## Fichiers prêts à envoyer

Les CV et lettres existent en trois formats :
- **`.pdf`** — ⭐ **la version à envoyer**. CV 2 pages, lettres 1 page, prêts à téléverser ;
- **`.docx`** — pour retoucher la mise en forme dans Word si besoin ;
- **`.md`** — la version de travail dans le dépôt.

Tout est régénéré après une modification du `.md` :

```bash
cd candidatures
python3 outils/generer_pdf.py     # PDF finaux (reportlab)
python3 outils/generer_docx.py    # versions Word (python-docx)
```

*(dépendances : `pip install reportlab python-docx`)*

---

## Les trois principes de ce dossier

**1. Rien n'est inventé.**
Chaque expérience, diplôme, outil ou compétence provient du CV. Aucune expérience salariée n'est revendiquée, aucun logiciel non maîtrisé n'est mentionné, aucune durée d'expérience n'est gonflée. Les documents sont conçus pour tenir devant un recruteur qui demanderait des preuves.

**2. Les écarts sont écrits noir sur blanc.**
Quand votre profil ne correspond pas, le dossier le dit — et explique s'il faut postuler quand même. C'est plus utile qu'une liste d'offres présentées comme autant de chances.

**3. Le statut de chaque offre est daté.**
Tout ce qui figure ici a été vérifié le 27 octobre 2026. Au-delà de deux semaines, revérifiez sur la source officielle : les annonces béninoises se ferment vite.

---

## Ce que dit le diagnostic, en trois phrases

Votre profil est solide sur l'**analyse de données de santé** et l'**éducation nutritionnelle** — trois analyses de situation menées en zone sanitaire, un DU Senghor, un Master à l'IRSP. Mais il n'a **aucune expérience salariée**, ce qui vous ferme pour l'instant les postes exigeant 2 à 5 ans.

Votre levier immédiat n'est donc pas le poste de nutritionniste : c'est la **consultance en production de supports de santé** (boîtes à images, affiches, modules, mise en page), qui se juge sur portfolio et non sur années d'expérience.

Les voies d'entrée réalistes dans le système ONU sont, dans l'ordre : **volontariat en ligne** (gratuit, immédiat), **stage FAO**, puis **consultances**, puis **VNU communautaire** une fois 2 ans d'expérience accumulés.

Et surtout : **n'achetez pas votre entrée.** Une affectation non rémunérée hors du Bénin coûterait entre 1,65 et 3,75 millions de FCFA pour six mois — soit deux à trois fois ce que rapporterait un volontariat rémunéré. Le volontariat **en ligne** produit la même ligne sur un CV, pour zéro franc. Détail du calcul dans `03_Veille/OPTIONS_A_COUT_ZERO_ET_MOBILITE.md`.

---

## Prochaines actions, dans l'ordre

| Quand | Quoi |
|---|---|
| ✅ Fait | Parcours vérifié : le CV est exact, les pièces sont en votre possession |
| Cette semaine | **Créer le profil app.unv.org** et viser une mission de **volontariat en ligne** (coût zéro, référence ONU) |
| 30 octobre | Inscription au répertoire du Ministère de la Communication (gratuit, 5 min, utile pour la visibilité) |
| 2-4 novembre | Envoyer la candidature PAM Communication Assistant (exporter les `.docx` en PDF) |
| Novembre | Constituer un portfolio PDF de 6-8 pages |
| Novembre | Soumettre la candidature FAO — **le stage**, pas le volontariat non rémunéré |
| Chaque lundi | 20 minutes de veille sur les 9 sources |

---

## Note sur le document `Offres d'emploi.docx`

Ce document daté du 22 octobre 2026 recense environ 90 annonces, dont **une douzaine seulement** concernent votre profil. Il mélange des postes béninois accessibles et des postes étrangers inaccessibles (autorisation de travail exigée), et plusieurs de ses dates limites étaient déjà dépassées cinq jours après sa rédaction. Le détail de l'analyse figure en section 2 du tableau de bord. Ce document n'est pas supprimé : il reste dans le dépôt à titre d'archive.
