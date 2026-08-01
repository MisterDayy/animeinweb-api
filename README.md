# AnimeInWeb API (Flask wrapper)

Unofficial wrapper around animeinweb.com's internal proxy API, with a
terminal-style docs page at `/`.

## Run locally (Termux)

```bash
pip install flask requests --break-system-packages
python3 app.py
```

Open `http://127.0.0.1:5001/` for the docs page with live "run" buttons.

## Deploy to Vercel (from Termux)

```bash
npm install -g vercel
cd animeinweb-api
vercel login
vercel --prod
```

Follow the prompts (link/create project). Once deployed, Vercel gives you a
URL like `https://animeinweb-api.vercel.app/` — that's your public docs +
API base, safe to call from the Aniku Android app.

## Endpoints

| Method | Path                              | Description                          |
|--------|-----------------------------------|---------------------------------------|
| GET    | `/`                                | Docs page                             |
| GET    | `/api/health`                      | Health check                          |
| GET    | `/api/homepage`                    | Hot/new/today/popular/trailer/random  |
| GET    | `/api/search?q=&page=&sort=&genre_in=` | Search anime                      |
| GET    | `/api/anime/<anime_id>`            | Anime details                         |
| GET    | `/api/anime/<anime_id>/episodes`   | Episode list                          |
| GET    | `/api/episode/<episode_id>/stream` | Direct video sources (mp4)            |
| GET    | `/api/schedule?day=`               | Daily release schedule                |
| GET    | `/api/genres`                      | List of genres                        |

## Notes

- No auth needed — animeinweb.com's proxy endpoint just requires the
  `x-proxy-secret` header, already hardcoded in `app.py`.
- `episode/<id>/stream` returns `type: "direct"` mp4 links hosted on
  `storages.animein.net` — safe to pass straight into ExoPlayer
  (`MediaItem.fromUri(link)`), no extraction step needed.
- Consider caching `/api/homepage` and `/api/anime/*` responses in Supabase
  to reduce load on animeinweb.com and avoid rate limiting.
