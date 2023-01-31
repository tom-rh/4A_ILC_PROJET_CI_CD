from flask import Flask, request
from operator import attrgetter

import sys
import csv
import os

app = Flask(__name__)

class Personne:
    def __init__(self, id, nom, prenom, solde):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.solde = solde

    def toJSON(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "solde": self.solde
        }

class Transaction:
    def __init__(self, p1, p2, date, somme):
        self.p1 = p1
        self.p2 = p2
        self.date = date
        self.somme = somme

        p1.solde -= somme
        p2.solde += somme

    def toJSON(self):
        return {
            "p1": self.p1.toJSON(),
            "p2": self.p2.toJSON(),
            "date": self.date,
            "somme": self.somme
        }

personnes = []

transactions = []

# Requete JSON

@app.route("/", methods=['GET'])
def donnerPersonnes():
    return [personne.toJSON() for personne in personnes]



@app.route("/E1/<int:id1>/<int:id2>/<date>/<int:somme>", methods=['GET', 'POST'])
def ajouterTransaction(id1, id2, date, somme):
    transaction = Transaction(personnes[int(id1)], personnes[int(id2)], date, int(somme))
    transactions.append(transaction)
    transactions.sort(key=attrgetter('date'))
    return transaction.toJSON()



@app.route("/E2", methods=['GET'])
def donnerTransactions():
    return [transaction.toJSON() for transaction in transactions]



@app.route("/E3/<int:id>", methods=['GET'])
def donnerTransactionsPersonne(id):
    out = []
    for transaction in transactions:
        if transaction.p1 == personnes[int(id)] or transaction.p2 == personnes[int(id)]:
            out.append(transaction.toJSON())
    return out



@app.route("/E4/<int:id>", methods=['GET'])
def donnerSoldePersonne(id):
    return { "solde": personnes[int(id)].solde }



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
