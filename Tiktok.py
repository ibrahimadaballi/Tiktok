import requests, sys, json, uuid, time, os, threading, re
from colorama import init, Fore, Back, Style

# Pydroid3 uyumlu bip sesi
def bip():
    print('\a', end='', flush=True)

# Terminal temizleme ve renkleri başlat
os.system('cls' if os.name=='nt' else 'clear')
init(autoreset=True)

API = "https://zefame-free.com/api_free.php?action=config"

names = {
    229: "TikTok Görüntüleme",
    228: "TikTok Takipçi",
    232: "TikTok Beğeni",
    235: "TikTok Paylaş",
    236: "TikTok Kaydetme"
}

# Banner
print(f"{Fore.YELLOW}{Back.BLUE}{'='*50}")
print(f"{Fore.YELLOW}{Back.BLUE}{'   TIKTOK OTOMASYON BOTU   ':^0}")
print(f"{Fore.YELLOW}{Back.BLUE}{'='*50}{Style.RESET_ALL}\n")

# Servisleri çekme
if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        data = json.load(f)
else:
    data = requests.get(API).json()

services = data.get('data', {}).get('tiktok', {}).get('services', [])
for i, service in enumerate(services, 1):
    sid = service.get('id')
    name = names.get(sid, service.get('name', '').strip())
    rate = service.get('description', '').strip()
    if rate:
        rate = f"[{rate.replace('vues', 'views').replace('partages', 'shares').replace('favoris', 'favorites')}]"
    
    status = f"{Fore.GREEN}[ÇALIŞIYOR]{Style.RESET_ALL}" if service.get('available') else f"{Fore.RED}[DURDURULDU]{Style.RESET_ALL}"
    print(f"{Fore.CYAN}{i}. {Style.BRIGHT}{name:<20} {status:<15} {Fore.MAGENTA}{rate}{Style.RESET_ALL}")

# Servis seçimi (birden fazla destekli)
choice = input(f"\n{Fore.YELLOW}{Style.BRIGHT}Bir veya birden fazla sayı gir (virgül ile ayır): {Style.RESET_ALL}").strip()
if not choice:
    sys.exit()

try:
    selected_indices = [int(x) for x in choice.split(",") if x.strip().isdigit()]
except:
    print(f"{Fore.RED}Geçersiz giriş!{Style.RESET_ALL}")
    sys.exit()

# Seçilen servisler
selected_services = [services[i-1] for i in selected_indices if 1 <= i <= len(services)]

# Takipçi servisi varsa kullanıcı linki al, yoksa video linki
has_follow = any(s.get('id') == 228 for s in selected_services)
if has_follow:
    link = input(f"{Fore.YELLOW}{Style.BRIGHT}Kullanıcı Linki (https://www.tiktok.com/@username): {Style.RESET_ALL}").strip()
else:
    link = input(f"{Fore.YELLOW}{Style.BRIGHT}Video Linki: {Style.RESET_ALL}").strip()

# Video ID kontrolü (takipçi için gerek yok)
video_id = None
if not has_follow:
    try:
        id_check = requests.post("https://zefame-free.com/api_free.php?", data={"action": "checkVideoId", "link": link})
        video_id = id_check.json().get("data", {}).get("videoId")
        print(f"{Fore.GREEN}{Style.BRIGHT}Video ID: {video_id}{Style.RESET_ALL}\n")
    except:
        print(f"{Fore.RED}Video ID alınamadı!{Style.RESET_ALL}")

# Log dosyası
log_file = "tiktok_bot_log.txt"

# Tek görev çalışan fonksiyon
def run_task(service):
    service_id = service.get('id')
    service_name = names.get(service_id, service.get('name', 'Bilinmeyen'))
    
    while True:
        try:
            order = requests.post(
                "https://zefame-free.com/api_free.php?action=order",
                data={
                    "service": service_id,
                    "link": link,
                    "uuid": str(uuid.uuid4()),
                    "videoId": video_id or ""
                }
            )
            result = order.json()
            message = result.get("message", "")
            order_id = result.get("data", {}).get("orderId")
            print(f"\n{Fore.CYAN}[{service_name}] Sipariş sonucu: {message} | ID: {order_id}{Style.RESET_ALL}")
            
            # Log kaydet
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{time.ctime()}] {service_name}: {message} | ID: {order_id}\n")

            # Bekleme süresi belirleme
            wait = result.get("data", {}).get("nextAvailable")
            wait_seconds = 0
            if wait:
                try:
                    wait = float(wait)
                    if wait > time.time():
                        wait_seconds = int(wait - time.time())
                except:
                    pass
            else:
                # API mesajından süreyi bul
                match = re.search(r"(\d+)\s*minute[s]?\s*et\s*(\d+)\s*seconde", message)
                if match:
                    mins = int(match.group(1))
                    secs = int(match.group(2))
                    wait_seconds = mins * 60 + secs
                elif "minute" in message:
                    m = re.search(r"(\d+)\s*minute", message)
                    if m: wait_seconds = int(m.group(1)) * 60
                elif "seconde" in message:
                    s = re.search(r"(\d+)\s*seconde", message)
                    if s: wait_seconds = int(s.group(1))
            
            # Ek 10 saniye
            wait_seconds += 10
            if wait_seconds <= 0:
                wait_seconds = 60
            
            # Geri sayım
            for remaining in range(wait_seconds, 0, -1):
                mins, secs = divmod(remaining, 60)
                print(f"\r{Fore.YELLOW}[{service_name}] Geri sayım: {mins:02d}:{secs:02d}{Style.RESET_ALL}", end="")
                time.sleep(1)
            
            bip()
            print(f"\n{Fore.GREEN}[{service_name}] Yeni sipariş zamanı!{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}[{service_name}] Hata: {e}{Style.RESET_ALL}")
            time.sleep(30)

# Her servis için thread başlat
for s in selected_services:
    threading.Thread(target=run_task, args=(s,), daemon=True).start()

print(f"\n{Fore.GREEN} {Style.RESET_ALL}")
while True:
    time.sleep(1)