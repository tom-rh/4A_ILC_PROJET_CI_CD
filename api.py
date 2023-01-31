from flask import Flask

from operator import attrgetter

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

personnes = [
    Personne(0, "Andres", "Baptiste", 1000000000), 
    Personne(1, "Roth", "Tom", 0),
    Personne(2, "Thomas", "Gauthier", -100)]

transactions = []

# Requete

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
def afficherTransactions():
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

# @app.route("/E5")