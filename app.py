#!/usr/bin/env python3
"""
AnimeInWeb API — Flask wrapper + terminal-style docs page.
Converted from Animeinweb.js. Deployable to Vercel (@vercel/python).

Local run:
    pip install flask requests --break-system-packages
    python3 app.py
    -> open http://127.0.0.1:5001/
"""

import requests
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

BASE_URL = "https://animeinweb.com/api/proxy/"
SECRET_HEADER = "animein-secure-proxy-key-123"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "x-proxy-secret": SECRET_HEADER,
    "Accept": "application/json, text/plain, */*",
}

REQUEST_TIMEOUT = 15

DAY_MAP = {
    "MONDAY": "SENIN",
    "TUESDAY": "SELASA",
    "WEDNESDAY": "RABU",
    "THURSDAY": "KAMIS",
    "FRIDAY": "JUMAT",
    "SATURDAY": "SABTU",
    "SUNDAY": "MINGGU",
}


def api_get(endpoint, params=None, timeout=None):
    url = f"{BASE_URL}{endpoint}"
    resp = requests.get(url, headers=HEADERS, params=params or {}, timeout=timeout or REQUEST_TIMEOUT)
    resp.raise_for_status()
    payload = resp.json()
    if payload and payload.get("status") == 200 and not payload.get("error"):
        return payload.get("data", {})
    raise ValueError(payload.get("message", f"API error with status {resp.status_code}"))


# ---------------------------------------------------------------------------
# Docs page (served at "/")
# ---------------------------------------------------------------------------

