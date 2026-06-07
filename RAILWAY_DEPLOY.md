# Deploying to Railway

Steps to deploy this Dockerized Django app to Railway:

1. Push your changes to GitHub (this repository).
2. In Railway, create a new Project → Deploy From GitHub → select this repo.
3. Choose **Docker** for the service type (Railway will build using the `Dockerfile`).
4. Set Environment Variables (Project → Settings → Variables):
   - `SECRET_KEY` — generate locally:
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - `DATABASE_URL` — PostgreSQL connection string (Railway DB or external)
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — your domain or `*` (temporary)
   - Optional: `GUNICORN_WORKERS` — number of gunicorn workers (default 3)

5. Set the Start Command to:
   ```bash
   ./entrypoint.sh
   ```

6. Deploy and monitor logs. If migrations or static collection fail, verify environment variables and DB/storage connectivity.

Notes:
- Do not commit `.env` or any secret to the repo.
- For media file persistence, use external object storage (S3 or compatible) and configure `DEFAULT_FILE_STORAGE` accordingly — Railway filesystem is ephemeral.
