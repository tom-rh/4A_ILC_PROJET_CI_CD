# 4A_ILC_PROJET_CI_CD
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

*Auteurs :* [Baptiste Andres](https://github.com/LeBourguignon) et [Tom Roth](https://github.com/tom-rh)

*Spécialité :* ILC

*Langage :* Python

## Sujet guidé

Consiédrant notre peu d'expérience et les diffiultés que nous avons rencontré en TD, nous avons choisi le sujet guidé en utilisant le langage Python.

Concernant la modélisation des données, nous avons choisi de créer deux classes Personne et Transaction.
Chaque classe possède des attributs permettant d'identifier facilement les instances de ces classes. Elles comprennent également deux méthodes toString() et toJSON() permmettant respectivement de retourner un String et un JSONObject.

## Exemple de commande à reponse JSON

E0 - Afficher toutes les personnes : 
```
url -X GET http://localhost:5000/E0
```
  
E1 - Enregistrer une transaction : 
```
curl -X GET http://localhost:5000/E1/{id1}/{id2}/{date}/{somme}
```
  
E2 - Afficher une liste de toutes les transactions dans l’ordre chronologique : 
```
curl -X GET http://localhost:5000/E2
```
  
E3 - Afficher une liste des transactions dans l’ordre chronologique liées à une personne : 
```
curl -X GET http://localhost:5000/E3/{id}
```
  
E4 - Afficher le solde du compte de la personne : 
```
curl -X GET http://localhost:5000/E4/{id}
```
  
E5 - Importer des données depuis un fichier csv : 
```
curl -X POST -F 'personnes=@{file.csv}' http://localhost:5000/E5/personnes
curl -X POST -F 'transactions=@{file.csv}' http://localhost:5000/E5/transactions
```

E6 - Vérifier l’intégrité des transactions : 
```
curl -X GET http://localhost:5000/E6
```

## Choix de l'algorithme de Hachage

Nous avons choisi le hachage `SHA-256` car il est l'un des algorithmes de hachage les plus répandus et très performants, en plus d'être considéré comme sécurisé encore aujourd'hui.

## Statuts actions

[![Create Docker image](https://github.com/tom-rh/4A_ILC_PROJET_CI_CD/actions/workflows/create_image.yml/badge.svg)](https://github.com/tom-rh/4A_ILC_PROJET_CI_CD/actions/workflows/create_image.yml)
[![Build application](https://github.com/tom-rh/4A_ILC_PROJET_CI_CD/actions/workflows/build_application.yml/badge.svg)](https://github.com/tom-rh/4A_ILC_PROJET_CI_CD/actions/workflows/build_application.yml)
[![Docker push GCR](https://github.com/tom-rh/4A_ILC_PROJET_CI_CD/actions/workflows/docker_push_GCR.yml/badge.svg)](https://github.com/tom-rh/4A_ILC_PROJET_CI_CD/actions/workflows/docker_push_GCR.yml)
