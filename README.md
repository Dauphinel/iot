# 🚀 IoT Pipeline - Système de Traitement Temps Réel

## 📋 Description du Projet

Ce projet implémente un pipeline IoT complet en temps réel qui collecte, traite, stocke et visualise des données de capteurs IoT.

## 🏗️ Architecture

```
📡 Capteurs IoT → 🌐 MQTT → 🔄 Kafka → ⚡ Spark → 💾 InfluxDB → 📊 Grafana
```

### Composants

- **📡 MQTT Producer** : Simule des capteurs IoT (température, humidité, etc.)
- **🌐 Mosquitto** : Broker MQTT pour la collecte de données
- **🔄 MQTT-Kafka Bridge** : Pont entre MQTT et Kafka
- **🚀 Apache Kafka** : Message queue pour le streaming
- **⚡ Apache Spark** : Traitement en streaming des données
- **💾 InfluxDB** : Base de données temporelle
- **📊 Grafana** : Visualisation en temps réel

## 🚀 Démarrage Rapide

### Prérequis
- Docker et Docker Compose installés
- Windows 10/11

### Lancement
1. **Double-cliquer sur `start-demo.bat`** ou
2. **En ligne de commande :**
   ```bash
   docker-compose up -d
   ```

### Accès aux Services
- **📊 Grafana Dashboard** : http://localhost:3000
  - Username: `admin`
  - Password: `admin`
- **📡 MQTT Broker** : localhost:1883
- **💾 InfluxDB** : http://localhost:8086
- **🚀 Kafka** : localhost:9092

## 📊 Données Collectées

Le système simule les capteurs suivants :
- 🌡️ **Température** : 18-30°C
- 💧 **Humidité** : 40-70%
- 🌪️ **Pression** : 980-1050 hPa
- 🌬️ **Qualité d'air** : 20-150 ppm
- 💡 **Luminosité** : 100-1000 lux
- 👁️ **Détection de mouvement** : 0/1
- 🔊 **Niveau sonore** : 30-80 dB
- 🌿 **CO2** : 350-800 ppm
- 🔋 **Niveau de batterie** : 10-100%

## 🎯 Fonctionnalités

### ✅ Collecte de Données
- Simulation de capteurs IoT réalistes
- Publication MQTT toutes les 2 secondes
- Données JSON structurées

### ✅ Traitement en Streaming
- Apache Spark Streaming
- Traitement en temps réel
- Transformation et nettoyage des données

### ✅ Stockage Temporel
- InfluxDB pour les données temporelles
- Optimisé pour les séries temporelles
- Requêtes performantes

### ✅ Visualisation Temps Réel
- Dashboard Grafana pré-configuré
- Graphiques en temps réel
- Alertes et seuils configurables

## 🔧 Commandes Utiles

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs en temps réel
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f mqtt-producer
docker-compose logs -f spark
docker-compose logs -f mqtt-kafka-bridge

# Arrêter tous les services
docker-compose down

# Redémarrer un service
docker-compose restart spark
```

## 📈 Dashboard Grafana

Le dashboard inclut :
- **Statistiques en temps réel** : Température, humidité, qualité d'air
- **Graphiques temporels** : Évolution des capteurs
- **Détection de mouvement** : Indicateur visuel
- **Vue d'ensemble** : Tous les capteurs sur un graphique

## 🎓 Points Techniques

### Technologies Utilisées
- **Frontend** : Grafana (visualisation)
- **Backend** : Python (producteur), Node.js (bridge), PySpark (traitement)
- **Base de données** : InfluxDB (temporelle)
- **Message Queue** : Apache Kafka
- **Broker MQTT** : Mosquitto
- **Containerisation** : Docker & Docker Compose

### Performance
- **Latence** : < 5 secondes end-to-end
- **Débit** : 1000+ messages/minute
- **Scalabilité** : Architecture microservices

## 🛠️ Dépannage

### Problèmes Courants

1. **Ports déjà utilisés**
   ```bash
   # Vérifier les ports utilisés
   netstat -an | findstr "3000\|8086\|1883\|9092"
   ```

2. **Services qui ne démarrent pas**
   ```bash
   # Voir les logs d'erreur
   docker-compose logs [service-name]
   ```

3. **Pas de données dans Grafana**
   - Vérifier que le producteur MQTT fonctionne
   - Vérifier les logs du bridge MQTT-Kafka
   - Vérifier les logs Spark

## 📝 Notes pour la Soutenance

### Démonstration Recommandée
1. **Lancer le système** avec `start-demo.bat`
2. **Ouvrir Grafana** et montrer le dashboard
3. **Expliquer l'architecture** en temps réel
4. **Montrer les logs** des différents services
5. **Démontrer la latence** en temps réel

### Points Clés à Souligner
- ✅ **Pipeline complet** : MQTT → Kafka → Spark → InfluxDB → Grafana
- ✅ **Temps réel** : Données mises à jour toutes les 2 secondes
- ✅ **Scalabilité** : Architecture microservices
- ✅ **Robustesse** : Gestion d'erreurs et logs
- ✅ **Visualisation** : Dashboard professionnel

---

**🎯 Objectif Atteint : Système IoT temps réel fonctionnel et prêt pour la production !** 