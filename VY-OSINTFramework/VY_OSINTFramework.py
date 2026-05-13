
import customtkinter as ctk
import socket
import requests
import threading

# --- GÜVENLİK VE MİMARİ NOTLARI ---
# 1. Pasif OSINT: Hedefe doğrudan saldırı yapılmaz, kısıtlı ve güvenli API'ler kullanılır.
# 2. Timeout (Zaman Aşımı): Karşı sunucu veya API yanıt vermezse programın çökmemesi için requests kütüphanesine timeout eklenmiştir.
# 3. Threading (Çoklu İşlem): Ağ sorguları UI'ı dondurmasın diye işlemler arka plana alınmıştır.

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VY_OSINT_Framework(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VY OSINT Framework - Lab v1.0")
        self.geometry("700x500")

        # 1. ÜST BAŞLIK ALANI
        self.label_title = ctk.CTkLabel(self, text="🛡️ Hedef Altyapı İstihbaratı (Pasif Bilgi Toplama)", font=ctk.CTkFont(size=18, weight="bold"))
        self.label_title.pack(pady=(20, 10))

        # 2. HEDEF GİRİŞ ALANI
        self.frame_input = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_input.pack(pady=10, padx=20, fill="x")

        self.entry_target = ctk.CTkEntry(self.frame_input, placeholder_text="Hedef Domain veya IP girin (Örn: volkanyildirim.com.tr)", height=40)
        self.entry_target.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_scan = ctk.CTkButton(self.frame_input, text="İSTİHBARAT TOPLA", height=40, font=ctk.CTkFont(weight="bold"), command=self.start_osint_thread)
        self.btn_scan.pack(side="right")

        # 3. SONUÇ EKRANI (LOG)
        self.txt_results = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=13), wrap="word")
        self.txt_results.pack(pady=10, padx=20, fill="both", expand=True)
        self.txt_results.insert("0.0", "[*] Sistem Hazır. Pasif tarama için hedef giriniz...\n")
        self.txt_results.configure(state="disabled")

    def log(self, message):
        """Sonuç ekranına güvenli veri yazma fonksiyonu."""
        self.txt_results.configure(state="normal")
        self.txt_results.insert("end", message + "\n")
        self.txt_results.see("end")
        self.txt_results.configure(state="disabled")

    def start_osint_thread(self):
        """Arayüzün donmasını engellemek için işlemi arka plana (Thread) atar."""
        target = self.entry_target.get().strip()
        if not target:
            self.log("[❌] HATA: Lütfen geçerli bir hedef girin.")
            return

        # URL Temizleme (http:// veya https:// varsa at)
        if "://" in target:
            target = target.split("://")[1].split("/")[0]

        self.btn_scan.configure(state="disabled", text="TARANIYOR...")
        self.log(f"\n[{'-'*40}]\n[+] YENİ İSTİHBARAT DÖNGÜSÜ BAŞLATILDI: {target}\n[{'-'*40}]")
        
        threading.Thread(target=self.run_osint, args=(target,), daemon=True).start()

    def run_osint(self, target):
        """Çekirdek OSINT Algoritmaları."""
        try:
            # ADIM 1: DNS & IP Çözümleme
            self.log("[*] Adım 1: IP Adresi Çözümleniyor...")
            target_ip = socket.gethostbyname(target)
            self.log(f"    ✅ Hedef IP Adresi: {target_ip}")

            # ADIM 2: Coğrafi Konum ve ISP İstihbaratı (ipinfo.io - API Key gerektirmez, pasif)
            self.log("\n[*] Adım 2: Coğrafi Konum ve Servis Sağlayıcı (ISP) Analizi...")
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"} # Güvenlik: Bot engeline takılmamak için
            geo_response = requests.get(f"https://ipinfo.io/{target_ip}/json", headers=headers, timeout=5)
            
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                self.log(f"    ✅ Şehir/Ülke: {geo_data.get('city', 'Bilinmiyor')}, {geo_data.get('country', 'Bilinmiyor')}")
                self.log(f"    ✅ Lokasyon (Enlem,Boylam): {geo_data.get('loc', 'Bilinmiyor')}")
                self.log(f"    ✅ Servis Sağlayıcı (ASN): {geo_data.get('org', 'Bilinmiyor')}")
            else:
                self.log("    ❌ Konum API'si yanıt vermedi.")

            # ADIM 3: Pasif Sunucu Başlık Analizi (HTTP Header Grabber)
            self.log("\n[*] Adım 3: Sunucu Teknolojisi Tespiti (Header Grabber)...")
            try:
                http_response = requests.get(f"http://{target}", headers=headers, timeout=5)
                server = http_response.headers.get('Server', 'Gizlenmiş (Güvenlik Yapılandırması Aktif)')
                tech = http_response.headers.get('X-Powered-By', 'Tespit Edilemedi')
                self.log(f"    ✅ Sunucu Yazılımı: {server}")
                self.log(f"    ✅ Arka Plan Teknolojisi: {tech}")
            except requests.exceptions.RequestException:
                self.log("    ❌ Sunucuya HTTP isteği yapılamadı (Koruma veya Kapalı Port).")

            self.log(f"\n[+] İSTİHBARAT RAPORU TAMAMLANDI.")

        except socket.gaierror:
            self.log(f"\n[❌] HATA: '{target}' adresi çözümlenemedi. Geçerli bir domain veya IP olduğundan emin olun!")
        except Exception as e:
            self.log(f"\n[❌] KRİTİK HATA: Beklenmeyen bir istisna oluştu: {str(e)}")
        finally:
            self.after(100, self.reset_ui)

    def reset_ui(self):
        """İşlem bitince arayüzü eski haline getirir."""
        self.btn_scan.configure(state="normal", text="İSTİHBARAT TOPLA")

if __name__ == "__main__":
    app = VY_OSINT_Framework()
    app.mainloop()