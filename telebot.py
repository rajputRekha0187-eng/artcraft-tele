import os, io, json, time, random, subprocess, requests, threading
from datetime import datetime, timedelta
from dateutil import tz
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials as UserCreds

# =========================================================
# LOAD ENV
# =========================================================
load_dotenv()

# =========================================================
# CONFIG
# =========================================================

VIDEO_FOLDER_ID = os.environ["VIDEO_FOLDER_ID"]
AUDIO_FOLDER_ID = os.environ["AUDIO_FOLDER_ID"]
STATE_FILE_ID   = os.environ["STATE_FOLDER_ID"]

TELEGRAM_TOKEN  = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT   = os.environ["TELEGRAM_CHAT_ID"]

TOTAL_VIDEOS    = int(os.environ.get("TOTAL_VIDEOS", "0"))

TZ = tz.gettz(os.environ["CHANNEL_TIMEZONE"])

# We set a default start date to "Tomorrow at 8:00 AM" if no state is found
DEFAULT_START_DATE = datetime.now(TZ) + timedelta(days=1)
DEFAULT_START_DATE = DEFAULT_START_DATE.replace(hour=8, minute=0, second=0, microsecond=0)

TIME_SLOTS = [8, 12, 16]
MAX_PER_DAY = 3

WATERMARK = "@ArtWeaver"
# This path is standard for the 'fonts-dejavu' package in Debian/Ubuntu
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BASE_DESCRIPTION = """Disclaimer: - Copyright Disclaimer under section 107 of the Copyright Act 1976. allowance is made for "fair use" for purposes such as criticism. Comment. News. reporting. Teaching. Scholarship . and research. Fair use is a use permitted by copy status that might otherwise be infringing Non-profit. Educational or per Sonal use tips the balance in favor

ArtCraft.
#bayshotyt #freefire #foryou #freefireconta #spas12 #aimbotfreefire #hackfreefire #sho
They think I'm an Emulatortgunhandcam
#shotgun #x1freefire #freefirebrasil #freefireclipes #melhoresmomentos #handcam #loud
a01,a11,a10,a20,a30,50,a70,a80, iphone,
#freefire #freefirehighlights #equipou #habash #bestplayer #m1014 #spas12 #dpifreefire #contarara #bestmoments #Iphonefreefire #androidfreefire #equipou ,
blackn444, bak, loud, ph, movimentação, como subir capa, como colocar gel rápido, free fire pro,pro player, ff, higlight, piuzinho, el gato, sansung a10, jogando no a10, jogador mestre, mobile nivel emulador, level up, nobru, como subir capa, mobile, kauan vm, kauan free fire, menino capudo, revelacao mobile, free fire argentina, free fire Tailândia, free fire, heróico, mastro, mestre, x1 dos youtubers free fire
оттяжка настройки на телефон для оттяжки в фри фаер настройки для телефона фри фаер настройки оттяжки thedonato
como levantar la mira en free fire test freefire galaxy a10 a30 free fire samsung a10 a20
настройки для фри фаер для оттяжки
#хардскилл #скепта #а10 #баги #скилл #чювствительность для фрифаер #смешные моменты
sick saint azoz yt darking b2kill akiles a3sag mrstiven tc luay
#the best player. #фрифаер
sensitivitas auto headshot hp samsung wawanmks frontalgaming sensitivitas hp samsung ff sensitivitas samsung ff sensitivitas mp40 sensitivitas shotgun sensitivitas m1014 let's hyper rendyrangers freefire antrax
#лучшая чювствительность #топ мира #азамм #смайл
настройки оттяжки на samsung #игры #топ игрок в фриаер #самсунг а10
boomsniper
configuracion de heroico free fire gran mestre configuracion de top global free fire configuracion para samsung free fire configuraciónes de free fire configuración para samsung a20 configuración para samsung a30 configuración para celulares samsung configuracion para samsung a20 configuracion para samsung a10 free fire headshots full tendencias
#gt #pvs gaming #rungaming
configuracion para samsung a70 free fire configuracion para samsung a60 free fire configuracion para samsung a30 free fire configuracion para samsung a40 equipou free fire configuracion para samsung a50 free fire configuración para samsung a10
#чувствительность #free fire #лучшаячувствительность
vivo y91 free fire golemcito antronixx highlights samsung a 10 samsung a10 configuracion blazze configuracion samsung a10 la mejor configuracion free fire josir yt instagram raiser asi juega un niño de 13 años solucion a bug 360 equipou free fire configuracion samsung a10 free fire free fire samsung a10 elma free fire latam Samsung a01
#kiraop kira op, white ff, enzin ff Light ff, Bryan Gabriel one shotgun free fire, satisfactory ruok, #broken, #shorts, enzin ff, martinsffx
#iphone just perfect #travando #iosfreefire #equipou #j5prime #j2prime #mestre #clipes
loud snow ff, drau ff, mini white, free fire 245
#pabluoff indonesia, los grandes, loud #highlights ruok free fire #jogos #white444 #ruanff #iphone8plus
fazinzz, uzzumak ff, hypudinhos, mark ff, jotah ff, produting, #bar1tb #textura #texturafreefire #clownffx
clownffx, xprod ff,d7 ff,junin 10, Bryan, brabox ff custom regedit como dar capa melhor hud #Freefreemax
movimentação free fire highlights Indonésia, loudgg melhor jogador de free fire, white ff, wize ff, #playhard
pedrinwq, mini since sensi do White ff, Just Perfect config best, samsung a01 free fire Enzinffx, enzinffx, martinsffx, nightfx, kira op, #freefireminiwhite, proplayer, melhor hud, emulador, eles me confudem com emulador, mobile, J2 prime, j1 mini, mini hinata, mini pivete ff, pivete ff, adr, instaplayer, xiaomi, highlights em campeonato, ruan ff, stivanelli, vega ff, ruok ff, Samsung a01 highlights, free fire, fazin ff, hud do fazin, hud 3 dedos fazin, como botar hud do fazin, como fazer gelo do fazin, fazin, raelznx highlights, como fazer thumb, textura ff, pack de textura, sensibilidade,
ArtCraft,
como fazer, hud 3 dedos,hud 4 dedos, hud 5 dedos, hud 1 dedo, #hudidea 6 dedos, bad ff, ruok, Dini ff, pack de textura, textura, fzn fps, melhor sensibilidade, sundex ff, redmi note 8, xiaomi, rog phone, Charlesz, 100tiro, Gabriel clips, x1 do buxexa, free fire highlights, white ff, pewdepie, Noel ff, vídeos do fazin, como fazer gel 1p #ideasearth
como fazer gelo 1p, gelo de um péo
#mrindianhackers #lyunaff #bkffofficial1 #equipou #manifestedit #khatushyambhajan #bullymaguire"""

