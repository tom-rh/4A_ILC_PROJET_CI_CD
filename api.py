from flask import Flask, request
from operator import attrgetter

import sys
import csv
import os
import hashlib

app = Flask(__name__)

# Class Personne

class Personne:
    def __init__(self, id, nom, prenom, solde):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.solde = solde

    def toString(self):
        return str(self.id) + ' : ' + self.nom + ' ' + self.prenom + ' ' + str(self.solde)

    def toJSON(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "solde": self.solde
        }

# Class Transaction

class Transaction:
    def __init__(self, p1, p2, date, somme):
        self.p1 = p1
        self.p2 = p2
        self.date = date
        self.somme = somme

        p1.solde -= somme
        p2.solde += somme

        input = str(p1.id) + str(p2.id) + str(somme)
        sha256 = hashlib.sha256()
        sha256.update(input.encode())
        self.hash = sha256.hexdigest()

    def toString(self):
        return self.p1.nom + ' -> ' +  self.p2.nom + ' ' +  self.date + ' ' + str(self.somme) + ' ' + self.hash

    def toJSON(self):
        return {
            "p1": self.p1.toJSON(),
            "p2": self.p2.toJSON(),
            "date": self.date,
            "somme": self.somme,
            "hash": self.hash
        }

# Initialisier les tableaux de données

personnes = []

transactions = []

# Requete HTML

@app.route("/")
@app.route("/personnes")
def afficherPersonnes():
    out = "<h3>Liste de Personne :</h3>\n"
    for personne in personnes:
        out += "<p>" + personne.toString() + "</p>\n"
    return out
    # Navigateur : http://localhost:5000
    # Navigateur : http://localhost:5000/personnes

@app.route("/transactions")
def afficherTransactions():
    out = "<h3>Liste de Transaction :</h3>\n"
    for transaction in transactions:
        out += "<p>" + transaction.toString() + "</p>\n"
    return out
    # Navigateur : http://localhost:5000/transactions

@app.route("/profil/<int:id>")
def afficherProfil(id):
    out = "<h3>" + personnes[int(id)].toString() + "</h3>\n"
    for transaction in transactions:
        if transaction.p1 == personnes[int(id)] or transaction.p2 == personnes[int(id)]:
            out += "<p>" + transaction.toString() + "</p>\n"
    return out
    # Navigateur : http://localhost:5000/profil/0

# Requete JSON

## E0 - Afficher toutes les personnes
@app.route("/E0", methods=['GET'])
def donnerPersonnes():
    return [personne.toJSON() for personne in personnes]
    # curl -X GET http://localhost:5000/E0

## E1 - Enregistrer une transaction
@app.route("/E1/<int:id1>/<int:id2>/<date>/<int:somme>", methods=['GET', 'POST'])
def ajouterTransaction(id1, id2, date, somme):
    transaction = Transaction(personnes[int(id1)], personnes[int(id2)], date, int(somme))
    transactions.append(transaction)
    transactions.sort(key=attrgetter('date'))
    return transaction.toJSON()
    # curl -X GET http://localhost:5000/E1/0/1/2023-09-01/100

## E2 - Afficher une liste de toutes les transactions dans l’ordre chronologique
@app.route("/E2", methods=['GET'])
def donnerTransactions():
    return [transaction.toJSON() for transaction in transactions]
    # curl -X GET http://localhost:5000/E2

## E3 - Afficher une liste des transactions dans l’ordre chronologique liées à une personne
@app.route("/E3/<int:id>", methods=['GET'])
def donnerTransactionsPersonne(id):
    out = []
    for transaction in transactions:
        if transaction.p1 == personnes[int(id)] or transaction.p2 == personnes[int(id)]:
            out.append(transaction.toJSON())
    return out
    # curl -X GET http://localhost:5000/E3/0

## E4 - Afficher le solde du compte de la personne
@app.route("/E4/<int:id>", methods=['GET'])
def donnerSoldePersonne(id):
    return { "solde": personnes[int(id)].solde }
    # curl -X GET http://localhost:5000/E4/0

## E5 - Importer des données depuis un fichier csv
## Importer des personnes
@app.route("/E5/personnes", methods=['POST'])
def chargerPersonnes():
    if request.files:
        file = request.files['personnes']
        filepath = os.path.join(file.filename)
        file.save(filepath)

        with open(filepath) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                personnes.append(Personne(len(personnes), row[0], row[1], int(row[2])))
    else:
        print("Erreur")    
    return donnerPersonnes()
    # curl -X POST -F 'personnes=@personnes.csv' http://localhost:5000/E5/personnes

## Importer des transactions
@app.route("/E5/transactions", methods=['POST'])
def chargerTransactions():
    if request.files:
        file = request.files['transactions']
        filepath = os.path.join(file.filename)
        file.save(filepath)

        with open(filepath) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                ajouterTransaction(int(row[0]), int(row[1]), row[2], int(row[3]))
    else:
        print("Erreur")      
    return donnerTransactions()
    # curl -X POST -F 'transactions=@transactions.csv' http://localhost:5000/E5/transactions

## E6 - Vérifier l’intégrité des transactions
@app.route("/E6", methods=['GET'])
def verifierIntegriteTransactions():
    out = True
    for transaction in transactions:
        input = str(transaction.p1.id) + str(transaction.p2.id) + str(transaction.somme)
        sha256 = hashlib.sha256()
        sha256.update(input.encode())
        hash = sha256.hexdigest()
        out = (hash == transaction.hash)
    return {
        "integrite": out
    }
    # curl -X GET http://localhost:5000/E6

# Chargement des données

with open("personnes.csv") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                personnes.append(Personne(len(personnes), row[0], row[1], int(row[2])))

with open("transactions.csv") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                ajouterTransaction(int(row[0]), int(row[1]), row[2], int(row[3]))