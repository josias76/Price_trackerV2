# Application de Suivi des Prix - Version Streamlit avec Navigation de Fichiers

## Description

Cette application Streamlit permet de suivre et d'analyser l'évolution des prix de différents produits organisés par catégories et sous-catégories. Elle offre une interface utilisateur moderne et interactive pour naviguer dans la structure de dossiers et sélectionner des fichiers Excel pour l'analyse des données de prix.

## Fonctionnalités

### 🗂️ **Navigation Interactive des Fichiers**
- Navigation hiérarchique dans la structure de dossiers `data/`
- Expansion/réduction des dossiers avec interface intuitive
- Sélection directe des fichiers Excel existants
- Affichage de la structure complète des données disponibles

### 🔍 **Filtrage Avancé**
- Filtres par marque, type, gramage, origine, format
- Filtres par plage de prix (minimum/maximum)
- Combinaison de plusieurs filtres simultanément
- Interface intuitive avec sélecteurs déroulants
- Mise à jour automatique des filtres selon les données du fichier sélectionné

### 📊 **Visualisations Interactives**
- Graphiques de l'évolution des prix dans le temps
- Graphiques interactifs avec Plotly
- Tooltips détaillés au survol
- Zoom et navigation dans les graphiques
- Adaptation automatique selon les données sélectionnées

### 📈 **Statistiques en Temps Réel**
- Prix moyen, minimum et maximum
- Nombre total d'entrées
- Statistiques mises à jour en temps réel selon les filtres
- Métriques visuelles avec indicateurs colorés

### 📋 **Tableau de Données**
- Affichage des données filtrées
- Tri par colonnes
- Interface responsive
- Export des données filtrées en CSV

## Structure des Données

L'application navigue automatiquement dans une structure de fichiers Excel organisée comme suit :

```
data/
├── CATEGORIE/
│   ├── SOUS_CATEGORIE/
│   │   ├── SOUS_SOUS_CATEGORIE/
│   │   │   └── produit.xlsx
```

### Exemple de Structure
```
data/
├── ASSURANCE/
│   ├── AUTO/
│   │   └── prime_mensuelle.xlsx
│   └── HABITATION/
│       └── prime_mensuelle.xlsx
├── MANUFACTURING/
│   └── MANUFACTURING_ALIMENTAIRE/
│       └── ALIMENTAIRE_GENERALE/
│           └── riz.xlsx
└── TELECOM/
    ├── INTERNET/
    │   └── abonnement_fibre.xlsx
    └── MOBILE/
        └── forfait_standard.xlsx
```

### Format des Fichiers Excel

Chaque fichier Excel doit contenir les colonnes suivantes :
- **marque** : Marque du produit
- **type** : Type/variété du produit
- **gramage** : Poids ou quantité
- **prix** : Prix en euros
- **origine** : Pays ou région d'origine
- **date** : Date de relevé des prix
- **format** : Format d'emballage

## Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## Utilisation

### Démarrage de l'application

```bash
cd streamlit_price_tracker
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

### Navigation et Utilisation

1. **Navigation dans les fichiers** : 
   - Utilisez la barre latérale pour naviguer dans la structure de dossiers
   - Cliquez sur les dossiers pour les expandre/réduire
   - Cliquez sur un fichier Excel pour le sélectionner

2. **Analyse des données** : 
   - Une fois un fichier sélectionné, les données sont automatiquement chargées
   - Utilisez les filtres pour affiner les données affichées
   - Consultez les statistiques, graphiques et tableau de données

3. **Filtrage** :
   - Les filtres s'adaptent automatiquement aux données du fichier sélectionné
   - Combinez plusieurs filtres pour des analyses précises
   - Les résultats se mettent à jour en temps réel

4. **Export** :
   - Téléchargez les données filtrées au format CSV
   - Le nom du fichier inclut automatiquement le nom du produit analysé

## Structure du Projet

```
streamlit_price_tracker/
├── app.py                 # Application principale Streamlit
├── data_processing.py     # Fonctions de traitement des données
├── data/                  # Dossier contenant les fichiers de données
├── README.md             # Documentation
└── requirements.txt      # Dépendances Python
```

## Fonctionnalités Techniques

### Navigation Hiérarchique
- Lecture automatique de la structure de dossiers
- Interface expandable/réductible pour chaque niveau
- Détection automatique des fichiers Excel

### Cache des Données
- Utilisation du cache Streamlit pour optimiser les performances
- Rechargement automatique lors de modifications des données
- Cache intelligent de la structure des dossiers

### Interface Responsive
- Design adaptatif pour différentes tailles d'écran
- Interface optimisée pour desktop et mobile
- Barre latérale redimensionnable

### Gestion d'Erreurs
- Messages d'erreur informatifs
- Gestion des fichiers manquants ou corrompus
- Validation des données d'entrée
- Affichage des erreurs de chargement

## Personnalisation

### Ajout de Nouveaux Fichiers
1. Placez le fichier Excel dans la structure de dossiers appropriée
2. Actualisez la page (F5) ou redémarrez l'application
3. Le nouveau fichier apparaîtra automatiquement dans la navigation

### Modification de la Structure
- L'application s'adapte automatiquement à toute modification de la structure de dossiers
- Aucune configuration manuelle n'est nécessaire
- Les nouveaux dossiers et fichiers sont détectés automatiquement

## Dépannage

### Problèmes Courants

**L'application ne démarre pas :**
- Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`
- Assurez-vous d'être dans le bon répertoire : `cd streamlit_price_tracker`

**Aucun fichier n'apparaît dans la navigation :**
- Vérifiez que le dossier `data/` existe et contient des fichiers Excel
- Vérifiez que les fichiers ont l'extension `.xlsx`
- Actualisez la page (F5)

**Erreurs de chargement des données :**
- Vérifiez que les fichiers Excel ne sont pas corrompus
- Assurez-vous que les colonnes requises sont présentes
- Vérifiez le format des données (dates, prix numériques)

**Interface qui ne répond pas :**
- Actualisez la page (F5)
- Redémarrez l'application Streamlit
- Vérifiez les logs dans le terminal

## Avantages de cette Version

✅ **Navigation intuitive** : Parcourez facilement vos fichiers de données  
✅ **Sélection flexible** : Choisissez n'importe quel fichier Excel existant  
✅ **Adaptation automatique** : Les filtres s'adaptent aux données de chaque fichier  
✅ **Interface moderne** : Design professionnel et responsive  
✅ **Performance optimisée** : Cache intelligent et chargement rapide  

## Support

Pour toute question ou problème :
1. Consultez les logs de l'application dans le terminal
2. Vérifiez que la structure des données respecte le format attendu
3. Assurez-vous que les dépendances sont correctement installées

## Version

Version 2.0 - Application Streamlit de suivi des prix avec navigation de fichiers, filtrage avancé et graphiques interactifs.

---

*Application développée avec Streamlit, Pandas et Plotly*

