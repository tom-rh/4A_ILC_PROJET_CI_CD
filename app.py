from flask import Flask

from operator import attrgetter

app = Flask(__name__)

class Personne:
    def __init__(self, id, nom, prenom, solde):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.solde = solde

    def toString(self):
        return str(self.id) + ' : ' + self.nom + ' ' + self.prenom + ' ' + str(self.solde)

class Transaction:
    def __init__(self, p1, p2, date, somme):
        self.p1 = p1
        self.p2 = p2
        self.date = date
        self.somme = somme

        p1.solde -= somme
        p2.solde += somme

    def toString(self):
        return self.p1.nom + ' ' +  self.p2.nom + ' ' +  self.date + ' ' + str(self.somme)

personnes = [
    Personne(0, "Andres", "Baptiste", 1000000000), 
    Personne(1, "Roth", "Tom", 0),
    Personne(2, "Thomas", "Gauthier", -100)]

transactions = []

@app.route("/")
def afficherPersonnes():
    out = "<h3>Liste de Personne :</h3>\n"
    for personne in personnes:
        out += "<p>" + personne.toString() + "</p>\n"
    return out

@app.route("/E1/<id1>/<id2>/<date>/<somme>")
@app.route("/ajouterTransaction/<id1>/<id2>/<date>/<somme>")
def transaction(id1, id2, date, somme):
    transactions.append(Transaction(personnes[int(id1)], personnes[int(id2)], date, int(somme)))
    sorted(transactions, key=attrgetter('date'))
    return "<h3>Transaction :   " + transactions[-1].toString() + "</h3>\n" + afficherPersonnes()

@app.route("/E2")
@app.route("/transactions")
def afficherTransactions():
    out = "<h3>Liste de Transaction :</h3>\n"
    for transaction in transactions:
        out += "<p>" + transaction.toString() + "</p>\n"
    return out

@app.route("/E3/<id>")
@app.route("/E4/<id>")
@app.route("/profil/<id>")
def afficherProfil(id):
    out = "<h3>" + personnes[int(id)].toString() + "</h3>\n"
    for transaction in transactions:
        if transaction.p1 == personnes[int(id)] or transaction.p2 == personnes[int(id)]:
            out += "<p>" + transaction.toString() + "</p>\n"
    return out