TAG_POOL = [
    "ArtCraft", "Art", "Craft", "DIY", "Drawing", "Painting", "Sketching",
    "Satisfying art", "ASMR art", "Viral art", "Trending art", "Creative",
    "Handmade", "Artist", "Shorts", "How to draw", "Tutorial", "Paper craft",
    "Origami", "Acrylic painting", "Watercolor", "Digital art", "Speedpaint",
    "Art hacks", "DIY hacks", "5 minute crafts", "School hacks", "Easy drawing",
    "Anime drawing", "Realistic drawing", "3D art", "Optical illusion",
    "Calligraphy", "Lettering", "Bullet journal", "Art challenge", "Art supplies",
    "Sketchbook", "Oil pastel", "Color theory", "Shading", "Blending",
    "Character design", "Illustration", "Painting tutorial", "Craft ideas",
    "Home decor DIY", "Clay art", "Resin art", "Canvas painting", "Pencil sketch",
    "Markers", "Procreate", "Ibis Paint X", "Art vlog", "Tiktok art",
    "Masterpiece", "Abstract art", "Modern art", "Fine art", "Sculpture",
    "Pottery", "Ceramics", "Embroidery", "Knitting", "Crochet", "Jewelry making",
    "Mixed media", "Collage", "Doodle", "Zentangle", "Mandala", "Graffiti",
    "Street art", "Mural", "Spray paint", "Fashion design", "Miniature",
    "Diorama", "Pixel art", "Satisfying video", "Stationery", "Aesthetic",
    "Cute art", "Kawaii", "Manga art", "Fluid art", "Palette knife", "Easel",
    "Art supplies haul", "Copic markers", "Posca pens", "Gouache", "Charcoal",
    "Graphite", "Colored pencils", "Prismacolor", "Faber castell", "Arteza",
    "Winsor and newton", "Polymer clay", "Air dry clay", "Sculpting",
    "Custom doll", "Cosplay props", "Costume design", "Macrame", "Woodworking",
    "Pyrogrpahy", "Leather working", "Stained glass", "Candle making",
    "Soap making", "Slime making", "Fidget toys", "Pop it", "Art therapy",
    "Mental health", "Inspiration", "Motivation", "Transformation", "Glow up",
    "Restoration", "Studio tour", "Desk setup", "Artist life"
]

