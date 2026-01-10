import tkinter as tk
from tkinter import messagebox
from config import Oturum

from arayuz.uye_ekrani import UyeEkrani
from arayuz.kitap_ekrani import KitapEkrani
from arayuz.odunc_ekrani import OduncEkrani
from arayuz.rapor_ekrani import RaporEkrani
from arayuz.dinamik_ekran import DinamikSorguEkrani
from arayuz.ceza_ekrani import CezaEkrani

class AnaMenu:
    def __init__(self):
        self.root = tk.Tk()  
        
        self.root.title(f"Yönetim Paneli - {Oturum.mevcut_kullanici}")
        self.root.geometry("850x700")
        self.root.protocol("WM_DELETE_WINDOW", self.cikis_yap)
        self.arayuz_olustur()
        self.root.mainloop()

    def arayuz_olustur(self):
        # ÜST BAŞLIK
        header = tk.Frame(self.root, bg="#34495e", height=80)
        header.pack(fill="x")
        
        lbl_baslik = tk.Label(header, text="KÜTÜPHANE YÖNETİM SİSTEMİ", font=("Segoe UI", 16, "bold"), bg="#34495e", fg="white")
        lbl_baslik.pack(side="left", padx=20, pady=20)
        
        tk.Button(header, text="Çıkış Yap", bg="#c0392b", fg="white", font=("Arial", 10, "bold"), 
                  relief="flat", command=self.cikis_yap).pack(side="right", padx=20)

        # KULLANICI BİLGİSİ
        tk.Label(self.root, text=f"Aktif Kullanıcı: {Oturum.mevcut_kullanici} ({Oturum.mevcut_rol})", font=("Arial", 12)).pack(pady=20)

        # MENÜ BUTONLARI
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady=10)

        # Üye ve Kitap
        self.btn_olustur(grid_frame, "👥 ÜYE YÖNETİMİ", "#1abc9c", 0, 0, lambda: UyeEkrani())
        self.btn_olustur(grid_frame, "📚 KİTAP YÖNETİMİ", "#3498db", 0, 1, lambda: KitapEkrani())
        
        # Ödünç ve Raporlar
        self.btn_olustur(grid_frame, "🔄 ÖDÜNÇ / İADE", "#9b59b6", 1, 0, lambda: OduncEkrani())
        self.btn_olustur(grid_frame, "📊 RAPORLAR", "#f1c40f", 1, 1, lambda: RaporEkrani())

        # Ceza ve Dinamik Sorgu
        self.btn_olustur(grid_frame, "💰 CEZA TAKİP", "#e74c3c", 2, 0, lambda: CezaEkrani())
        
        # DİNAMİK SORGU BUTONU
        self.btn_olustur(grid_frame, "💻 SQL / DİNAMİK SORGU", "#34495e", 2, 1, self.kontrol_ve_ac)

    def btn_olustur(self, parent, text, color, r, c, komut):
        tk.Button(parent, text=text, bg=color, fg="white", font=("Segoe UI", 11, "bold"),
                  width=22, height=5, cursor="hand2", command=komut).grid(row=r, column=c, padx=20, pady=20)

    def kontrol_ve_ac(self):
        # Yetki kontrolü (Boşlukları sil, küçük harfe çevir)
        gelen_rol = str(Oturum.mevcut_rol).strip().lower()

        # "yonet", "netici" veya "admin" geçiyorsa izin ver
        if "yonet" in gelen_rol or "netici" in gelen_rol or "admin" in gelen_rol:
            DinamikSorguEkrani()
        else:
            messagebox.showerror("Yetki Hatası", f"Bu alana sadece Yöneticiler girebilir!\n(Rolünüz: {Oturum.mevcut_rol})")

    def cikis_yap(self):
        self.root.destroy()
        # Uygulamayı tamamen kapatmak için
        import sys
        sys.exit()