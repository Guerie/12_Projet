import sys
from PySide2.QtWidgets import (QLabel, QApplication, QMainWindow,
    QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QSizePolicy, QTableWidgetItem, QDoubleSpinBox, QInputDialog)
from PySide2.QtGui import QPixmap
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from PySide2 import QtCore, QtUiTools
from projet_ui import Ui_MainWindow
import json

filename = "structureDonnees.json"
class Fenetre(QMainWindow):
    def __init__(self, parent=None):
        super(Fenetre, self).__init__(parent)
        self.dico = {}
        with open('structureDonnees.json', encoding='UTF-8') as json_data:
            self.dico = json.load(json_data)
            print(self.dico)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pbAjouterAcademie.clicked.connect(self.ajouterAcademie)
        self.ui.pbAjouterEtablissement.clicked.connect(self.ajouterEtablissement)
        # self.ui.pbAjouterClasse.clicked.connect(self.ajouterClasse)
        self.ui.pbAjouterNote.clicked.connect(self.ajouterNote)


        self.ui.cbAcademie.currentIndexChanged.connect(self.updateEtablissement)
        self.ui.cbEtablissement.currentIndexChanged.connect(self.updateClasse)
        self.ui.cbClasse.currentIndexChanged.connect(self.updateMatiere)
        self.ui.cbMatiere.currentIndexChanged.connect(self.updateSaisieEleves)
        self.updateAcademie()

        global dicoClass
        global nomE
        global spinB

    def ajouterAcademie(self):
        print("Ajout Académie")

        retour = QInputDialog().getText(self, "Ajout Académie", "Nom")
        if retour[0] == "":
            return
        fiche = {}
        fiche["nom"] = retour[0]
        fiche["etablissements"] = ""
        self.dico["academies"].append(fiche)
        print(fiche)

        self.ui.cbAcademie.addItem(fiche["nom"])
        self.sauveJSON()

    def ajouterEtablissement(self):
        print("Ajout Etablissement")
        retour = QInputDialog().getText(self, "Ajout Etablissement", "Nom")
        if retour[0] == "":
            return
        fiche = {}
        fiche["nom"] = retour[0]
        fiche["adresse"] = ""
        self.dico["academies"][self.ui.cbAcademie.currentIndex()]["etablissements"].append(fiche)
        print(fiche)

        self.ui.cbEtablissement.addItem(fiche["nom"])
        self.sauveJSON()

    def updateAcademie(self):
         self.ui.cbAcademie.clear()
         for a in self.dico["academies"]:
             self.ui.cbAcademie.addItem(a["nom"])

    def updateEtablissement(self):
        self.ui.cbEtablissement.clear()
        for e in self.dico["academies"][self.ui.cbAcademie.currentIndex()]["etablissements"]:
            self.ui.cbEtablissement.addItem(e["nom"])

    def updateClasse(self):
        self.ui.cbClasse.clear()
        for c in self.dico["academies"][self.ui.cbAcademie.currentIndex()]["etablissements"][self.ui.cbEtablissement.currentIndex()]["classes"]:
            self.ui.cbClasse.addItem(c["nom"])

    def updateMatiere(self):
        self.ui.cbMatiere.clear()
        listMat = []
        for el in self.dico["academies"][self.ui.cbAcademie.currentIndex()]["etablissements"][self.ui.cbEtablissement.currentIndex()]["classes"][self.ui.cbClasse.currentIndex()]["eleves"]:
            for matiere in el["matieres"]:
                listMat.append(matiere["nom"])
        self.ui.cbMatiere.addItems(np.unique(listMat))

    def updateSaisieEleves(self):
        cpt = 0
        self.ui.twTableau.clear()
        dicoClass = self.dico["academies"][self.ui.cbAcademie.currentIndex()]["etablissements"][self.ui.cbEtablissement.currentIndex()]["classes"][self.ui.cbClasse.currentIndex()]
        for eleve in dicoClass ["eleves"]:
            for matiere in eleve["matieres"]:
                mat = self.ui.cbMatiere.currentText()
                if matiere["nom"] == mat:
                    nomE = eleve["nom"]
                    self.ui.twTableau.setRowCount(cpt+1)
                    itemE = QTableWidgetItem(nomE)
                    self.ui.twTableau.setItem(cpt, 0, itemE)
                    spinB = QDoubleSpinBox()
                    spinB.setMaximum(20.0)
                    spinB.setSingleStep(0.25)
                    spinB.setProperty("nom", nomE)
                    self.ui.twTableau.setCellWidget(cpt, 1, spinB)
                    cpt += 1
        self.ui.twTableau.setHorizontalHeaderLabels(['Nom d\'eleve', 'Note'])

    def ajouterNote(self):
        cpt = 0
        spinB = QDoubleSpinBox()
        self.ui.twTableau.setCellWidget(cpt, 1, spinB)
        dicoNote = {}
        dicoNote["nom"] = self.ui.twTableau.item(i,0).text
        dicoNote["coef"] = self.ui.dsbCoef.value()
        dicoNote["valeur"] = self.ui.twTableau.cellWidget(cpt, spinB.value())


        # for eleve in self.ui.twTableau.cellWidget(cpt, "nom"): #trouver l'eleve
        #     if nomE == QTableWidgetItem(nomE):
        #         for matiere in eleve["matiere"]: #trouver la matiere pour chaque eleve
        #             note = dicoClass["eleve"]["nom"]["matiere"][self.ui.cbMatiere.currentText()]["note"][spinB.value]
        #             listeNote = [note]
        #             note.append(dicoNote)
        #             cpt += 1
        # self.sauveJSON()






    #calculer les mmoyennes

        #     self.dico["matiere"].append(note)
    #     self.updateListw()  # on appelle la fonction updateListw comme si on l'a copié
    #     self.sauveJSON()
    #
    # def updateListw(self):
    #     for fiche in self.monDico["note"]:  # [] j ai la liste note
    #         self.ui.twTableau.addItem(fiche["note"])

    def sauveJSON(self):
        jsonClasse = json.dumps(self.dico, sort_keys=True, indent=4) #dumps = transforme le dictionnaire en chaine de texte
        # #self.dico objet dictionnaire
        f = open(filename, 'w')
        f.write(jsonClasse)
        f.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fen = Fenetre()
    fen.show()
    sys.exit(app.exec_())