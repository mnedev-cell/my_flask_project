my_flask_project/
│
├── app/
│   ├── __init__.py          # Fichier d'initialisation de l'application
│   ├── routes.py            # Définitions des routes (endpoints)
│   ├── models.py            # Modèles de base de données (si SQLAlchemy ou autre ORM)
│   ├── static/              # Fichiers statiques (CSS, JavaScript, images)
│   │   ├── css/
│   │   └── js/
│   └── templates/           # Templates HTML (pour Flask Jinja2)
│       ├── base.html        # Template de base (héritage pour les autres pages)
│       └── index.html       # Page d'accueil
│
├── config.py                # Configuration de l'application (base de données, secrets)
├── run.py                   # Script pour démarrer l'application Flask
├── requirements.txt         # Liste des dépendances Python (pour `pip install`)
├── mydatabase.db            # Base de données SQLite
├── README.md                # Documentation du projet
└── .env                     # Variables d'environnement (ex. : clés API, config sensibles)

mkdir -p my_flask_project/static/css
mkdir -p my_flask_project/static/js
mkdir -p my_flask_project/templates
