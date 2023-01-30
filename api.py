from flask import Flask

from operator import attrgetter

import json

app = Flask(__name__)

class Personne:
    def __init__(self, id, nom, prenom, solde):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.solde = solde

class Transaction:
    def __init__(self, p1, p2, date, somme):
        self.p1 = p1
        self.p2 = p2
        self.date = date
        self.somme = somme

        p1.solde -= somme
        p2.solde += somme

personnes = [
    Personne(0, "Andres", "Baptiste", 1000000000), 
    Personne(1, "Roth", "Tom", 0),
    Personne(2, "Thomas", "Gauthier", -100)]

transactions = []

@app.route("/")
def afficherPersonnes():
    return json.dumps(personnes, default=lambda o: o.__dict__, sort_keys=True, indent=4)

@app.route("/E1/<id1>/<id2>/<date>/<somme>")
def transaction(id1, id2, date, somme):
    transactions.append(Transaction(personnes[int(id1)], personnes[int(id2)], date, int(somme)))
    transactions.sort(key=attrgetter('date'))

@app.route("/E2")
def afficherTransactions():
    return json.dumps(transactions, default=lambda o: o.__dict__, sort_keys=True, indent=4)

@app.route("/E3/<id>")
def afficherTransactionsPersonne(id):
    out = []
    for transaction in transactions:
        if transaction.p1 == personnes[int(id)] or transaction.p2 == personnes[int(id)]:
            out.append(transaction)
    return json.dumps(out, default=lambda o: o.__dict__, sort_keys=True, indent=4)

@app.route("/E4/<id>")
def afficherSoldePersonne(id):
    out = { "solde": personnes[int(id)].solde }
    return out

# @app.route("/E5")