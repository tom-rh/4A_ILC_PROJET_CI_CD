from flask import Flask

app = Flask(__name__)

class Personne:
    def __init__(self, id, nom, prenom, solde):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.solde = solde

    def toString(self):
        return self.nom + ' ' + self.prenom + ' ' + str(self.solde)

class Transation:
    def __init__(self, p1, p2, t, s):
        self.p1 = p1
        self.p2 = p2
        self.t = t
        self.s = s

        p1.solde -= s
        p2.solde += s

    def toString(self):
        return self.p1.nom + ' ' +  self.p2.nom + ' ' +  str(self.t) + ' ' + str(self.s)

personnes = [
    Personne(0, "Andres", "Baptiste", 1000000000), 
    Personne(1, "Roth", "Tom", 0),
    Personne(2, "Thomas", "Gauthier", -100)]

transations = []

@app.route("/")
def hello_world():
    return {}

@app.route("/E1/<p1>/<p2>/<t>/<s>")
def e1(p1, p2, t, s):
    transations.append(Transation(personnes[p1], personnes[p2], t, s))
    return [transations[-1], personnes[p1], personnes[p2]]
