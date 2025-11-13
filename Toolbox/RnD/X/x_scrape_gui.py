# x_scrape_gui.py
# X (Twitter) scraper GUI with List URL support.
# Paste a List URL (e.g., https://x.com/i/lists/143036...) and scrape either:
#  - Members (handles + profile meta)
#  - Timeline (recent tweets shown in that List)
#
# Uses twikit for authenticated requests via cookies.json.
# Defensive about twikit versions: tries multiple method names and logs if missing.

import csv
import json
import os
import re
import threading
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

import logging
from logging.handlers import RotatingFileHandler

try:
    from twikit import Client, TooManyRequests
except Exception as e:
    raise SystemExit("Failed to import twikit. Create the conda env and ensure twikit is installed.") from e

APP_DIR = Path(__file__).resolve().parent
COOKIE_FILE = APP_DIR / "cookies.json"
OUTPUT_DIR = APP_DIR / "output"
LOG_DIR = APP_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

LIST_URL_RE = re.compile(r"(?:https?://)?(?:www\.)?(?:x|twitter)\.com/i/lists/(\d+)")

# -------------------- Logging --------------------
class TextHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.widget.configure(state="disabled")

    def emit(self, record):
        msg = self.format(record) + "\n"
        def append():
            self.widget.configure(state="normal")
            self.widget.insert(tk.END, msg)
            self.widget.see(tk.END)
            self.widget.configure(state="disabled")
        try:
            self.widget.after(0, append)
        except tk.TclError:
            pass

def make_logger(text_widget=None) -> logging.Logger:
    logger = logging.getLogger("x_list_gui")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        fh = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
        fh.setFormatter(fmt); fh.setLevel(logging.DEBUG); logger.addHandler(fh)
        ch = logging.StreamHandler()
        ch.setFormatter(fmt); ch.setLevel(logging.INFO); logger.addHandler(ch)
        if text_widget is not None:
            th = TextHandler(text_widget)
            th.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
            th.setLevel(logging.INFO); logger.addHandler(th)
    return logger

# -------------------- twikit helpers --------------------
def init_client(lang: str = "en-US") -> Client:
    return Client(lang)

def ensure_login(client: Client, force_relogin: bool = False, logger: logging.Logger = None) -> None:
    cookies_loaded = False
    if not force_relogin and COOKIE_FILE.exists():
        try:
            client.load_cookies(path=str(COOKIE_FILE))
            cookies_loaded = True
            if logger: logger.info("Loaded cookies from %s", COOKIE_FILE)
        except Exception as e:
            if logger: logger.warning("Failed to load cookies: %s", e)
            cookies_loaded = False
    if cookies_loaded and getattr(client, "logged_in", False):
        return
    user = simpledialog.askstring("Login", "X username / email / phone:")
    if not user:
        raise RuntimeError("Login cancelled")
    pwd = simpledialog.askstring("Login", "X password:", show="*")
    if not pwd:
        raise RuntimeError("Login cancelled")
    def _challenge_handler():
        return simpledialog.askstring("2FA / Verification", "Enter code (SMS / app / email):") or ""
    client.login(auth_info_1=user, password=pwd, two_factor_callback=_challenge_handler)
    client.save_cookies(str(COOKIE_FILE))
    if logger: logger.info("Login successful. Saved cookies to %s", COOKIE_FILE)

# -------------------- List scraping core --------------------
def parse_list_id(url: str) -> str:
    m = LIST_URL_RE.search(url.strip())
    if not m:
        raise ValueError("Not a valid X List URL")
    return m.group(1)

def _safe_get(obj: Any, name: str, default=None):
    try:
        return getattr(obj, name)
    except Exception:
        return default

def _utc_iso(dt) -> str:
    try:
        if hasattr(dt, "astimezone"):
            return dt.astimezone(timezone.utc).isoformat()
        return str(dt)
    except Exception:
        return str(dt)

