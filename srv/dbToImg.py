import mariadb
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from datetime import timedelta, datetime
import matplotlib.dates as mdates

conn = mariadb.connect(user="SAE", password="DBPassword", host="127.0.0.1", port=3306, database="SAE") #connection à la base de données
cur = conn.cursor()

delta=6 #le nombre d'heures sur lesquelles récupérer les données

#data = tableau de 2,3,4 string avec les noms des valeurs
#table = dans quelle table chercher
#name = nom du fichier de sortie en .png
#Crée un graph en image

def graphMake2(data, table, name):
    date=datetime.now()-timedelta(hours=delta) #obtenir la date et l'heure il y a six heures

    cur.execute("SELECT "+data[0]+","+data[-1]+" FROM "+table+" WHERE NOT timestamp<'"+str(date)+"'") #Obtenir les données de la base de données

    idx = pd.date_range(date, datetime.now(), freq = 'min') #crée un tableau de dates avec une date et heure par minute

    #manipulations pour rendre les données utiliseables par matplotlib
    y=data[0]

    tabx=[]
    taby=[]

    for (y, x) in cur:
        taby.append(y)
        tabx.append(x)

    plt.figure(figsize=(9.00, 7.00), dpi=100) #Taille de l'image
    
    fig, ax = plt.subplots() #initialiser la figure
    hours = mdates.HourLocator(interval = 1) #Créer une liste de dates et heures par heure
    h_fmt = mdates.DateFormatter('%H:%M') #formatter cette liste pour obtenir uniquement les minutes et heures
    ax.plot(tabx, taby, label=data[0]) #Dessiner le graph
    ax.xaxis.set_major_locator(hours) #faire en sorte que l'axe des ordonnées contienne des graduations toutes les heures
    ax.xaxis.set_major_formatter(h_fmt) #Formatter les valeurs de ces graduations en utiliseant uniquement les minutes et heures
    fig.autofmt_xdate() #Auto formatter la figure

    plt.legend() #Ajouter une légende pour les courbes
    plt.xlabel("Temps") #Ajouter une légende sur l'axe des ordonnées
    plt.ylabel(name) #Ajouter une légende sur l'axe des abcisses
    plt.savefig('/var/www/html/graph/'+name+'.png', dpi=100) #sauvegarder la figure

def graphMake3(data, table, name):
    date=datetime.now()-timedelta(hours=delta)

    cur.execute("SELECT "+data[0]+","+data[1]+","+data[-1]+" FROM "+table+" WHERE NOT timestamp<'"+str(date)+"'")

    idx = pd.date_range(date, datetime.now(), freq = 'min')


    y1=data[0]
    y2=data[1]
    x=data[-1]

    tabx=[]
    taby1=[]
    taby2=[]

    for (y1, y2, x) in cur:
        taby1.append(y1)
        taby2.append(y2)
        tabx.append(x)

    plt.figure(figsize=(9.00, 7.00), dpi=100)

    fig, ax = plt.subplots()
    hours = mdates.HourLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%H:%M')
    ax.plot(tabx, taby1, label=data[0])
    ax.plot(tabx, taby2, label=data[1])
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt)
    fig.autofmt_xdate()

    plt.legend()
    plt.xlabel("Temps")
    plt.ylabel(name)
    plt.savefig('/var/www/html/graph/'+name+'.png', dpi=100)

def graphMake4(data, table, name):
    date=datetime.now()-timedelta(hours=delta)

    cur.execute("SELECT "+data[0]+","+data[1]+","+data[2]+","+data[-1]+" FROM "+table+" WHERE NOT timestamp<'"+str(date)+"'")

    idx = pd.date_range(date, datetime.now(), freq = 'min')

    y1=data[0]
    y2=data[1]
    y3=data[2]
    x=data[-1]

    tabx=[]
    taby1=[]
    taby2=[]
    taby3=[]

    for (y1, y2, y3, x) in cur:
        taby1.append(y1)
        taby2.append(y2)
        taby3.append(y3)
        tabx.append(x)

    plt.figure(figsize=(9.00, 7.00), dpi=100)

    fig, ax = plt.subplots()
    hours = mdates.HourLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%H:%M')

    ax.plot(tabx, taby1, label=data[0])
    ax.plot(tabx, taby2, label=data[1])
    ax.plot(tabx, taby3, label=data[2])

    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt)
    fig.autofmt_xdate()

    plt.legend()
    plt.xlabel("Temps")
    plt.ylabel(name)
    plt.savefig('/var/www/html/graph/'+name+'.png', dpi=100)

#noms des valeurs dans les tables
humid = ['louishum', 'pawelhum', 'owmhum', 'timestamp']
temp = ['louistemp', 'paweltemp', 'owmtemp', 'timestamp']
servLouis = ['louisCPU', 'louisRAM', 'timestamp']
servPawel = ['pawelCPU', 'pawelRAM', 'timestamp']
powerLouis = ['louisPAPP', 'timestamp']
powerPawel = ['PawelPAPP', 'timestamp']

#arranger les tables pour être facilement implémentés dans une boucle
tables = [humid, temp, servLouis, servPawel, powerLouis, powerPawel]

#noms des tables SQL
tabname = ['environment', 'environment', 'system_usage', 'system_usage', 'power_data', 'power_data']

#noms des fichiers en sortie
filename = ['Humidité', 'Température', 'ServeurLouis', 'ServeurPawel', 'ConsoServeurLouis', 'LinkyPawel']

#Boucle de création des graphes
x=0
for tab in tables:
    if len(tab)==2:
        #print(tab)
        graphMake2(tab, tabname[x], filename[x])
    if len(tab)==3:
        #print(tab)
        graphMake3(tab, tabname[x], filename[x])
    if len(tab)==4:
        #print(tab)
        graphMake4(tab, tabname[x], filename[x])
    x+=1

#Fermeture de la connexion
conn.close()
