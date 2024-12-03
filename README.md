# D-T-F Tool 🛠️

![License](https://img.shields.io/github/license/ErrorNoName/D-T-F?style=flat-square)
![Version](https://img.shields.io/github/v/release/ErrorNoName/D-T-F?style=flat-square)
![Issues](https://img.shields.io/github/issues/ErrorNoName/D-T-F?style=flat-square)

**D-T-F Tool** est un outil puissant et interactif permettant de **générer, tester, et valider des tokens Discord** avec une interface utilisateur avancée et intuitive basée sur **Rich**.

---

## 📋 Fonctionnalités

- **Vérification automatique des mises à jour** : Le script s'assure qu'il est toujours à jour en récupérant la dernière version depuis GitHub.
- **Génération de tokens** : Transformez un ID fourni en plusieurs tokens générés aléatoirement.
- **Vérification des tokens** : Testez automatiquement les tokens générés pour déterminer leur validité.
- **Interface utilisateur dynamique** :
  - Logo stylisé.
  - Boîtes interactives et tableaux enrichis grâce à Rich.
  - Progression en temps réel avec feedback visuel.
- **Enregistrement des résultats** :
  - Tokens valides enregistrés dans le fichier `hit.txt` pour une gestion facile.

---

## 🚀 Installation et Prérequis

### Prérequis
- **Python** : Version 3.8 ou supérieure.
- **Dépendances** :
  - `requests`
  - `rich`
  - `colorama`

Installez les dépendances nécessaires avec la commande suivante :

```bash
pip install -r requirements.txt
```

### Installation
Clonez le dépôt GitHub et accédez au répertoire du projet :

```bash
git clone https://github.com/ErrorNoName/D-T-F.git
cd D-T-F
```

---

## 🛠️ Utilisation

Exécutez le script avec Python :

```bash
python main.py
```

### Fonctionnement interactif
1. **Vérification des mises à jour** : Le script s'assure que vous utilisez la dernière version.
2. **Saisie de l'ID** : Entrez votre ID pour générer les tokens.
3. **Génération et test des tokens** : Les tokens générés sont testés automatiquement via l'API Discord.
4. **Affichage des résultats** :
   - Liste des tokens valides et invalides sous forme de tableaux interactifs.
   - Tokens valides enregistrés dans `hit.txt`.

---

## 📂 Structure des fichiers

```
D-T-F/
├── main.py             # Script principal
├── requirements.txt    # Liste des dépendances Python
├── hit.txt             # Fichier généré contenant les tokens valides
├── README.md           # Documentation
```

---

## 🌟 Fonctionnalités avancées

### 1. Vérification des mises à jour
Le script compare le contenu local avec celui du dépôt GitHub et applique les mises à jour automatiquement.

### 2. Génération de tokens
- Les tokens sont construits en combinant l'ID fourni avec des chaînes aléatoires.
- Format des tokens : `<id_to_token>.<random_4>.<random_25>`.

### 3. Vérification via l'API Discord
- Le script envoie des requêtes à l'API Discord (`/api/v9/auth/login`) pour tester la validité des tokens.

### 4. Interface Rich
- Utilisation de **Rich** pour des tableaux, des panneaux, et une mise en page visuelle moderne.

---

## ⚠️ Avertissements

- **Utilisation responsable** : Cet outil est à des fins éducatives uniquement. Ne l'utilisez pas pour des activités non conformes aux Conditions d'Utilisation de Discord.
- **API Discord** : Discord peut détecter un comportement anormal et bloquer les requêtes abusives.

---

## 🤝 Contribution

Les contributions sont bienvenues ! Suivez les étapes ci-dessous pour contribuer :

1. Forkez le projet.
2. Créez une branche : `git checkout -b feature/nom-de-la-feature`.
3. Commitez vos modifications : `git commit -m 'Ajout d'une nouvelle fonctionnalité'`.
4. Poussez vos modifications : `git push origin feature/nom-de-la-feature`.
5. Soumettez une Pull Request.

---

## 📜 Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](./LICENSE) pour plus d'informations.

---

## 📧 Contact

Si vous avez des questions ou des idées, vous pouvez me contacter via [mon profil GitHub](https://github.com/ErrorNoName).

---

_"Créer, tester, et innover."_ - ErrorNoName