# Try multiple twikit variants to get list members
def get_list_members(client: Client, list_id: str, limit: int, sleep_s: float, logger: logging.Logger) -> List[Dict]:
    members: List[Dict] = []
    cursor = None
    fetched = 0

    def fetch_page(cur):
        # A) client.get_list_members(list_id, count=..., cursor=...)
        if hasattr(client, "get_list_members"):
            return client.get_list_members(list_id=list_id, count=100, cursor=cur)
        # B) client.get_list(...).get_members(...)
        if hasattr(client, "get_list"):
            lst = client.get_list(list_id)
            if hasattr(lst, "get_members"):
                return lst.get_members(count=100, cursor=cur)
        raise AttributeError("No list-members method available in this twikit version.")

    while fetched < limit:
        page = fetch_page(cursor)
        # Expected shapes vary: (users, next_cursor) or dict-like or list
        users = None; next_cursor = None
        if isinstance(page, tuple) and len(page) == 2:
            users, next_cursor = page
        elif isinstance(page, dict):
            users = page.get("users") or page.get("items") or []
            next_cursor = page.get("next_cursor") or page.get("cursor") or None
        else:
            users = page
            next_cursor = None

        if not users:
            break

        for u in users:
            rec = {
                "screen_name": _safe_get(u, "screen_name"),
                "user_id": _safe_get(u, "id") or _safe_get(u, "rest_id"),
                "name": _safe_get(u, "name"),
                "description": _safe_get(u, "description"),
                "followers_count": _safe_get(u, "followers_count"),
                "following_count": _safe_get(u, "friends_count"),
                "listed_count": _safe_get(u, "listed_count"),
                "verified": bool(_safe_get(u, "verified") or _safe_get(u, "is_verified")),
                "created_at": _utc_iso(_safe_get(u, "created_at")),
                "location": _safe_get(u, "location"),
                "url": f"https://x.com/{_safe_get(u, 'screen_name')}" if _safe_get(u, "screen_name") else None,
                "profile_image_url": _safe_get(u, "profile_image_url_https") or _safe_get(u, "profile_image_url"),
            }
            members.append(rec)
            fetched += 1
            if fetched >= limit:
                break
        if not next_cursor:
            break
        cursor = next_cursor
        time.sleep(sleep_s)
    logger.info("Collected %d member(s).", len(members))
    return members[:limit]

# Try multiple twikit variants to get list timeline
def get_list_timeline(client: Client, list_id: str, limit: int, sleep_s: float, logger: logging.Logger) -> List[Dict]:
    tweets: List[Dict] = []
    cursor = None
    fetched = 0

    def fetch_page(cur):
        # A) client.get_list_tweets(list_id, count=..., cursor=...)
        if hasattr(client, "get_list_tweets"):
            return client.get_list_tweets(list_id=list_id, count=50, cursor=cur)
        # B) client.get_list(...).get_tweets(...)
        if hasattr(client, "get_list"):
            lst = client.get_list(list_id)
            if hasattr(lst, "get_tweets"):
                return lst.get_tweets(count=50, cursor=cur)
        raise AttributeError("No list-timeline method available in this twikit version.")

    while fetched < limit:
        page = fetch_page(cursor)
        # Expected shapes: (tweets, next_cursor) or dict-like or list
        items = None; next_cursor = None
        if isinstance(page, tuple) and len(page) == 2:
            items, next_cursor = page
        elif isinstance(page, dict):
            items = page.get("tweets") or page.get("items") or []
            next_cursor = page.get("next_cursor") or page.get("cursor") or None
        else:
            items = page
            next_cursor = None

        if not items:
            break

        for t in items:
            author_sn = _safe_get(t, "user", None)
            if author_sn and hasattr(author_sn, "screen_name"):
                author_sn = author_sn.screen_name
            rec = {
                "tweet_id": _safe_get(t, "id") or _safe_get(t, "rest_id"),
                "author_screen_name": author_sn or _safe_get(t, "screen_name"),
                "created_at": _utc_iso(_safe_get(t, "created_at")),
                "full_text": _safe_get(t, "full_text") or _safe_get(t, "text"),
                "in_reply_to": _safe_get(t, "in_reply_to_status_id") or _safe_get(t, "in_reply_to_tweet_id"),
                "retweet_of": _safe_get(t, "retweeted_status_id"),
                "quote_of": _safe_get(t, "quoted_status_id"),
                "favorite_count": _safe_get(t, "favorite_count"),
                "reply_count": _safe_get(t, "reply_count"),
                "retweet_count": _safe_get(t, "retweet_count"),
                "bookmark_count": _safe_get(t, "bookmark_count"),
                "view_count": _safe_get(t, "view_count"),
            }
            if rec["tweet_id"] and rec["author_screen_name"]:
                rec["permalink"] = f"https://x.com/{rec['author_screen_name']}/status/{rec['tweet_id']}"
            tweets.append(rec)
            fetched += 1
            if fetched >= limit:
                break
        if not next_cursor:
            break
        cursor = next_cursor
        time.sleep(sleep_s)
    logger.info("Collected %d tweet(s) from list timeline.", len(tweets))
    return tweets[:limit]

