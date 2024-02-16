## Préréquis

- [Docker](https://www.docker.com/)

## Installation

1. Cloner le projet
2. Faire un `docker compose up --build -d` à la racine du projet
3. Aller dans le container `web` avec `docker exec -it <container_id> bash`
4. Faire un `cd app/src/hotel` pour se rendre dans le dossier de l'API
5. Faire un `flask db init`, `flask db migrate`, `flask db upgrade` pour créer les tables dans la base de données

## Utilisation

- L'API est accessible à l'adresse `http://localhost:5001`

### Routes

- `/api/chambres/disponibles` --> GET: Récupère toutes les chambres disponibles
- `/api/reservations` --> POST: Crée une réservation
- `/api/reservations/<int:id>` --> DELETE: Supprime une réservation
- `/api/chambres` --> POST: Crée une chambre
- `/api/chambres/<int:id>` --> DELETE/PUT: Supprime une chambre/Modifie une chambre
