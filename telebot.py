import os, io, json, time, random, subprocess, requests
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

START_DATE = datetime(2026, 2, 10, 8, 0, tzinfo=TZ)
TIME_SLOTS = [8, 12, 16]
MAX_PER_DAY = 3

WATERMARK = "@ArtWeaver"
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
#mrindianhackers #lyunaff #bkffofficial1 #equipou #manifestedit #khatushyambhajan #bullymaguire
"""

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

# =========================================================
# TELEGRAM
# =========================================================

def tg(msg):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={
            "chat_id": TELEGRAM_CHAT,
            "text": msg,
            "parse_mode": "HTML"
        },
        timeout=10
    )

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
    for f in os.listdir("/tmp"):
        try:
            os.remove(os.path.join("/tmp", f))
        except:
            pass

def next_filename(n):
    return f"{n:03d}craft.mp4"

def load_state():
    buf = io.BytesIO()
    MediaIoBaseDownload(buf, drive.files().get_media(fileId=STATE_FILE_ID)).next_chunk()
    return json.loads(buf.getvalue()).get("last_uploaded", 0)

def save_state(n):
    data = json.dumps({"last_uploaded": n}).encode()
    media = MediaIoBaseUpload(io.BytesIO(data), mimetype="application/json")
    drive.files().update(fileId=STATE_FILE_ID, media_body=media).execute()

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
    # --- WORD BANKS ---
    
    # Adjectives describing the process or result
    adjectives = [
        "Satisfying", "Oddly Satisfying", "Relaxing", "Crazy", "Impossible", 
        "Realistic", "3D", "Glowing", "Neon", "Tiny", "Huge", "Quick", "Easy", 
        "Simple", "Complex", "Abstract", "Detailed", "Messy", "Clean", "Perfect"
    ]

    # The specific art action being done
    actions = [
        "Drawing", "Painting", "Sketching", "Sculpting", "Crafting", "Mixing", 
        "Designing", "Coloring", "Building", "Restoring", "Doodling", "Shading",
        "Layering", "Carving", "Pouring", "Spraying"
    ]

    # The medium or tool used
    mediums = [
        "Acrylics", "Watercolors", "Pencil", "Charcoal", "Resin", "Clay", 
        "Polymer Clay", "Posca Markers", "Gouache", "Spray Paint", "Oil Pastels", 
        "Digital Art", "Procreate", "Ink", "Tape", "Paper", "Origami", "Slime"
    ]

    # What is being created
    subjects = [
        "Anime Eyes", "a Dragon", "a Landscape", "a Portrait", "an Illusion", 
        "a Logo", "a Mandala", "a Flower", "a Sunset", "a Galaxy", "a Pattern", 
        "Textures", "a Face", "Hands", "Lips", "a 3D Hole", "Among Us", 
        "Pokemon", "Naruto", "Demon Slayer", "Room Decor", "Stickers"
    ]

    # Engagement hooks (Shorts algorithm loves these)
    hooks = [
        "Wait for the end", "Don't blink", "Trust the process", "You won't believe this", 
        "Can I draw this?", "Turning trash into art", "ASMR Art", "My best work yet", 
        "I tried a hack", "Art Challenge", "Do not try this at home", "Satisfying peel", 
        "Mixing random colors", "Guess the drawing", "Rate this 1-10"
    ]

    # Emojis to make it pop
    emojis = [
        "🎨", "✨", "🔥", "🖌️", "🖍️", "😱", "🤩", "🧵", "🧶", "✏️", "🌈", 
        "🦋", "👀", "🖼️", "🤯", "🥶", "🟢", "💜", "🦄", "🌊"
    ]
    
    # Niche hashtags
    hashtags = ["#shorts", "#art", "#drawing", "#diy", "#satisfying", "#artist", "#painting", "#crafts"]

    # --- TEMPLATES ---
    # We randomize which sentence structure gets used to keep it fresh
    
    template_choice = random.randint(1, 7)
    
    if template_choice == 1:
        # Standard: "Satisfying Acrylic Painting 🎨 #shorts"
        return f"{random.choice(adjectives)} {random.choice(mediums)} {random.choice(actions)} {random.choice(emojis)} {random.choice(hashtags)}"
        
    elif template_choice == 2:
        # How-to: "How to Draw Anime Eyes (Easy) ✏️"
        return f"How to {random.choice(actions).lower()} {random.choice(subjects)} ({random.choice(adjectives)}) {random.choice(emojis)}"
        
    elif template_choice == 3:
        # Hook based: "Wait for the end... 😱 #art"
        return f"{random.choice(hooks)}... {random.choice(emojis)} {random.choice(hashtags)}"
        
    elif template_choice == 4:
        # Medium focus: "Drawing a Dragon with Posca Markers 🔥"
        return f"{random.choice(actions)} {random.choice(subjects)} with {random.choice(mediums)} {random.choice(emojis)}"
        
    elif template_choice == 5:
        # Hack/Challenge: "I tried this Crazy Art Hack! ✨"
        return f"I tried this {random.choice(adjectives)} Art Hack! {random.choice(emojis)}"
        
    elif template_choice == 6:
        # Progression Series: "Day 45 of Drawing every day 🖌️"
        # Randomizes the day number to make it look like a series
        day = random.randint(1, 365)
        return f"Day {day} of {random.choice(actions)} every day {random.choice(emojis)} {random.choice(hashtags)}"
    
    elif template_choice == 7:
        # ASMR Style: "ASMR: Mixing Clay (Satisfying) 🎧"
        return f"ASMR: {random.choice(actions)} {random.choice(mediums)} ({random.choice(adjectives)}) {random.choice(emojis)}"



# =========================================================
# CORE SCHEDULER
# =========================================================

def run_scheduler():
    clean_tmp()

    audios = list_audios()
    last_uploaded = load_state()

    schedule_day = START_DATE
    uploaded_today = 0

    tg("▶️ <b>/schedule started</b>")

    while True:
        next_num = last_uploaded + 1
        fname = next_filename(next_num)
        file = find_video(fname)

        if not file:
            tg("🏁 <b>No more videos found</b>")
            return

        if uploaded_today >= MAX_PER_DAY:
            schedule_day += timedelta(days=1)
            uploaded_today = 0

        publish_at = schedule_day.replace(hour=TIME_SLOTS[uploaded_today])

        title = random_title()
        tags = random.sample(TAG_POOL, min(10, len(TAG_POOL)))
        description = f"{title}\n\n{BASE_DESCRIPTION}\n\n{', '.join(tags)}"

        vid = f"/tmp/{fname}"
        aud = random.choice(audios)
        aud_p = f"/tmp/{aud['name']}"
        out = f"/tmp/out_{fname}"

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

        try:
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
        except HttpError as e:
            clean_tmp()
            tg(
                f"❌ <b>Upload stopped</b>\n\n"
                f"{fname}\n\n"
                f"<code>{str(e)}</code>"
            )
            return

        # ✅ SUCCESS → update state
        save_state(next_num)
        last_uploaded = next_num

        tg(
            f"✅ <b>Uploaded</b>\n\n"
            f"{fname}\n"
            f"📝 {title}\n"
            f"🕒 {publish_at.strftime('%d %b • %H:%M')}"
        )

        os.remove(vid)
        os.remove(aud_p)
        os.remove(out)

        uploaded_today += 1
        time.sleep(random.randint(60,120))

# =========================================================
# TELEGRAM COMMAND LOOP
# =========================================================

tg("🤖 <b>Bot online</b>\n/send /help")

offset = 0

while True:
    r = requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates",
        params={"offset": offset + 1},
        timeout=30
    ).json()

    for u in r.get("result", []):
        offset = u["update_id"]

        if "message" not in u:
            continue

        text = u["message"].get("text","").strip().lower()

        if text == "/help":
            tg(
                "<b>Commands</b>\n\n"
                "/schedule – start scheduling\n"
                "/status – progress\n"
                "/reset_tmp – clear temp\n"
                "/help – this message"
            )

        elif text == "/status":
            bar = progress_bar(last_processed, TOTAL_VIDEOS)
            tg(
                f"📊 <b>Status</b>\n\n"
                f"{bar}\n"
                f"{last_processed} / {TOTAL_VIDEOS}\n"
                f"Paused: {PAUSED}"
            )


        elif text == "/reset_tmp":
            clean_tmp()
            tg("🧹 <b>/tmp cleaned</b>")

        elif text == "/schedule":
            run_scheduler()

    time.sleep(2)
