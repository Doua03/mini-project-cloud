# Mini-Projet Cloud - TODO API

## Description
API de gestion de tâches (TODO) déployée avec Docker et Docker Compose.

## Technologies utilisées
- Docker / Docker Compose
- Flask (Python)
- PostgreSQL
- Redis
- Nginx
- Prometheus + Grafana
- GitHub Actions

## Services

| Service | Port | Rôle |
|---------|------|------|
| Nginx | 80, 443 | Reverse proxy + HTTPS |
| Flask | 5000 (interne) | API TODO |
| PostgreSQL | 5432 (interne) | Base de données |
| Redis | 6379 (interne) | Cache |
| Prometheus | 9090 | Monitoring |
| Grafana | 3000 | Visualisation |
| cAdvisor | 8080 | Métriques Docker |

## Installation

```bash

# Démarrer les services
docker-compose up -d
