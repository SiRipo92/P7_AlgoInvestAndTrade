# 💼 AlgoInvest&Trade — Résolvez des problèmes en utilisant des algorithmes en Python

**Author:** Sierra Ripoche  
**Formation:** OpenClassrooms – *Développeur d’Application Python*  
**Project 7:** *Résolvez des problèmes en utilisant des algorithmes en Python*  

---

## 🧭 Description du projet

AlgoInvest&Trade est une société financière cherchant à **optimiser ses stratégies d’investissement à court terme** à l’aide d’algorithmes.  
L’objectif de ce projet est de concevoir un programme Python capable de **sélectionner les actions les plus rentables** pour maximiser le profit d’un client après deux ans d’investissement, tout en respectant certaines contraintes.

Le projet est divisé en **trois parties** :

---

## 🧩 Partie 1 — Brute Force : Trouver la solution optimale

**Objectif :**  
Explorer **toutes les combinaisons possibles** d’actions pour déterminer celle offrant le profit total le plus élevé, dans la limite d’un budget fixé à **500 €**.

**Contraintes :**
- Chaque action ne peut être achetée **qu'une seule fois**.
- On ne peut pas acheter de **fraction d’action**.
- Le budget total ne doit **pas dépasser 500 €**.

**Fichier principal :** `bruteforce.py`  
**Données :** `Actions.csv` (fournie dans le dossier `/data`)  
**Colonnes :**
- `Actions #` — Nom de l’action  
- `Coût par action (en euros)` — Prix d’achat de l’action  
- `Bénéfice (après 2 ans)` — Pourcentage de profit sur 2 ans  

**Approche :**
- Lecture du fichier CSV.
- Énumération de toutes les combinaisons possibles d’actions (via `itertools.combinations`).
- Calcul du coût total et du profit total pour chaque combinaison.
- Sélection de la combinaison maximale sous contrainte.

**Limite :**
Cette méthode est exacte, mais **très coûteuse en temps** (`O(2^n)`).  
Elle devient rapidement inutilisable lorsque le nombre d’actions augmente (explosion combinatoire).

---

## ⚙️ Partie 2 — Optimisation : Réduire le temps d’exécution

**Contexte :**  
Après le succès initial, AlgoInvest&Trade souhaite que le programme traite **des ensembles de données beaucoup plus grands** en **moins d’une seconde**.

**Objectif :**  
Concevoir un **algorithme optimisé** qui conserve la précision du résultat tout en réduisant drastiquement le temps de calcul.

**Fichier principal :** `optimized.py`

**Approche proposée :**
- Implémentation d’un algorithme de **programmation dynamique (0/1 knapsack)**.
- Utilisation d’une **discrétisation en centimes** pour conserver la précision monétaire.
- Complexité : `O(n × W)` où `W` = budget exprimé en centimes (ex. 50 000 pour 500 €).
- Temps d’exécution bien plus faible que le brute force.

**Livrables attendus :**
- `optimized.py` — programme Python optimisé.
- **Diaporama de présentation** contenant :
  - Analyse du fonctionnement et de la complexité du brute force.
  - Pseudocode ou organigramme de la solution optimisée.
  - Analyse de la complexité temporelle et mémoire (`Big-O`).
  - Comparaison brute force vs optimisé (temps, mémoire, résultats).

---

## 📊 Partie 3 — Backtesting et analyse des performances

**Contexte :**  
Les conseillers financiers souhaitent comparer les résultats de l’algorithme avec leurs décisions passées sur plusieurs ensembles de données.

**Objectif :**  
Évaluer la précision de l’algorithme en le testant sur des **données historiques** et en comparant les décisions obtenues à celles de Sienna, une conseillère senior.

**Livrables attendus :**
- Programme mis à jour capable de charger différents datasets (ex. `dataset_1.csv`, `dataset_2.csv`).
- Rapport d’exploration et de validation des données.
- Comparaison côte à côte entre :
  - Résultats de l’algorithme.
  - Décisions d’investissement réelles de Sienna.
- Section supplémentaire dans le diaporama avec :
  - Taux de concordance entre les décisions.
  - Analyse des écarts (erreurs, données manquantes, valeurs aberrantes).

---

## 🧠 Objectifs pédagogiques

Ce projet vise à démontrer la capacité à :
1. **Analyser un problème algorithmique** et en extraire les contraintes métiers.
2. **Concevoir et comparer** plusieurs approches algorithmiques (brute force, programmation dynamique).
3. **Optimiser un programme Python** en termes de performance et de complexité.
4. **Documenter** et **présenter** clairement une démarche de résolution algorithmique.
5. **Tester et valider** les résultats à l’aide de jeux de données réels et simulés.

---

## 🗂️ Structure du projet
```
AlgoInvestAndTrade/
├─ data/
│  └─ Actions.csv
├─ bruteforce.py
├─ optimized.py
├─ README.md
└─ requirements.txt
```

## 🧰 Installation et exécution

### 1. Cloner le projet
```bash
git clone https://github.com/SiRipo92/AlgoInvestAndTrade.git
cd AlgoInvestAndTrade
```

### 2. Créer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate     # macOS / Linux
source .venv\Scripts\activate  # Windows PowerShell
```

### 3. Installer les dépendances (si nécessaires)
```bash
pip install -r requirements.txt
```

### 4. Exécuter le programme

#### - Version brute force : 
```bash
python bruteforce.py
```

#### - Version optimisée :
```bash
python optimized.py
```

## 📈 Sortie attendue

Le programme affiche :

- Le profit total maximal après 2 ans.

- Le coût total du portefeuille sélectionné.

- La liste des actions à acheter.

Un fichier best_investment.csv est généré dans le répertoire racine pour archivage.

