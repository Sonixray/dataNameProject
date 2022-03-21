import sqlite3
import matplotlib.pyplot as plt
bdd=sqlite3.connect('bdd_prenoms.db')
curseur = bdd.cursor()

"""Requête SQL et cas spéciaux (notamment si aucune naissance n'est enregistrée)"""
resultat=[]
while resultat==[]: #On demande un prénom jusqu'à ce qu'un graphique apparaisse (oui oui on ne lachera rien !)
    prenom=input("Prénom ?").upper()
    curseur.execute("SELECT sum(nombre), annee FROM donnees where prenom=? AND annee<>'XXXX' group by annee",[prenom])
    resultat=curseur.fetchall()
    if resultat==[]:
      print("Oups, il semblerait qu'aucune naissance de '",prenom,"' ne soit enregistrée entre 1900 et 2020 :/")
    else:
        """Initialisation des variables utiles à la construction du tableau"""
        max=0
        min=3000
        naissancemax=0
        x=[]
        y=[]
        if resultat!=[]:
            for i in range(len(resultat)):
                if max<resultat[i][1]:
                    max=resultat[i][1]
                if min>resultat[i][1]:
                    min=resultat[i][1]

        """Construction de la table X (dans ce cas les années en abscisses)"""
        for i in range(min,max+1):
            x.append(i)

        """Construction de la table Y (nombres de naissances)"""
        curseurx=0           # On créé des curseurs pour éviter le problème des années où 0 naissances sont enregistrés, ce
        curseur2x=0          # qui peut poser problème dans certains cas car Mathplotlib exige deux tableaux X et Y de même longueur !

        for i in range(max+1-min):
            if x[curseurx]==resultat[curseur2x][1]:
                y.append(resultat[curseur2x][0])
                if naissancemax<resultat[curseur2x][0]:
                    naissancemax=resultat[curseur2x][0]
                curseurx+=1
                curseur2x+=1
            else:
                curseurx+=1
                y.append(0)

        """Ajout des barres sur le graphique avec des couleurs différentes en fonction du nombre de naissance"""
        for i in range(len(x)):
            color=(y[i]/naissancemax-1)*(-1)
            plt.bar(x[i],y[i],color=(1,color,color))

        """Partie graphique chiante et inutile"""
        plt.title("Evolution du prénom "+prenom)
        plt.ylabel('Naissances')
        plt.xlabel("Années")
        plt.grid(b=True, which='major', color='#999999', linestyle='-', alpha=0.3)
        ax = plt.gca()
        ax.set_facecolor('#62FCF0')
        plt.show()

"""Requête SQL et boucle infinie tant que tant que l'année n'est pas comprise entre 1900 et 2019 inclus"""
annee=0
while annee>2019 or annee<1900:
    annee=int(input("Année ?"))
curseur.execute("SELECT prenom,sum(nombre) FROM donnees where annee=? and prenom<>'_PRENOMS_RARES' group by prenom order by sum(nombre) desc",[annee])
resultat=curseur.fetchall()

"""Affichage des prénoms sur les barres"""
y=8.85
for i in range(10):
    plt.text(200,y,resultat[i][0])
    y-=1

"""Initialisation de la table X"""
Naissances=[]
for i in range(10):
    Naissances.append(resultat[9-i][1])

"""Initialisation de la table Y"""
Classement = ["10","9","8","7","6","5","4","3","2","1"]

"""Construction du graphique avec variation de couleur"""
for i in range(10):
    plt.barh(Classement[i], Naissances[i],color=(0,Naissances[0]/Naissances[i],Naissances[0]/Naissances[i]))

"""Partie graphique"""
plt.title("Prénoms les plus populaires en l'an "+str(annee))
plt.ylabel('Classement')
plt.xlabel("Naissances")
plt.show()