# -------------------- Writers --------------------
def _timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")

def write_txt(rows: List[Dict], out_path: Path, kind: str) -> None:
    lines = []
    if kind == "members":
        for r in rows:
            lines += [
                f"@{r.get('screen_name')}  ({r.get('name')})",
                f"followers={r.get('followers_count')} following={r.get('following_count')} verified={r.get('verified')}",
                f"url={r.get('url')}",
                (r.get('description') or '').strip(),
                "-"*80
            ]
    else:
        for r in rows:
            lines += [
                f"{r.get('created_at')}  @{r.get('author_screen_name')}",
                f"{r.get('permalink')}",
                f"♥ {r.get('favorite_count')}  🔁 {r.get('retweet_count')}  💬 {r.get('reply_count')}  🔖 {r.get('bookmark_count')}  👁 {r.get('view_count')}",
                (r.get('full_text') or '').strip(),
                "-"*80
            ]
    out_path.write_text("\n".join(lines), encoding="utf-8")

def write_csv(rows: List[Dict], out_path: Path) -> None:
    if not rows:
        out_path.write_text("", encoding="utf-8"); return
    keys = sorted({k for r in rows for k in r.keys()})
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def write_json(rows: List[Dict], out_path: Path) -> None:
    out_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

# -------------------- GUI --------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("X List Scraper — Paste URL, Click, Save")
        self.geometry("980x600")

        # Top controls (List URL + options)
        top = ttk.Frame(self, padding=10)
        top.pack(fill=tk.X)

        ttk.Label(top, text="List URL:").pack(side=tk.LEFT)
        self.url_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.url_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

        self.limit_members = tk.IntVar(value=500)
        self.limit_tweets = tk.IntVar(value=200)
        self.sleep_s = tk.DoubleVar(value=0.5)
        self.as_json = tk.BooleanVar(value=False)

        opts = ttk.Frame(top)
        opts.pack(side=tk.LEFT, padx=(8,0))
        ttk.Label(opts, text="Members:").grid(row=0, column=0, sticky="w")
        ttk.Entry(opts, width=6, textvariable=self.limit_members).grid(row=0, column=1, padx=(4,10))
        ttk.Label(opts, text="Tweets:").grid(row=0, column=2, sticky="w")
        ttk.Entry(opts, width=6, textvariable=self.limit_tweets).grid(row=0, column=3, padx=(4,10))
        ttk.Label(opts, text="Sleep(s):").grid(row=0, column=4, sticky="w")
        ttk.Entry(opts, width=6, textvariable=self.sleep_s).grid(row=0, column=5, padx=(4,10))
        ttk.Checkbutton(opts, text="Also JSON", variable=self.as_json).grid(row=0, column=6, sticky="w")

        btns = ttk.Frame(self, padding=10)
        btns.pack(fill=tk.X)
        ttk.Button(btns, text="Login / Relogin", command=self.relogin).pack(side=tk.LEFT, padx=(0,6))
        ttk.Button(btns, text="Scrape List → Members", command=self.scrape_members).pack(side=tk.LEFT, padx=(0,6))
        ttk.Button(btns, text="Scrape List → Timeline", command=self.scrape_timeline).pack(side=tk.LEFT)

        out_row = ttk.Frame(self, padding=(10,0,10,10))
        out_row.pack(fill=tk.X)
        ttk.Label(out_row, text="Output Folder:").pack(side=tk.LEFT)
        self.out_dir_var = tk.StringVar(value=str(OUTPUT_DIR))
        ttk.Entry(out_row, textvariable=self.out_dir_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        ttk.Button(out_row, text="Browse…", command=self.pick_output_dir).pack(side=tk.LEFT)

        ttk.Label(self, text="Log").pack(anchor="w", padx=10)
        self.log = tk.Text(self, height=22, wrap="word")
        self.log.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        self.log.configure(state="disabled")

        self.status_var = tk.StringVar(value="Ready.")
        status = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w", padding=4)
        status.pack(side=tk.BOTTOM, fill=tk.X)

        self.logger = make_logger(self.log)
        self.client = init_client("en-US")

    # ---- Utilities ----
    def set_status(self, s: str):
        self.status_var.set(s)

    def pick_output_dir(self):
        path = filedialog.askdirectory(initialdir=self.out_dir_var.get() or str(OUTPUT_DIR))
        if path:
            self.out_dir_var.set(path)

    def relogin(self):
        def task():
            try:
                ensure_login(self.client, force_relogin=True, logger=self.logger)
                messagebox.showinfo("Login", "Login successful. Cookies saved.")
            except Exception:
                self.logger.error("Login failed: %s", traceback.format_exc())
                messagebox.showerror("Error", "Login failed. See logs/app.log.")
        threading.Thread(target=task, daemon=True).start()

    def _parse_list_id_ui(self) -> str:
        url = (self.url_var.get() or "").strip()
        if not url:
            raise ValueError("Paste a List URL first.")
        list_id = parse_list_id(url)
        self.logger.info("Parsed List ID: %s", list_id)
        return list_id

    def _ensure_login_ui(self):
        try:
            ensure_login(self.client, force_relogin=False, logger=self.logger)
        except Exception:
            self.logger.error("Not logged in: %s", traceback.format_exc())
            messagebox.showerror("Error", "Not logged in. Use Login/Relogin first.")
            raise

    # ---- Handlers ----
    def scrape_members(self):
        def task():
            try:
                list_id = self._parse_list_id_ui()
                self._ensure_login_ui()
                self.set_status("Scraping members…")
                rows = get_list_members(self.client, list_id, self.limit_members.get(), self.sleep_s.get(), self.logger)
                ts = _timestamp()
                out_base = Path(self.out_dir_var.get() or OUTPUT_DIR)
                txtp = out_base / f"list_{list_id}_members_{ts}.txt"
                csvp = out_base / f"list_{list_id}_members_{ts}.csv"
                write_txt(rows, txtp, "members")
                write_csv(rows, csvp)
                if self.as_json.get():
                    jsonp = out_base / f"list_{list_id}_members_{ts}.json"
                    write_json(rows, jsonp)
                self.logger.info("Members saved: %s ; %s", txtp, csvp)
                self.set_status("Done.")
                messagebox.showinfo("Done", f"Saved members to:\n{txtp}\n{csvp}")
            except AttributeError as e:
                self.logger.error("Twikit list-members not available: %s", e)
                messagebox.showerror("Unsupported", "Your twikit version doesn't expose list member APIs.\nUpdate twikit or use user-based scraping.")
            except Exception:
                self.logger.error("Scrape members failed: %s", traceback.format_exc())
                messagebox.showerror("Error", "Failed. See logs/app.log.")
            finally:
                self.set_status("Ready.")
        threading.Thread(target=task, daemon=True).start()

    def scrape_timeline(self):
        def task():
            try:
                list_id = self._parse_list_id_ui()
                self._ensure_login_ui()
                self.set_status("Scraping list timeline…")
                rows = get_list_timeline(self.client, list_id, self.limit_tweets.get(), self.sleep_s.get(), self.logger)
                ts = _timestamp()
                out_base = Path(self.out_dir_var.get() or OUTPUT_DIR)
                txtp = out_base / f"list_{list_id}_timeline_{ts}.txt"
                csvp = out_base / f"list_{list_id}_timeline_{ts}.csv"
                write_txt(rows, txtp, "timeline")
                write_csv(rows, csvp)
                if self.as_json.get():
                    jsonp = out_base / f"list_{list_id}_timeline_{ts}.json"
                    write_json(rows, jsonp)
                self.logger.info("Timeline saved: %s ; %s", txtp, csvp)
                self.set_status("Done.")
                messagebox.showinfo("Done", f"Saved timeline to:\n{txtp}\n{csvp}")
            except AttributeError as e:
                self.logger.error("Twikit list-timeline not available: %s", e)
                messagebox.showerror("Unsupported", "Your twikit version doesn't expose list timeline APIs.\nUpdate twikit or use user-based scraping.")
            except Exception:
                self.logger.error("Scrape timeline failed: %s", traceback.format_exc())
                messagebox.showerror("Error", "Failed. See logs/app.log.")
            finally:
                self.set_status("Ready.")
        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