# Global flag to check if scheduler is running
SCHEDULER_RUNNING = False

# =========================================================
# TELEGRAM HELPERS
# =========================================================

def tg(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT,
                "text": msg,
                "parse_mode": "HTML"
            },
            timeout=10
        )
    except Exception as e:
        print(f"Telegram Error: {e}")

def progress_bar(done, total, size=20):
    if total <= 0:
        return "?"
    filled = int(size * done / total)
    return "█" * filled + "░" * (size - filled)

# =========================================================
# AUTH
# =========================================================

drive = build(
    "drive", "v3",
    credentials=Credentials.from_service_account_info(
        json.loads(os.environ["DRIVE_SERVICE_ACCOUNT_JSON"]),
        scopes=["https://www.googleapis.com/auth/drive"]
    )
)

youtube = build(
    "youtube", "v3",
    credentials=UserCreds.from_authorized_user_info(
        json.loads(os.environ["YOUTUBE_TOKEN_JSON"]),
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
)

# =========================================================
# HELPERS
# =========================================================

def clean_tmp():
    if not os.path.exists("/tmp"):
        os.makedirs("/tmp")
    for f in os.listdir("/tmp"):
        try:
            os.remove(os.path.join("/tmp", f))
        except:
            pass

def next_filename(n):
    return f"{n:03d}craft.mp4"

def load_state():
    """
    Returns (last_uploaded_number, next_schedule_datetime)
    The datetime will be the EXACT time the *next* video should go out.
    """
    try:
        buf = io.BytesIO()
        MediaIoBaseDownload(
            buf, drive.files().get_media(fileId=STATE_FILE_ID)
        ).next_chunk()
        
        data = json.loads(buf.getvalue())
        last_n = data.get("last_uploaded", 0)
        
        saved_date_str = data.get("next_schedule_date")
        if saved_date_str:
            # Load the date and ensure it has timezone info
            schedule_dt = datetime.fromisoformat(saved_date_str)
            if schedule_dt.tzinfo is None:
                schedule_dt = schedule_dt.replace(tzinfo=TZ)
        else:
            # Default to Tomorrow 8 AM if no file exists
            schedule_dt = datetime.now(TZ) + timedelta(days=1)
            schedule_dt = schedule_dt.replace(hour=TIME_SLOTS[0], minute=0, second=0, microsecond=0)
            
        return last_n, schedule_dt
    except Exception as e:
        print(f"Error loading state: {e}")
        # Fallback default
        d = datetime.now(TZ) + timedelta(days=1)
        return 0, d.replace(hour=TIME_SLOTS[0], minute=0, second=0, microsecond=0)

def save_state(n, next_date):
    """
    Saves the last uploaded number AND the next calculated schedule date
    """
    data = json.dumps({
        "last_uploaded": n,
        "next_schedule_date": next_date.isoformat()
    }).encode()
    
    media = MediaIoBaseUpload(
        io.BytesIO(data),
        mimetype="application/json"
    )
    drive.files().update(
        fileId=STATE_FILE_ID,
        media_body=media
    ).execute()

def find_video(name):
    res = drive.files().list(
        q=f"'{VIDEO_FOLDER_ID}' in parents and name='{name}' and trashed=false",
        fields="files(id,name)",
        pageSize=1
    ).execute()
    files = res.get("files", [])
    return files[0] if files else None

def list_audios():
    return drive.files().list(
        q=f"'{AUDIO_FOLDER_ID}' in parents and trashed=false",
        fields="files(id,name)"
    ).execute()["files"]

def download(fid, path):
    req = drive.files().get_media(fileId=fid)
    with open(path, "wb") as f:
        dl = MediaIoBaseDownload(f, req)
        done = False
        while not done:
            _, done = dl.next_chunk()

def random_title():
    adjectives = ["Satisfying", "Oddly Satisfying", "Relaxing", "Crazy", "Impossible"]
    actions = ["Drawing", "Painting", "Sketching", "Sculpting"]
    mediums = ["Acrylics", "Watercolors", "Pencil", "Charcoal"]
    subjects = ["Anime Eyes", "a Dragon", "a Landscape", "a Portrait"]
    emojis = ["🎨", "✨", "🔥", "🖌️"]
    hashtags = ["#shorts", "#art", "#drawing"]
    
    return f"{random.choice(adjectives)} {random.choice(mediums)} {random.choice(actions)} {random.choice(emojis)} {random.choice(hashtags)}"

# =========================================================
# CORE SCHEDULER (THREADED & SMART)
# =========================================================

def scheduler_thread():
    global SCHEDULER_RUNNING
    clean_tmp()

    # 1. Load exactly where we left off
    last_uploaded, next_publish_time = load_state()
    audios = list_audios()
    
    # Safety: If the loaded time is in the past, bump it to the future
    # (keeps the same time slot, just moves to tomorrow)
    if next_publish_time < datetime.now(TZ):
        print("⚠️ Saved time was in the past. Moving to tomorrow.")
        next_publish_time += timedelta(days=1)

    tg(f"▶️ <b>Scheduler started</b>\nNext: #{last_uploaded + 1}\nAt: {next_publish_time.strftime('%d %b %H:%M')}")

    while SCHEDULER_RUNNING:
        # --- PREPARE ---
        next_num = last_uploaded + 1
        fname = next_filename(next_num)
        file = find_video(fname)

        if not file:
            tg("🏁 <b>No more videos found</b>")
            SCHEDULER_RUNNING = False
            return

        # --- UPLOAD ---
        # Use the exact time loaded from state (or calculated from previous loop)
        publish_at = next_publish_time
        
        title = random_title()
        tags = random.sample(TAG_POOL, min(10, len(TAG_POOL)))
        description = f"{title}\n\n{BASE_DESCRIPTION}\n\n{', '.join(tags)}"

        vid = f"/tmp/{fname}"
        aud = random.choice(audios)
        aud_p = f"/tmp/{aud['name']}"
        out = f"/tmp/out_{fname}"

        try:
            download(file["id"], vid)
            download(aud["id"], aud_p)

            subprocess.run([
                "ffmpeg","-y",
                "-i",vid,"-i",aud_p,
                "-filter_complex",
                f"[1:a]volume=0.45[bg];"
                f"[0:v]drawtext=fontfile={FONT_PATH}:"
                f"text='{WATERMARK}':x=10:y=10:fontsize=24:fontcolor=white@0.4[v]",
                "-map","[v]","-map","[bg]","-shortest",out
            ], check=True)

            youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet":{
                        "title": title,
                        "description": description,
                        "tags": tags,
                        "categoryId":"26"
                    },
                    "status":{
                        "privacyStatus":"private",
                        "publishAt": publish_at.isoformat()
                    }
                },
                media_body=MediaFileUpload(out)
            ).execute()

        except Exception as e:
            clean_tmp()
            tg(f"❌ <b>Error:</b> <code>{str(e)}</code>")
            SCHEDULER_RUNNING = False
            return

        # --- CALCULATE NEXT SLOT (THE HOPPING LOGIC) ---
        current_hour = publish_at.hour
        
        try:
            # Find which slot we just used (e.g., index 0 for 8am)
            idx = TIME_SLOTS.index(current_hour)
            
            if idx < len(TIME_SLOTS) - 1:
                # If there are more slots today (e.g., 8 -> 12, or 12 -> 16)
                new_hour = TIME_SLOTS[idx + 1]
                # Same day, new hour
                next_publish_time = publish_at.replace(hour=new_hour, minute=0, second=0)
            else:
                # If we just did the last slot (16), move to tomorrow first slot (8)
                new_hour = TIME_SLOTS[0]
                next_publish_time = publish_at + timedelta(days=1)
                next_publish_time = next_publish_time.replace(hour=new_hour, minute=0, second=0)
                
        except ValueError:
            # Fallback if the hour isn't in TIME_SLOTS for some reason
            next_publish_time = publish_at + timedelta(days=1)
            next_publish_time = next_publish_time.replace(hour=TIME_SLOTS[0], minute=0, second=0)

        # --- SAVE STATE ---
        # We save the calculated time for the NEXT video immediately
        save_state(next_num, next_publish_time)
        last_uploaded = next_num

        tg(
            f"✅ <b>Uploaded #{next_num}</b>\n"
            f"📅 {publish_at.strftime('%d %b • %H:%M')}\n"
            f"⏭️ Next: {next_publish_time.strftime('%H:%M')}"
        )

        # Cleanup
        if os.path.exists(vid): os.remove(vid)
        if os.path.exists(aud_p): os.remove(aud_p)
        if os.path.exists(out): os.remove(out)

        # Sleep (approx 2 mins to avoid quota rate limits)
        time.sleep(random.randint(60,120))

