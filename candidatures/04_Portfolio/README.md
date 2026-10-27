# PORTFOLIO — MODE D'EMPLOI

**`Portfolio_GNACADJA_Marie_Edith.pdf`** — 7 pages A4 paysage, 2,2 Mo.

---

## Ce qu'il contient

| Page | Réalisation | Contexte |
|---|---|---|
| 1 | Couverture | — |
| 2 | **Logo du Benin Science Leadership Program (B-SLP)** | Programme de leadership scientifique, Université d'Abomey-Calavi |
| 3 | **Série d'attestations** | Projet MINNAGAN — Union européenne / Erasmus+, avril 2024 |
| 4 | **Tableau de formation pédagogique** | URMAPHA / EPAC, Université d'Abomey-Calavi |
| 5 | **Étiquette produit PolFFree-AC** | Charbon actif pour l'eau, mis au point par l'URMAPHA |
| 6 | **Série de visuels réseaux sociaux** | Campagne personnelle, format 1080 × 1080 |
| 7 | Compétences et contact | — |

---

## Deux points à valider avant d'envoyer ce portfolio

### 1. Le logo B-SLP est-il bien de vous ?

Il se trouvait dans une archive nommée `Benin science leadership program.zip`, à côté des attestations que vous avez visiblement produites. J'ai considéré qu'il était de vous — **mais confirmez-le.** C'est la pièce d'ouverture du portfolio : si elle n'était pas de vous, cela s'entendrait en entretien et abîmerait tout le reste.

### 2. Garder ou retirer la série « Et si tu mourais maintenant ? »

La page 6 présente une série de visuels d'inspiration chrétienne, avec des versets bibliques. Techniquement, elle démontre bien ce qu'un recruteur cherche : une série cohérente, une palette tenue, des gabarits réutilisables.

Mais elle parle de foi, pas de nutrition. Pour une candidature au PAM, à la FAO ou à l'ANAN, elle peut :
- distraire du reste du portfolio ;
- être mal reçue par certains recruteurs ;
- ou, à l'inverse, humaniser votre profil si l'employeur est une organisation confessionnelle.

**Mon avis : retirez-la pour les candidatures ONU et santé publique. Gardez-la si vous postulez auprès d'une structure confessionnelle (Caritas, Secours catholique, cliniques confessionnelles, ONG d'église), où elle devient un atout.**

Pour la retirer : ouvrez `outils/construire_portfolio.py`, mettez `INCLURE_SERIE_FOI = False`, puis relancez le script. Le portfolio passe à 6 pages.

---

## Comment regénérer ou modifier le portfolio

```bash
cd candidatures
python3 04_Portfolio/outils/construire_portfolio.py
```

**Dépendances :** `pip install Pillow reportlab`

### Ajouter une réalisation

1. Déposez le visuel dans `04_Portfolio/sources/`, nommé `08_mon_travail.png`
2. Dans `construire_portfolio.py` :
   - ajoutez la ligne dans `PLAN_IMAGES` : `("08_mon_travail.png", "08_mon_travail.png", None)`
   - ajoutez un bloc dans `PROJETS` en suivant le modèle existant
3. Relancez le script

### Ce que le script fait automatiquement

- redimensionne les visuels à 1800 px maximum, pour un PDF léger et net ;
- **masque les noms de personnes** sur les attestations nominatives (page 3) — un portfolio ne doit pas diffuser les noms de tiers sans leur accord ;
- conserve les ratios des images et compose les pages.

---

## Les fichiers du dossier

```
04_Portfolio/
├── Portfolio_GNACADJA_Marie_Edith.pdf   ← à envoyer
├── sources/                              ← les 7 visuels sélectionnés
├── preparees/                            ← versions retravaillées (générées)
└── outils/construire_portfolio.py        ← script de génération
```

Les archives d'origine (`Benin science leadership program.zip`, `Copie de BSLP.zip`, `ETIQUETTES.zip`, `ET SI TU MOURRAIS.zip`) et le fichier `Citation.png` restent sur la branche `main` du dépôt : ils contiennent 34 visuels, dont la plupart ne sont pas retenus ici. Le portfolio en présente 7, sélectionnés pour leur pertinence.

---

## Comment l'envoyer

- **Ne jamais** joindre le portfolio en pièce jointe d'une première candidature si l'employeur ne l'a pas demandé — cela alourdit le message. Mentionnez-le dans le CV (« portfolio disponible sur demande ») et dans la lettre.
- **Si un portfolio est demandé** : envoyez le PDF tel quel, nommé `GNACADJA_Marie_Edith_Portfolio.pdf`. Il fait 2,2 Mo, ce qui passe les filtres de taille des boîtes mail.
- **Pour les métiers de la communication** (PAM Communication Assistant, consultances graphisme), joignez-le systématiquement : c'est votre meilleure pièce.