DOCS_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>animeinweb-api // docs</title>
<style>
  :root {
    --bg: #0a0e0a;
    --fg: #39ff88;
    --fg-dim: #1e8a4d;
    --amber: #ffb454;
    --red: #ff5f56;
    --panel: #0f1510;
    --border: #1e3324;
  }
  * { box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--fg);
    font-family: "SF Mono", "Fira Code", "Consolas", monospace;
    margin: 0;
    padding: 24px 16px 80px;
    line-height: 1.5;
  }
  .wrap { max-width: 860px; margin: 0 auto; }
  .banner {
    color: var(--fg);
    font-size: 11px;
    white-space: pre;
    overflow-x: auto;
    margin-bottom: 4px;
  }
  .subtitle { color: var(--fg-dim); margin-bottom: 28px; font-size: 13px; }
  .subtitle .ok { color: var(--fg); }
  h2 {
    color: var(--amber);
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin-top: 40px;
  }
  .endpoint {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 14px 16px;
    margin-bottom: 14px;
  }
  .method {
    display: inline-block;
    background: #10331f;
    color: var(--fg);
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 3px;
    margin-right: 8px;
    font-weight: bold;
  }
  .path { color: #d7ffe6; font-size: 13.5px; }
  .desc { color: var(--fg-dim); font-size: 12.5px; margin-top: 6px; }
  .params { color: var(--fg-dim); font-size: 12px; margin-top: 8px; }
  .params code { color: var(--amber); }
  .try-row { margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap; }
  .try-row input {
    background: #06090a;
    border: 1px solid var(--border);
    color: var(--fg);
    font-family: inherit;
    font-size: 12.5px;
    padding: 6px 8px;
    border-radius: 3px;
    flex: 1;
    min-width: 90px;
  }
  .try-row button {
    background: var(--fg-dim);
    color: #06090a;
    border: none;
    font-family: inherit;
    font-weight: bold;
    font-size: 12px;
    padding: 6px 14px;
    border-radius: 3px;
    cursor: pointer;
  }
  .try-row button:hover { background: var(--fg); }
  pre.result {
    background: #05080a;
    border: 1px solid var(--border);
    color: #b6ffcf;
    font-size: 11.5px;
    padding: 10px;
    margin-top: 10px;
    border-radius: 3px;
    max-height: 320px;
    overflow: auto;
    display: none;
    white-space: pre-wrap;
    word-break: break-all;
  }
  footer {
    margin-top: 60px;
    color: var(--fg-dim);
    font-size: 11.5px;
    border-top: 1px solid var(--border);
    padding-top: 16px;
  }
  a { color: var(--amber); }
</style>
</head>
<body>
<div class="wrap">
<div class="banner">
 _____       .__                .__            __
/  _  \\   ____ |__| _____   ____ |__| ____   __  _  __ ____   ____
/  /_\\  \\ /    \\|  |/     \\_/ __ \\|  |/    \\  \\ \\/ \\/ // __ \\_/ __ \\
/    |    \\   |  \\  |  Y Y  \\  ___/|  |   |  \\  \\     /\\  ___/\\  ___/
\\____|__  /___|  /__|__|_|  /\\___  >__|___|  /   \\/\\_/  \\___  >\\___  >
        \\/     \\/         \\/     \\/        \\/               \\/     \\/
</div>
<div class="subtitle"><span class="ok">status: online</span> &nbsp;|&nbsp; unofficial wrapper around animeinweb.com's internal proxy API &nbsp;|&nbsp; base: <span class="ok">/api</span></div>

<h2>&gt; homepage</h2>
<div class="endpoint">
  <span class="method">GET</span><span class="path">/api/homepage</span>
  <div class="desc">Hot / new / today / popular / trailer / random / waiting / slider anime sections.</div>
  <div class="try-row">
    <button onclick="tryIt('/api/homepage', this)">run</button>
  </div>
  <pre class="result"></pre>
</div>

<h2>&gt; search</h2>
<div class="endpoint">
  <span class="method">GET</span><span class="path">/api/search</span>
  <div class="params">params: <code>q</code> (keyword) &middot; <code>page</code> (default 0) &middot; <code>sort</code> (views|latest|favorites) &middot; <code>genre_in</code> (comma ids) &middot; <code>status</code> (ONGOING|FINISHED|WAITING, filtered locally) &middot; <code>type</code> (SERIES|MOVIE|ONA, filtered locally)</div>
  <div class="try-row">
    <input type="text" placeholder="q (e.g. one piece)" id="search-q" value="">
    <input type="text" placeholder="status (e.g. ONGOING)" id="search-status" value="">
    <input type="text" placeholder="type (e.g. MOVIE)" id="search-type" value="">
    <button onclick="tryIt('/api/search?q=' + encodeURIComponent(document.getElementById('search-q').value) + '&status=' + encodeURIComponent(document.getElementById('search-status').value) + '&type=' + encodeURIComponent(document.getElementById('search-type').value), this)">run</button>
  </div>
  <pre class="result"></pre>
</div>

<h2>&gt; anime details</h2>
<div class="endpoint">
  <span class="method">GET</span><span class="path">/api/anime/&lt;anime_id&gt;</span>
  <div class="desc">Full details for a single anime.</div>
  <div class="try-row">
    <input type="text" placeholder="anime_id (e.g. 426)" id="anime-id" value="426">
    <button onclick="tryIt('/api/anime/' + document.getElementById('anime-id').value, this)">run</button>
  </div>
  <pre class="result"></pre>
</div>

<h2>&gt; episode list</h2>
<div class="endpoint">
  <span class="method">GET</span><span class="path">/api/anime/&lt;anime_id&gt;/episodes</span>
  <div class="desc">List of episodes for an anime.</div>
  <div class="try-row">
    <input type="text" placeholder="anime_id (e.g. 426)" id="ep-anime-id" value="426">
    <button onclick="tryIt('/api/anime/' + document.getElementById('ep-anime-id').value + '/episodes', this)">run</button>
  </div>
  <pre class="result"></pre>
</div>

<h2>&gt; episode stream</h2>
<div class="endpoint">
  <span class="method">GET</span><span class="path">/api/episode/&lt;episode_id&gt;/stream</span>
  <div class="desc">Direct video sources (mp4, multi-quality) for one episode.</div>
  <div class="try-row">
    <input type="text" placeholder="episode_id (e.g. 317534)" id="stream-ep-id" value="317534">
    <button onclick="tryIt('/api/episode/' + document.getElementById('stream-ep-id').value + '/stream', this)">run</button>
  </div>
  <pre class="result"></pre>
</div>

<h2>&gt; schedule</h2>
<div class="endpoint">
  <span class="method">GET</span><span class="path">/api/schedule</span>
  <div class="params">params: <code>day</code> (MONDAY..SUNDAY or SENIN..MINGGU, default MINGGU)</div>
  <div class="try-row">
    <input type="text" placeholder="day (e.g. MONDAY)" id="sched-day" value="MONDAY">
    <button onclick="tryIt('/api/schedule?day=' + document.getElementById('sched-day').value, this)">run</button>
  </div>
  <pre class="result"></pre>
</div>

<h2>&gt; genres</h2>
<div class="endpoint">
  <span class="method">GET</span><span class="path">/api/genres</span>
  <div class="desc">List of all available genres.</div>
  <div class="try-row">
    <button onclick="tryIt('/api/genres', this)">run</button>
  </div>
  <pre class="result"></pre>
</div>

<footer>
  built by Dayynime &middot; unofficial &middot; no auth required &middot; not affiliated with animeinweb.com
</footer>
</div>

<script>
async function tryIt(path, btn) {
  const box = btn.parentElement.nextElementSibling;
  box.style.display = 'block';
  box.textContent = 'loading...';
  try {
    const res = await fetch(path);
    const data = await res.json();
    box.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    box.textContent = 'error: ' + e.message;
  }
}
</script>
</body>
</html>
"""


@app.route("/")
def docs():
    return Response(DOCS_HTML, mimetype="text/html")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "animeinweb-flask-wrapper"})


@app.route("/api/homepage")
def homepage():
    try:
        # Upstream default cuma ngasih 3 item per section kalau gak dikasih limit.
        # Kita naikin ke 10 biar preview di Home lebih keisi (ketemu empiris, bukan
        # didokumentasiin resmi — kalau upstream berubah perilaku, ini yang dicek duluan).
        limit = request.args.get("limit", "10")
        data = api_get("3/2/home/data", params={"limit": limit})
        return jsonify({
            "hot": data.get("hot", []),
            "new": data.get("new", []),
            "today": data.get("today", []),
            "popular": data.get("popular", []),
            "trailer": data.get("trailer", []),
            "random": data.get("random", []),
            "waiting": data.get("waiting", []),
            "slider": data.get("slider", []),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/search")
def search():
    query = request.args.get("q", "")
    page = request.args.get("page", "0")
    sort = request.args.get("sort", "views")
    genre_in = request.args.get("genre_in", "")
    # animeinweb's upstream proxy ignores status/type query params entirely
    # (confirmed empirically) — so we filter locally on the returned results
    # instead. Valid status values seen in the data: ONGOING, FINISHED, WAITING
    # (there's no "COMPLETED" — FINISHED is the equivalent).
    status = request.args.get("status", "").upper()
    anime_type = request.args.get("type", "").upper()

    try:
        if status or anime_type:
            # Sebagian besar halaman upstream cuma dikit yang match status/type
            # tertentu (misal MOVIE bisa 0 di halaman pertama padahal total ada
            # ratusan). Jadi kalau ada filter ini, kita nyisir beberapa halaman
            # upstream SEKALIGUS di server (dibatasin biar gak kena timeout
            # function), baru dibalikin satu batch hasil yang udah lumayan padat.
            MAX_PAGES_PER_REQUEST = 4  # diturunin dari 8 — riwayat gagal-muat dicurigai
            # gara-gara ini nyeret function ngelewatin timeout Vercel
            TARGET_RESULTS = 20
            LOOP_TIMEOUT = 3.5  # worst-case 4 x 3.5s = 14s kalau semua lambat — masih
            # bisa kena limit 10s default Vercel Hobby, tapi kemungkinan lebih kecil
            start_page = int(page)
            results = []
            seen_ids = set()
            scanned = 0
            next_page = None
            reached_end = False

            for i in range(MAX_PAGES_PER_REQUEST):
                cur_page = start_page + i
                params = {"keyword": query, "page": str(cur_page), "sort": sort}
                if genre_in:
                    params["genre_in"] = genre_in
                try:
                    data = api_get("3/2/explore/movie", params, timeout=LOOP_TIMEOUT)
                except Exception:
                    # 1 halaman gagal/lambat gak boleh nggagalin seluruh request —
                    # stop di sini, balikin apa yang udah kekumpul (kalau ada), dan
                    # biarin next_page = halaman ini biar dicoba ulang nanti.
                    next_page = cur_page
                    break
                raw = data.get("movie", [])
                scanned += 1

                if not raw:
                    reached_end = True
                    break

                for r in raw:
                    if status and r.get("status", "").upper() != status:
                        continue
                    if anime_type and r.get("type", "").upper() != anime_type:
                        continue
                    if r.get("id") not in seen_ids:
                        seen_ids.add(r.get("id"))
                        results.append(r)

                if len(results) >= TARGET_RESULTS:
                    next_page = cur_page + 1
                    break
            else:
                next_page = start_page + MAX_PAGES_PER_REQUEST

            if reached_end:
                next_page = None

            return jsonify({
                "query": query,
                "page": page,
                "sort": sort,
                "genreIds": genre_in.split(",") if genre_in else [],
                "status": status or None,
                "type": anime_type or None,
                "note": "status/type filtered locally across multiple upstream pages per request",
                "pages_scanned": scanned,
                "next_page": next_page,
                "results": results,
            })

        params = {"keyword": query, "page": page, "sort": sort}
        if genre_in:
            params["genre_in"] = genre_in

        data = api_get("3/2/explore/movie", params)
        results = data.get("movie", [])

        return jsonify({
            "query": query,
            "page": page,
            "sort": sort,
            "genreIds": genre_in.split(",") if genre_in else [],
            "status": None,
            "type": None,
            "note": None,
            "next_page": (int(page) + 1) if results else None,
            "results": results,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/anime/<anime_id>")
def anime_details(anime_id):
    try:
        data = api_get(f"3/2/movie/detail/{anime_id}")
        movie = data.get("movie")
        if movie is None:
            return jsonify({"error": "Anime not found"}), 404
        return jsonify(movie)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/anime/<anime_id>/episodes")
def episodes(anime_id):
    try:
        page = request.args.get("page")
        params = {"page": page} if page else None
        data = api_get(f"3/2/movie/episode/{anime_id}", params)
        return jsonify(data.get("episode", []))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/episode/<episode_id>/stream")
def episode_stream(episode_id):
    try:
        data = api_get(f"3/2/episode/streamnew/{episode_id}")
        return jsonify({
            "episode": data.get("episode"),
            "episodeNext": data.get("episode_next"),
            "servers": data.get("server", []),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/schedule")
def schedule():
    day = request.args.get("day", "MINGGU").upper()
    mapped_day = DAY_MAP.get(day, day)
    try:
        data = api_get("3/2/schedule/data", {"day": mapped_day})
        return jsonify(data.get("movie", []))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/genres")
def genres():
    try:
        data = api_get("3/2/explore/genre")
        return jsonify(data.get("genre", []))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