# =========================================================
# TELEGRAM COMMAND LOOP
# =========================================================

tg("🤖 <b>Bot online</b>\n/schedule /status /help")

offset = 0

while True:
    try:
        r = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates",
            params={"offset": offset + 1},
            timeout=30
        ).json()
    except Exception:
        time.sleep(5)
        continue

    for u in r.get("result", []):
        offset = u["update_id"]

        if "message" not in u:
            continue

        text = u["message"].get("text","").strip().lower()

        if text == "/help":
            tg(
                "<b>Commands</b>\n"
                "/schedule – Start background upload\n"
                "/stop – Stop uploading\n"
                "/status – Check progress\n"
                "/reset_tmp – Clear temp files"
            )

        elif text == "/status":
            # Load state to see current progress
            last_up, next_dt = load_state()
            bar = progress_bar(last_up, TOTAL_VIDEOS)
            status_text = "🟢 Running" if SCHEDULER_RUNNING else "🔴 Stopped"
            
            tg(
                f"📊 <b>Status: {status_text}</b>\n\n"
                f"{bar}\n"
                f"Videos: {last_up} / {TOTAL_VIDEOS}\n"
                f"Next Sched: {next_dt.strftime('%d %b %H:%M')}"
            )

        elif text == "/reset_tmp":
            clean_tmp()
            tg("🧹 <b>/tmp cleaned</b>")

        elif text == "/schedule":
            if SCHEDULER_RUNNING:
                tg("⚠️ <b>Scheduler is already running!</b>")
            else:
                SCHEDULER_RUNNING = True
                # Start the thread
                t = threading.Thread(target=scheduler_thread)
                t.daemon = True  # Thread dies if main program dies
                t.start()

        elif text == "/stop":
            if SCHEDULER_RUNNING:
                SCHEDULER_RUNNING = False
                tg("🛑 <b>Stopping after current upload...</b>")
            else:
                tg("It is already stopped.")

    time.sleep(2)
