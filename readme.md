# 📡 SAE 203 - Mettre en place une solution informatique pour l’entreprise  

> _SAE 203 — BUT Réseaux & Télécommunications_  
> **BUT RT - Semestre 2** | IUT Université de pau et des pays de l'adour (UPPA)
---

## 🎯 Objectif du projet

Ce projet vise à concevoir une **plateforme de gestion d’informations IoT**, capable de :  
- Collecter des données à partir de capteurs (réels ou simulés)  
- Échanger les données via le protocole **MQTT**  
- Stocker et afficher les données via un **site web dynamique**  
- Étudier les vulnérabilités de la solution et proposer des mesures de **cybersécurité**  

La plateforme suit le modèle suivant :  
- 🔁 Données transmises via MQTT (publish/subscribe)  
- 🗃️ Stockage en base de données  
- 🌐 Visualisation via un site  
- 🧠 Traitement, et sécurisation des données  
---

## 📜 Sujet
[Le sujet est consultable ICI](https://munier.perso.univ-pau.fr/teaching/butrt-sae203/)
---

## 🛠️ Technologies utilisées

| Outil / Langage       | Utilisation principale                        |
|-----------------------|-----------------------------------------------|
| `ESP32 / Arduino IDE` | Capteurs, collecte de données (DHT11/DHT22)   |
| `openweathermap`      | Capteurs, collecte de données depuis internet |
| `Python`              | Scripts d’émission / réception MQTT           |
| `MQTT (Mosquitto)`    | Communication entre objets et serveurs        |
| `MariaDB`             | Stockage des mesures collectées               |
| `PHP / HTML`          | Interface web dynamique                       |
| `Wireshark`           | Analyse réseau, détection de vulnérabilités   |
---

## 📂 Arborescence du projet

```bash
SAE203/
├── capteur/           # Scripts Python et Arduino pour l'envoi sur le broker MQTT.  
├── srv/               # Script Python pour la récupération des flux MQTT, le traitement dans la DB, et la génération des graphiques.  
├── www/               # Scripts PHP et fichiers HTML du serveur web.  
├── diagrame.pdf       # Diagramme de l'infrastructure mis en place.  
├── initDB.sql         # Fichier SQL pour la génération de la BD.  
└── RapportCyber.pdf   # Rapport sur les aspects cybersécurité.  
```
---

## 🧑‍💻 Auteur
- 👤 **Louis Deschamps**  
  📧 [contact@louino.fr](mailto:contact@louino.fr)  
  🎓 Étudiant en BUT Réseaux & Télécoms, IUT Université de pau et des pays de l'adour (UPPA)  
- 👤 **Pawel Zajac**  
  📧 [justendie@endtech.fr](mailto:justendie@endtech.fr)  
  🎓 Étudiant en BUT Réseaux & Télécoms, IUT Université de pau et des pays de l'adour (UPPA)  

---

## 🔒 Licence  
> [!WARNING]  
> **Plagiat interdit**  
> Ce projet est distribué sous la licence **MIT**. Vous êtes **autorisé à réutiliser, modifier, distribuer ou intégrer ce code**, y compris à des fins commerciales, à **condition d'en citer l'auteur original et de conserver cette licence** dans toute copie ou version modifiée.  
> Le plagiat, défini comme la reproduction ou paraphrase non créditée d’un contenu, constitue une infraction aux **règles universitaires** et au droit d’auteur. **(Vous pouvez consulter, vous inspirer, mais pas copier.)**  
> Toute utilisation sans attribution peut entraîner des sanctions académiques et juridiques.   
> **MIT License – Libre usage, mais attribution obligatoire.**   
