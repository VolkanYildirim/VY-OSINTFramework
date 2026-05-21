import customtkinter as ctk
import socket
import requests
import threading
import time
import os
from tkinter import filedialog
from PIL import Image, ExifTags
import PyPDF2

# --- GÜVENLİK VE MİMARİ NOTLARI (VY-OSINTFramework) ---
# 1. Pasif OSINT: Hedefe doğrudan saldırı yapılmaz.
# 2. Sıfır Telemetri: Veriler dışarı sızdırılmaz. (Modül 3 %100 Çevrimdışı çalışır)
# 3. Asenkron Mimari: Ağ istekleri UI'ı dondurmaz.

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VY_OSINT_Framework(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VY OSINT Framework (Pro Edition)")
        self.geometry("900x650")

        # --- ÜST BAR (HEADER) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=15, pady=(15, 0))

        self.lbl_app_logo = ctk.CTkLabel(self.header_frame, text="🛡️ VY OSINT Framework", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_app_logo.pack(side="left")

        # Hakkında Butonu
        self.btn_about = ctk.CTkButton(self.header_frame, text="Hakkında", width=90, height=30, font=ctk.CTkFont(weight="bold"), command=self.show_about)
        self.btn_about.pack(side="right", padx=(10, 0)) # Araya 10px boşluk koyduk

        # Tema Seçici Açılır Menü (Yeni Eklendi)
        self.theme_menu = ctk.CTkOptionMenu(self.header_frame, values=["Karanlık", "Aydınlık"], command=self.change_theme, width=100, height=30)
        self.theme_menu.pack(side="right")
        self.theme_menu.set("Karanlık") # Varsayılan değer

        # --- SEKME (TAB) MİMARİSİ ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        self.tab_1 = self.tabview.add("1. Altyapı OSINT")
        self.tab_2 = self.tabview.add("2. Ayak İzi Avcısı")
        self.tab_3 = self.tabview.add("3. Medya Analizi")



        self.setup_tab_1()
        self.setup_tab_2()
        self.setup_tab_3()



    # ==========================================
    # MODÜL 1: ALTYAPI İSTİHBARATI (DOMAIN/IP)
    # ==========================================
    def show_about(self):

        """Hakkında (About) penceresini açar ve felsefeyi gösterir."""
        about_win = ctk.CTkToplevel(self)
        about_win.title("Hakkında")
        about_win.geometry("520x260")
        about_win.resizable(False, False)
        about_win.attributes("-topmost", True) # Pencerenin hep üstte kalmasını sağlar

        lbl_title = ctk.CTkLabel(about_win, text="VY OSINT Framework", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_title.pack(pady=(25, 5))

        lbl_version = ctk.CTkLabel(about_win, text="Version 1.0 (Pro Edition)", font=ctk.CTkFont(size=13), text_color="gray")
        lbl_version.pack(pady=(0, 15))

        desc = ("Bu yazılım; dijital mahremiyet (Privacy-First) ilkeleri gözetilerek,\n"
                "tamamen açık kaynaklı altyapılar kullanılarak geliştirilmiştir.\n"
                "Hiçbir kullanıcı verisi veya telemetri toplamaz ve dışarıya aktarmaz.")
        lbl_desc = ctk.CTkLabel(about_win, text=desc, font=ctk.CTkFont(size=13))
        lbl_desc.pack(pady=(0, 20))

        lbl_dev = ctk.CTkLabel(about_win, text="🛡️ Developed by Volkan YILDIRIM - Proctives\nwww.volkanyildirim.com.tr", font=ctk.CTkFont(size=13, weight="bold"))
        lbl_dev.pack(pady=(0, 10))

    def change_theme(self, new_theme: str):
        """Kullanıcının seçimine göre arayüz temasını değiştirir."""
        if new_theme == "Karanlık":
            ctk.set_appearance_mode("Dark")
        elif new_theme == "Aydınlık":
            ctk.set_appearance_mode("Light")

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
        if not target: return
        if "://" in target: target = target.split("://")[1].split("/")[0]

        self.btn_scan_t1.configure(state="disabled", text="TARANIYOR...")
        self.log_t1(f"\n[{'-'*40}]\n[+] YENİ TARAMA BAŞLATILDI: {target}\n[{'-'*40}]")
        threading.Thread(target=self.run_osint, args=(target,), daemon=True).start()

    def run_osint(self, target):
        try:
            self.log_t1("[*] Adım 1: IP Adresi Çözümleniyor...")
            target_ip = socket.gethostbyname(target)
            self.log_t1(f"    ✅ IP Adresi: {target_ip}")

            self.log_t1("\n[*] Adım 2: ISP Analizi (Pasif)...")
            headers = {"User-Agent": "Mozilla/5.0"}
            geo_response = requests.get(f"https://ipinfo.io/{target_ip}/json", headers=headers, timeout=5)
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                self.log_t1(f"    ✅ Ülke: {geo_data.get('country', 'Bilinmiyor')} | ISP: {geo_data.get('org', 'Bilinmiyor')}")

            self.log_t1("\n[*] Adım 3: Header Analizi (HackerTarget API)...")
            ht_response = requests.get(f"https://api.hackertarget.com/httpheaders/?q={target}", headers=headers, timeout=10)
            if ht_response.status_code == 200 and "error" not in ht_response.text.lower():
                for line in ht_response.text.split('\n')[:5]:
                    if line.strip() and not line.startswith("http"): self.log_t1(f"       - {line.strip()}")
            self.log_t1("\n[+] İSTİHBARAT TAMAMLANDI.")
        except Exception as e:
            self.log_t1(f"\n[❌] HATA: {str(e)}")
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

        self.entry_target_t2 = ctk.CTkEntry(self.frame_input_t2, placeholder_text="Kullanıcı adı girin...", height=35)
        self.entry_target_t2.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_scan_t2 = ctk.CTkButton(self.frame_input_t2, text="KULLANICIYI ARA", height=35, font=ctk.CTkFont(weight="bold"), command=self.start_enum_thread)
        self.btn_scan_t2.pack(side="right")

        self.txt_results_t2 = ctk.CTkTextbox(self.tab_2, font=ctk.CTkFont(family="Consolas", size=13), wrap="word")
        self.txt_results_t2.pack(pady=10, padx=10, fill="both", expand=True)
        self.log_t2("[*] Ayak İzi Modülü Hazır. Genişletilmiş platformlar kontrol edilecektir...")

    def log_t2(self, message):
        self.txt_results_t2.configure(state="normal")
        self.txt_results_t2.insert("end", message + "\n")
        self.txt_results_t2.see("end")
        self.txt_results_t2.configure(state="disabled")

    def start_enum_thread(self):
        username = self.entry_target_t2.get().strip()
        if not username or " " in username: return
        self.btn_scan_t2.configure(state="disabled", text="ARANIYOR...")
        self.log_t2(f"\n[{'-'*40}]\n[+] HEDEF: '{username}' İÇİN TARAMA BAŞLADI\n[{'-'*40}]")
        threading.Thread(target=self.run_username_enumeration, args=(username,), daemon=True).start()

    def run_username_enumeration(self, username):
        platforms = {
            "GitHub": f"https://github.com/{username}", "GitLab": f"https://gitlab.com/{username}",
            "Pastebin": f"https://pastebin.com/u/{username}", "HackTheBox": f"https://app.hackthebox.com/users/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}", "Telegram": f"https://t.me/{username}",
            "Flickr": f"https://www.flickr.com/people/{username}/", "Patreon": f"https://www.patreon.com/{username}",
            "Linktree": f"https://linktr.ee/{username}", "Blogger": f"https://{username}.blogspot.com/"
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        found_count = 0
        for site, url in platforms.items():
            self.log_t2(f"[*] {site} platformu kontrol ediliyor...")
            try:
                time.sleep(0.5) 
                response = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
                if response.status_code == 200:
                    self.log_t2(f"    ✅ BULUNDU: {url}")
                    found_count += 1
                elif response.status_code == 404: self.log_t2("    [-] Bulunamadı.")
            except Exception: self.log_t2("    [-] Bulunamadı. (Alan adı yok)")
        self.log_t2(f"\n[+] TARAMA BİTTİ. {found_count}/{len(platforms)} platformda iz bulundu.")
        self.after(100, lambda: self.btn_scan_t2.configure(state="normal", text="KULLANICIYI ARA"))

    # ==========================================
    # MODÜL 3: MEDYA ADLİ BİLİŞİMİ (EXIF & METADATA)
    # ==========================================
    def setup_tab_3(self):
        self.label_title_t3 = ctk.CTkLabel(self.tab_3, text="📷 Çevrimdışı Medya Adli Bilişimi (EXIF/Metadata)", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_title_t3.pack(pady=(10, 5))

        self.btn_select_file = ctk.CTkButton(self.tab_3, text="DOSYA SEÇ (Resim veya PDF)", height=40, font=ctk.CTkFont(weight="bold"), fg_color="#8B0000", hover_color="#5C0000", command=self.analyze_media)
        self.btn_select_file.pack(pady=10)

        self.txt_results_t3 = ctk.CTkTextbox(self.tab_3, font=ctk.CTkFont(family="Consolas", size=13), wrap="word")
        self.txt_results_t3.pack(pady=10, padx=10, fill="both", expand=True)
        self.log_t3("[*] Modül 3 Hazır. Veriler sunucuya gönderilmez, cihazınızda (%100 Çevrimdışı) analiz edilir.")

    def log_t3(self, message):
        self.txt_results_t3.configure(state="normal")
        self.txt_results_t3.insert("end", message + "\n")
        self.txt_results_t3.see("end")
        self.txt_results_t3.configure(state="disabled")

    def analyze_media(self):
        """Kullanıcıdan dosya alır ve uzantısına göre analiz motoruna yönlendirir."""
        filepath = filedialog.askopenfilename(
            title="Analiz Edilecek Dosyayı Seçin",
            filetypes=(("Tüm Desteklenen Dosyalar", "*.jpg *.jpeg *.png *.pdf"), ("Resimler", "*.jpg *.jpeg *.png"), ("PDF Belgeleri", "*.pdf"))
        )
        
        if not filepath: return # Kullanıcı iptal etti
        
        filename = os.path.basename(filepath)
        self.log_t3(f"\n[{'-'*50}]\n[+] HEDEF DOSYA: {filename}\n[{'-'*50}]")
        
        ext = filename.lower().split('.')[-1]
        
        if ext in ['jpg', 'jpeg', 'png']:
            self.extract_image_exif(filepath)
        elif ext == 'pdf':
            self.extract_pdf_metadata(filepath)
        else:
            self.log_t3("❌ Desteklenmeyen dosya formatı.")

    def extract_image_exif(self, filepath):
        """Resimlerdeki gizli EXIF meta verilerini çıkartır."""
        self.log_t3("[*] İşlem: Görüntü Analizi Başladı...")
        try:
            image = Image.open(filepath)
            exif_data = image._getexif()
            
            if not exif_data:
                self.log_t3("[-] Bu fotoğrafta okunabilir bir EXIF meta verisi bulunamadı. (Sosyal medyadan indirilmiş veya temizlenmiş olabilir).")
                return

            self.log_t3("[+] EXIF Verileri Bulundu:\n")
            found_gps = False
            
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                
                # Sadece okunabilir ve işe yarar verileri filtreliyoruz
                if isinstance(value, bytes): continue 
                
                if tag_name == "GPSInfo":
                    found_gps = True
                    self.log_t3(f"    🌍 {tag_name}: [GİZLİ KOORDİNATLAR TESPİT EDİLDİ]")
                else:
                    # Uzun dataları kısalt
                    val_str = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                    self.log_t3(f"    ✔️ {tag_name}: {val_str}")
                    
            if not found_gps:
                self.log_t3("\n[-] GPS Koordinat verisi bulunamadı.")
                
        except Exception as e:
            self.log_t3(f"❌ Resim analiz hatası: {str(e)}")

    def extract_pdf_metadata(self, filepath):
        """PDF belgelerindeki gizli meta verileri çıkartır."""
        self.log_t3("[*] İşlem: PDF Belge Analizi Başladı...")
        try:
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                info = reader.metadata
                
                if not info:
                    self.log_t3("[-] Bu PDF dosyasında meta veri bulunamadı.")
                    return

                self.log_t3("[+] PDF Meta Verileri Bulundu:\n")
                for key, value in info.items():
                    # /Author gibi key'lerin başındaki slash'i temizle
                    clean_key = key.replace("/", "") 
                    self.log_t3(f"    📄 {clean_key}: {value}")
                    
        except Exception as e:
            self.log_t3(f"❌ PDF analiz hatası: {str(e)}")

if __name__ == "__main__":
    app = VY_OSINT_Framework()
    app.mainloop()