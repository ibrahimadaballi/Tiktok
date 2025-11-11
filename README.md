# TikTok Otomasyon Botu

Bu proje, TikTok için otomatik **Görüntüleme, Beğeni, Takipçi, Paylaşma ve Kaydetme** işlemleri yapabilen bir Python botudur.  
Bot, **Pydroid3** ve **Termux** üzerinde çalışacak şekilde tasarlanmıştır.

---

## ⚙️ Özellikler
- Video linki veya kullanıcı profili linki ile sipariş oluşturur.
- Birden fazla servisi aynı anda çalıştırabilir.
- Her sipariş için geri sayım yapar ve 10 saniye ekstra bekler.
- Sipariş sonuçlarını `tiktok_bot_log.txt` dosyasına kaydeder.
- Sonsuz döngü ile durmadan çalışır.
- Pydroid3 ve Termux uyumlu.

---

## 🛠 Kurulum

### 1️⃣ Python ve pip
Termux:
```bash
pkg update && pkg upgrade -y

pkg install python git -y

git clone https://github.com/ibrahimadaballi/Tiktok
cd Tiktok
ls
tiktok.py

