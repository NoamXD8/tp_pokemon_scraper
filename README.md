# Poké Scraper 🐍

## 🎯 Objectif du projet
L’objectif était de mettre en place une infrastructure simple sur **AWS** permettant :
- de scraper les images de Pokémon depuis **Bulbapedia**,
- de les stocker automatiquement dans un **bucket S3 public**,
- en utilisant un script Python exécuté sur une **instance EC2**.

---

## ⚙️ Architecture mise en place
1. Création d’un **utilisateur IAM** (`noam_tp`) avec les droits nécessaires (S3FullAccess + EC2FullAccess).
2. Création d’un **rôle IAM pour EC2**, afin de permettre à l’instance d’accéder directement à S3 sans stocker de clés dans le code.
3. Déploiement d’une **instance EC2 (Ubuntu)** où ont été installés Python et les bibliothèques (`requests`, `beautifulsoup4`, `boto3`).
4. Développement d’un **script Python (`scraper.py`)** qui :
   - scrape les images par génération (Gen I → Gen IX),
   - télécharge temporairement chaque image,
   - l’upload dans S3 via `boto3`,
   - organise les fichiers selon la structure demandée :
     ```
     images/genI/...
     images/genII/...
     ...
     images/genIX/...
     ```
5. Mise en place d’une **Bucket Policy publique** pour autoriser l’accès uniquement au dossier `images/*`.

---

## 🖥️ Fonctionnement du script
- `requests` → récupère le HTML de la page Bulbapedia.  
- `BeautifulSoup` → extrait les URLs d’images et identifie les générations.  
- Téléchargement local temporaire sur l’EC2.  
- `boto3` → envoie les fichiers vers le bucket S3.  
- Suppression des fichiers temporaires après upload.  

Chaque image devient accessible publiquement via une URL, par exemple :  
https://poke-scrapper-noam.s3.eu-north-1.amazonaws.com/images/genI/70px-0001Bulbasaur.png

Et voici la demo du Scraping puis de l'envoie des images de EC" à S3 :
https://drive.google.com/file/d/1fr3lqZjkh9wai2sRtUvv0JASNoSicOvJ/view?usp=sharing

## 🗂️ Architecture

<img width="789" height="366" alt="Capture d’écran 2025-09-04 à 14 07 14" src="https://github.com/user-attachments/assets/88a2bca3-27b5-458b-974a-24da85ef2a8e" />

## 🗂️ IAM, Role et Policy
User IAM que nous utilisons pour éviter d'avoir à utiliser le root qui a donc accès à S3 et EC2 ainsi que IAM temporairement pour la création du rôle de l'EC2
<img width="1000" height="600" alt="Capture d’écran 2025-09-04 à 14 31 06" src="https://github.com/user-attachments/assets/1052b90c-7a4a-46b1-9154-6f3d71644649" />

VOici le role qu'on donne à l'instance pour qu'elle puisse passer les images de EC2 à S3 :
<img width="1000" height="600" alt="Capture d’écran 2025-09-04 à 14 33 02" src="https://github.com/user-attachments/assets/2aa046df-a29d-4843-b6c1-4ef67cd5b8a9" />

