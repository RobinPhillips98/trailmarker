# Trailmarker

A **Pathfinder 2e combat encounter simulator** that lets you build a party of characters, select enemies, and run repeated automated simulations to evaluate how your party may fare in combat — using the **Beginner Box** ruleset.

## ✨ Features

- 🧙 **Party Management** — Create and manage player characters with stats from their character sheets (attacks, spells, skills, and more)
- 👹 **Enemy Roster** — Browse enemies from the Beginner Box
- ⚔️ **Combat Simulation** — Run 100 automated combat encounters between your party and a chosen set of enemies
- 📊 **Simulation Results** — View win rate, average rounds, average deaths, and a full round-by-round combat log for each simulated encounter
- 🔐 **User Accounts** — Register and log in to save your party and access simulation features

## 🎓 Academic Project

Trailmarker is my Capstone Project for the Computer Science program at the **University of North Carolina Asheville**

- **Course Instructor:** Dr. Kenneth Bogert
- **Mentor:** Professor Michael Sarris

## 🛠️ Tech Stack

### Backend
- **Python** with [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
- **PostgreSQL** database
- **SQLAlchemy** ORM
- **Poetry** for dependency management
- **JWT authentication** via `python-jose` and `passlib`

### Frontend
- **React** with [Vite](https://vitejs.dev/)
- **Ant Design** component library
- **React Router** for client-side routing
- **Axios** for API communication

### Infrastructure
- **Docker Compose** for local development

## 📁 Project Structure

```
trailmarker/
├── backend/
│   ├── api/
│   │   └── routes/          # FastAPI route handlers (auth, characters, enemies, encounters, simulation, user)
│   ├── simulation/
│   │   ├── core/            # Simulation driver
│   │   ├── creatures/       # Player and enemy combat logic
│   │   └── encounters/      # Encounter turn-order and round management
│   ├── schemas/             # Pydantic models
│   ├── models.py            # SQLAlchemy ORM models
│   ├── server.py            # FastAPI app entrypoint
│   └── populate.py          # Seeds the database with enemy data from GitHub
├── frontend/
│   └── src/
│       └── js/
│           └── components/  # React components (simulation, characters, enemies, etc.)
└── compose.yaml             # Docker Compose configuration
```

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone the repository

```bash
git clone https://github.com/RobinPhillips98/trailmarker.git
cd trailmarker
```

### 2. Configure the environment

Create a `.env` file in the `backend/` directory. The following variables are required:

```env
DB_USERNAME=postgres
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
DB_NAME=trailmarker
SECRET_KEY=your_secret_key
```

> **Note:** `POSTGRES_PASSWORD` is hardcoded in `DockerfileDatabase` for initial database setup. Update this for any non-local environment.

### 3. Run with Docker Compose

```bash
docker compose up
```

This will:
1. Start a **PostgreSQL** database container
2. Run the **db_setup** service to create the database (if it doesn't exist)
3. Start the **backend** server (installs dependencies, seeds enemy data, starts Uvicorn at port `8000`)
4. Start the **frontend** UI (installs dependencies, starts Vite dev server at port `5173`)

### 4. Open the app

| Service  | URL                    |
|----------|------------------------|
| Frontend | http://localhost:5173  |
| Backend  | http://localhost:8000  |
| API Docs | http://localhost:8000/docs |

## 🎲 How It Works

1. **Register / Log in** to create your account.
2. **Add characters** to your party with their combat stats (HP, AC, attacks, saves, etc.).
3. On the **homepage**, select enemies from the bestiary and specify how many of each.
4. Click **Run Simulation** — the backend runs 100 combat encounters and returns the results.
5. View your **win rate**, average rounds, average deaths, and read further into the **combat log** of any individual simulation.

## 📄 License

This project is for personal/educational use. Pathfinder 2e content sourced from the [Foundry VTT pf2e system](https://github.com/foundryvtt/pf2e) is subject to the Paizo Community Use Policy.
