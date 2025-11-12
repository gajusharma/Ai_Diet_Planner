# Smart AI Diet Planner – Deployment Guide

This guide covers deploying the project using **Render** for the FastAPI backend, **MongoDB Atlas** for the database, and **Vercel** for the Vite/React frontend.

## 1. Prerequisites

- GitHub repository containing this project
- Python 3.11+ locally (optional, for testing)
- Node.js 18+ locally (optional, for testing)
- Accounts on:
  - [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
  - [Render](https://render.com)
  - [Vercel](https://vercel.com)
- Gemini API key (from Google AI Studio)

## 2. Environment Variables

### Backend (`render` web service)
Set the following env vars in Render → *Environment*:

| Key | Description |
| --- | --- |
| `MONGO_URI` | MongoDB Atlas connection string |
| `MONGO_DB_NAME` | Database name (default `aiplanner`) |
| `FOOD_COLLECTION_NAME` | Collection name (default `foods`) |
| `JWT_SECRET` | Auth secret (generate a strong random value) |
| `GEMINI_API_KEY` | Gemini API key |
| `GEMINI_MODEL` | Example: `models/gemini-1.5-pro-latest` |
| `FORCE_REFRESH_FOODS` | Set to `true` for first deployment to seed data |

### Frontend (Vercel)

| Key | Description |
| --- | --- |
| `VITE_API_BASE_URL` | URL of deployed backend (e.g., `https://smart-ai-diet-backend.onrender.com`) |

## 3. MongoDB Atlas Setup

1. Create a free cluster.
2. Create a database user with password.
3. Whitelist IPs: add `0.0.0.0/0` or specific addresses.
4. Get connection string, e.g. `mongodb+srv://USER:PASS@cluster0.mongodb.net/aiplanner?retryWrites=true&w=majority`.

## 4. Backend Deployment (Render)

1. Push project to GitHub.
2. In Render → **New + → Web Service**.
3. Connect GitHub repo.
4. Root directory: `backend`.
5. Build Command:
   ```bash
   pip install -r requirements.txt
   ```
6. Start Command:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
7. Set environment variables (see table above).
8. Deploy. Check logs.
9. Run data seeding once:
   - Set `FORCE_REFRESH_FOODS=true` in env vars and redeploy, or
   - Use Render shell: `python utils/seed_data.py`.

   ## 5. Backend Deployment (Railway)

   1. Install the [Railway CLI](https://docs.railway.app/develop/cli) and log in, or use the dashboard.
   2. Connect the GitHub repository and create a new service.
   3. Railway reads `railway.toml`, which pins the service root to `backend`, installs `requirements.txt`, sets `PYTHON_VERSION=3.11`, and starts `uvicorn` with `main:app`.
   4. In Railway → *Variables*, add the same environment variables listed for Render. Set `FORCE_REFRESH_FOODS=true` for the first deploy to seed data; remove or set to `false` afterward and redeploy.
   5. Trigger a deploy. The logs should show `uvicorn` binding to the provided `$PORT` once dependencies finish installing.
   6. Copy the public domain from the Railway service details and use it as the API base for the frontend (`https://<service>.up.railway.app`).

   If you prefer to configure manually instead of relying on `railway.toml`, make sure the service directory is `backend`, build command `pip install -r requirements.txt`, and start command `uvicorn main:app --host 0.0.0.0 --port $PORT`.

   ## 6. Backend Deployment (Replit)

   Use this path if you prefer to host the FastAPI backend on Replit instead of Render.

   1. Create a new Repl and import the GitHub repository (`gajusharma/Ai_Diet_Planner`).
   2. Replit reads the `.replit` and `replit.nix` files to prepare a Python 3.11 environment and automatically installs the backend dependencies.
   3. Once the install step finishes, the server starts with:
      ```bash
      cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
      ```
   4. In **Secrets** (lock icon), add the backend environment variables listed earlier (`MONGO_URI`, `MONGO_DB_NAME`, `FOOD_COLLECTION_NAME`, `JWT_SECRET`, `GEMINI_API_KEY`, `GEMINI_MODEL`, `FORCE_REFRESH_FOODS`).
   5. For the initial deployment, set `FORCE_REFRESH_FOODS=true` so the seed script runs on startup. After the data is seeded, remove or set it to `false` and click **Run** again.
   6. Replit exposes a public HTTPS URL (shown in the webview). Use this URL as the API base for the frontend.
   7. If you need to rerun the install step manually, open the Shell tab and run:
      ```bash
      pip install -r backend/requirements.txt
      ```

   > **Note:** Keep the Repl running or enable the Always On upgrade so the API stays reachable.

   ## 7. Frontend Deployment (Vercel)

1. In Vercel → **Add New Project**.
2. Select GitHub repo, choose root `frontend`.
3. Framework: Vite (auto-detected).
4. Build & Output settings:
   - Install Command: `npm install`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Add environment variable `VITE_API_BASE_URL` with backend URL.
6. Deploy. Launch the provided domain.

## 8. Testing Locally

Backend:
```powershell
cd backend
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
$env:MONGO_URI="mongodb://localhost:27017" # adjust
uvicorn main:app --reload
```

Frontend:
```powershell
cd frontend
npm install
npm run dev
```

## 9. Optional: GitHub Workflows

- Add CI to lint/test backend.
- Add Vercel/Render deploy hooks for automatic deployments.

## 10. Maintenance

- Monitor Render logs and Atlas metrics.
- Rotate secrets periodically.
- Update dependencies regularly (`pip`, `npm`).

Happy deploying! 🚀
