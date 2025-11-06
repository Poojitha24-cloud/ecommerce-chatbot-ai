# Ecommerce Chatbot AI - Ready to Deploy
**Interactive E‑Commerce Chatbot** (Frontend + Flask AI + PHP auth + MySQL schema)

## Overview
- Frontend: `frontend/` (static HTML/CSS/JS) — host on GitHub Pages
- AI Service: `backend/python/` (Flask) — host on Render at https://e-commerce-chatbot.onrender.com
- PHP API: `backend/php/` — host on your domain https://myshopbot.in
- Database: `database/schema.sql` — MySQL (PlanetScale / cPanel)

The Flask AI integrates with **OpenAI GPT** if `OPENAI_API_KEY` is set; otherwise it falls back to a lightweight TF-IDF search for product recommendations.

## Quick start (local)
1. Create MySQL DB and run `database/schema.sql`.

2. PHP: configure `backend/php/config.php` with DB credentials and upload to your PHP host.

3. Python: create virtualenv, install `backend/python/requirements.txt` and run `python backend/python/ai_service.py`.

4. Frontend: open `frontend/index.html` or host on GitHub Pages. Edit `frontend/app.js` to point to your deployed endpoints.

