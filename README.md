# communevent

**CS 3200 — Spring 2026 | Marky Mark and the Funky Bunch**

A local event discovery and management platform connecting attendees, event organizers, performers, and venue owners.

## Team Members

| Name | Email |
|------|-------|
| Matthew Garcia (Point Person) | garcia.matt@northeastern.edu |
| Janie Lu | lu.jan@northeastern.edu |
| Eoin Collette | collette.e@northeastern.edu |
| Jacob Yu | yu.jaco@northeastern.edu |
| Nevin Kannalath | kannalath.n@northeastern.edu |

## About

communevent is a data-driven event platform that lets:
- **Attendees** browse a personalized feed, RSVP, save favorites, and leave reviews
- **Event Organizers** post events, find performers, and request venue bookings
- **Performers** manage their profile, receive booking requests, and track gigs
- **Venue Owners** review booking requests, manage their calendar, and track revenue

## Demo Video

> [Link to demo video — add before submission]

## Setup & Running

### Prerequisites
- Docker Desktop installed and running

### Steps

1. **Clone the repo**
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```

2. **Create your `.env` file** (copy from the template and fill in credentials)
   ```bash
   cp api/.env.template api/.env
   ```
   Edit `api/.env`:
   ```
   DB_USER=root
   DB_PASSWORD=<your-password>
   DB_HOST=db
   DB_PORT=3306
   DB_NAME=CommunEvent
   SECRET_KEY=somesecret
   ```

3. **Start all services**
   ```bash
   docker compose up -d
   ```
   This starts three containers:
   - `db` — MySQL on port 3200
   - `web-api` — Flask REST API on port 4000
   - `app` — Streamlit UI on port 8501

4. **Open the app** at [http://localhost:8501](http://localhost:8501)

### Resetting the database

If you change SQL files in `database-files/`, delete and recreate the database container:
```bash
docker compose down
docker volume rm <project>_db_data
docker compose up -d
```

## Project Structure

```
├── app/            # Streamlit frontend
│   └── src/
│       ├── Home.py         # Login / role selector
│       ├── pages/          # Per-persona feature pages
│       └── modules/nav.py  # Sidebar navigation
├── api/            # Flask REST API
│   └── backend/
│       ├── attendee/
│       ├── event/
│       ├── organizer/
│       ├── owner/
│       ├── performer/
│       ├── venue/
│       └── review/
└── database-files/ # MySQL schema + seed data
```
