import customtkinter as ctk
import socket
import requests
import threading
import time

# --- GÜVENLİK VE MİMARİ NOTLARI (VY-OSINTFramework) ---
# 1. Pasif OSINT: Hedefe doğrudan saldırı/istek yapılmaz.
# 2. Sıfır Telemetri: Kullanıcı verisi hiçbir şekilde üçüncü partilerle paylaşılmaz.
# 3. Asenkron Mimari: Ağ istekleri sırasında UI (Arayüz) donmaz.

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VY_OSINT_Framework(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VY OSINT Framework - Lab v1.2")
        self.geometry("850x600")

        # --- SEKME (TAB) MİMARİSİ ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_1 = self.tabview.add("1. Altyapı OSINT")
        self.tab_2 = self.tabview.add("2. Ayak İzi Avcısı")
        self.tab_3 = self.tabview.add("3. Medya Analizi") # Gelecek Modül İçin Hazırlık

        self.setup_tab_1()
        self.setup_tab_2()
        self.setup_tab_3()

    # ==========================================
    # MODÜL 1: ALTYAPI İSTİHBARATI (DOMAIN/IP)
    # ==========================================
    def setup_tab_1(self):
        self.label_title_t1 = ctk.CTkLabel(self.tab_1, text="🛡️ Hedef Altyapı İstihbaratı", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_title_t1.pack(pady=(10, 5))

        self.frame_input_t1 = ctk.CTkFrame(self.tab_1, fg_color="transparent")
        self.frame_input_t1.pack(pady=5, padx=10, fill="x")

        self.entry_target_t1 = ctk.CTkEntry(self.frame_input_t1, placeholder_text="Hedef Domain veya IP girin...", height=35)
        self.entry_target_t1.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_scan_t1 = ctk.CTkButton(self.frame_input_t1, text="İSTİHBARAT TOPLA", height=35, font=ctk.CTkFont(weight="bold"), command=self.start_osint_thread)
        self.btn_scan_t1.pack(side="right")

        self.txt_results_t1 = ctk.CTkTextbox(self.tab_1, font=ctk.CTkFont(family="Consolas", size=13), wrap="word")
        self.txt_results_t1.pack(pady=10, padx=10, fill="both", expand=True)
        self.log_t1("[*] Sistem Hazır. %100 Pasif tarama için hedef giriniz...")

    def log_t1(self, message):
        self.txt_results_t1.configure(state="normal")
        self.txt_results_t1.insert("end", message + "\n")
        self.txt_results_t1.see("end")
        self.txt_results_t1.configure(state="disabled")

    def start_osint_thread(self):
        target = self.entry_target_t1.get().strip()
        if not target:
            self.log_t1("[❌] HATA: Lütfen geçerli bir hedef girin.")
            return

        if "://" in target:
            target = target.split("://")[1].split("/")[0]

        self.btn_scan_t1.configure(state="disabled", text="TARANIYOR...")
        self.log_t1(f"\n[{'-'*40}]\n[+] YENİ TARAMA BAŞLATILDI: {target}\n[{'-'*40}]")
        threading.Thread(target=self.run_osint, args=(target,), daemon=True).start()

    def run_osint(self, target):
        try:
            self.log_t1("[*] Adım 1: IP Adresi Çözümleniyor...")
            target_ip = socket.gethostbyname(target)
            self.log_t1(f"    ✅ IP Adresi: {target_ip}")

            self.log_t1("\n[*] Adım 2: ISP Analizi (Pasif)...")
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) VY-OSINT/1.1"}
            geo_response = requests.get(f"https://ipinfo.io/{target_ip}/json", headers=headers, timeout=5)
            
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                self.log_t1(f"    ✅ Ülke: {geo_data.get('country', 'Bilinmiyor')}")
                self.log_t1(f"    ✅ ISP: {geo_data.get('org', 'Bilinmiyor')}")

            self.log_t1("\n[*] Adım 3: Header Analizi (HackerTarget API)...")
            try:
                ht_response = requests.get(f"https://api.hackertarget.com/httpheaders/?q={target}", headers=headers, timeout=10)
                if ht_response.status_code == 200 and "error" not in ht_response.text.lower():
                    for line in ht_response.text.split('\n')[:5]:
                        if line.strip() and not line.startswith("http"):
                            self.log_t1(f"       - {line.strip()}")
            except requests.exceptions.RequestException:
                self.log_t1("    ❌ OSINT servisine bağlanılamadı.")

            self.log_t1("\n[+] İSTİHBARAT TAMAMLANDI.")
        except socket.gaierror:
            self.log_t1("\n[❌] HATA: Adres çözümlenemedi.")
        except Exception as e:
            self.log_t1(f"\n[❌] KRİTİK HATA: {str(e)}")
        finally:
            self.after(100, lambda: self.btn_scan_t1.configure(state="normal", text="İSTİHBARAT TOPLA"))

    # ==========================================
    # MODÜL 2: DİJİTAL AYAK İZİ (USERNAME ENUMERATION)
    # ==========================================
    def setup_tab_2(self):
        self.label_title_t2 = ctk.CTkLabel(self.tab_2, text="👤 Dijital Ayak İzi Avcısı", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_title_t2.pack(pady=(10, 5))

        self.frame_input_t2 = ctk.CTkFrame(self.tab_2, fg_color="transparent")
        self.frame_input_t2.pack(pady=5, padx=10, fill="x")

        self.entry_target_t2 = ctk.CTkEntry(self.frame_input_t2, placeholder_text="Kullanıcı adı girin (Örn: volkanyildirim)...", height=35)
        self.entry_target_t2.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_scan_t2 = ctk.CTkButton(self.frame_input_t2, text="KULLANICIYI ARA", height=35, font=ctk.CTkFont(weight="bold"), command=self.start_enum_thread)
        self.btn_scan_t2.pack(side="right")

        self.txt_results_t2 = ctk.CTkTextbox(self.tab_2, font=ctk.CTkFont(family="Consolas", size=13), wrap="word")
        self.txt_results_t2.pack(pady=10, padx=10, fill="both", expand=True)
        self.log_t2("[*] Ayak İzi Modülü Hazır. Genişletilmiş platformlar üzerinden pasif tarama yapılacaktır...")

    def log_t2(self, message):
        self.txt_results_t2.configure(state="normal")
        self.txt_results_t2.insert("end", message + "\n")
        self.txt_results_t2.see("end")
        self.txt_results_t2.configure(state="disabled")

    def start_enum_thread(self):
        username = self.entry_target_t2.get().strip()
        if not username:
            self.log_t2("[❌] HATA: Lütfen bir kullanıcı adı girin.")
            return

        if " " in username:
            self.log_t2("[❌] HATA: Kullanıcı adları boşluk içeremez.")
            return

        self.btn_scan_t2.configure(state="disabled", text="ARANIYOR...")
        self.log_t2(f"\n[{'-'*40}]\n[+] HEDEF: '{username}' İÇİN TARAMA BAŞLADI\n[{'-'*40}]")
        threading.Thread(target=self.run_username_enumeration, args=(username,), daemon=True).start()

    def run_username_enumeration(self, username):
        """Kullanıcı adını popüler platformlarda arar (Sahte Pozitif Korumalı)."""
        platforms = {
            "YouTube": f"https://www.youtube.com/@{username}",
            "Twitch": f"https://www.twitch.tv/{username}",
            "Pinterest": f"https://tr.pinterest.com/{username}/",
            "Spotify": f"https://open.spotify.com/user/{username}",
            "Medium": f"https://medium.com/@{username}",
            "Telegram": f"https://t.me/{username}",
            "GitHub": f"https://github.com/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "Vimeo": f"https://vimeo.com/{username}",
            "SoundCloud": f"https://soundcloud.com/{username}",
        }

        # --- SAHTE POZİTİF (FALSE-POSITIVE) KALKANI ---
        # Platformların 200 OK döndürüp aslında "kullanıcı yok" dediği anahtar kelimeler
        error_flags = {
            "Twitch": ["content is unavailable", "core-error-message"],
            "Pinterest": ["Not Found", "bulunamadı", "hata"],
            "YouTube": ["Not Found", "404", "bulunamadı"],
            "Spotify": ["not found", "bulunamadı"],
            "Medium": ["Out of nothing, something", "404"],
            "SoundCloud": ["we can't find that user", "404"],
            "Vimeo": ["404"]
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.5"
        }
        
        found_count = 0

        for site, url in platforms.items():
            self.log_t2(f"[*] {site} platformu kontrol ediliyor...")
            try:
                time.sleep(0.7) 
                response = requests.get(url, headers=headers, timeout=8, allow_redirects=False)
                
                if response.status_code == 200:
                    html_content = response.text.lower()
                    is_false_positive = False
                    
                    # Eğer platformun bilinen bir hata imzası varsa, HTML içinde onu ara
                    if site in error_flags:
                        for flag in error_flags[site]:
                            if flag.lower() in html_content:
                                is_false_positive = True
                                break # Hata imzası bulundu, aramayı kes
                    
                    if not is_false_positive:
                        self.log_t2(f"    ✅ BULUNDU: {url}")
                        found_count += 1
                    else:
                         pass # Soft 404 yakalandı, ekrana yazdırma
                         
                elif response.status_code in [301, 302]:
                    if site == "Telegram":
                        self.log_t2(f"    ✅ BULUNDU: {url}")
                        found_count += 1
                elif response.status_code == 404:
                    pass
                else:
                    self.log_t2(f"    ⚠️ Yanıt kodu: {response.status_code} ({site}) - WAF Koruması")
            except requests.exceptions.RequestException:
                self.log_t2(f"    ❌ Bağlantı hatası ({site})")

        self.log_t2(f"\n[+] TARAMA BİTTİ. Toplam {found_count}/{len(platforms)} platformda eşleşme bulundu.")
        self.after(100, lambda: self.btn_scan_t2.configure(state="normal", text="KULLANICIYI ARA"))

    # ==========================================
    # MODÜL 3: MEDYA ADLİ BİLİŞİMİ (EXIF)
    # ==========================================
    def setup_tab_3(self):
        self.label_t3 = ctk.CTkLabel(self.tab_3, text="📷 Medya Adli Bilişimi (Çok Yakında)", font=ctk.CTkFont(size=14, slant="italic"))
        self.label_t3.pack(pady=50)

if __name__ == "__main__":
    app = VY_OSINT_Framework()
    app.mainloop()