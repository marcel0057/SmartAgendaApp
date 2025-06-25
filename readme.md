# AgendaPlus

AgendaPlus est une application web de gestion d'agenda moderne, conçue pour organiser ton temps avec élégance. Elle permet aux utilisateurs de créer, modifier, et supprimer des rendez-vous, de gérer des tâches, et de recevoir des rappels vocaux personnalisés via l'API d'Eleven Labs. L'application utilise Flask pour le backend, Supabase pour la gestion des données et l'authentification, et une interface front-end intuitive avec un design responsive.

## Fonctionnalités

- **Authentification** : Inscription et connexion sécurisées via Supabase Auth.
- **Gestion des rendez-vous** : Ajout, modification, et suppression de rendez-vous, avec stockage dans Supabase.
- **Tâches** : Affichage et gestion de tâches (actuellement statiques, avec possibilité d'extension dynamique).
- **Notifications** : Notifications navigateur pour les rendez-vous du lendemain.
- **Rappels vocaux** : Génération de rappels vocaux via l'API d'Eleven Labs, envoyés quotidiennement à 18h00.
- **Interface utilisateur** : Tableau de bord moderne avec sidebar, calendrier, et cartes de statistiques.

## Arborescence du projet
SmartAgendaApp/
├── app.py                 # Application Flask principale
├── templates/            # Fichiers HTML
│   ├── index.html        # Page d'accueil publique
│   ├── login.html        # Page de connexion
│   ├── register.html     # Page d'inscription
│   ├── dashboard.html    # Tableau de bord
│   ├── ajouter_rdv.html  # Formulaire d'ajout de rendez-vous
│   └── modifier_rdv.html # Formulaire de modification/suppression
├── static/               # Fichiers statiques (CSS, JS, images, audio)
│   ├── styles.css        # Styles pour la page d'accueil
│   ├── login.css         # Styles pour la connexion
│   ├── register.css      # Styles pour l'inscription
│   ├── dashboard.css     # Styles pour le tableau de bord
│   ├── dashboard.js      # Scripts pour le tableau de bord
│   ├── script.js         # Scripts pour les notifications
│   └── audio/            # Fichiers audio générés
├── utils/                # Utilitaires
│   ├── notifications.py  # Gestion des notifications
│   └── eleven_labs.py    # Gestion des rappels vocaux
├── requirements.txt      # Dépendances Python
├── .env                  # Variables d'environnement
├── .gitignore            # Fichiers à ignorer par Git

## Prérequis

- Python 3.8+
- Compte Supabase (pour l'authentification et la base de données)
- Compte Eleven Labs (pour les rappels vocaux)
- Git (pour cloner le projet)

## Installation

1. **Cloner le dépôt** :

   git clone https://github.com/marcel0057/SmartAgendaApp.git
   cd SmartAgendaApp

2. **Créer et activer un environnement virtuel** :
    python -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate

3. **Installer les dépendances** :
    pip install -r requirements.txt