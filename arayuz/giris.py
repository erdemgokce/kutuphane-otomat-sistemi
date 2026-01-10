import tkinter as tk
from tkinter import messagebox
from config import Oturum
from veritabani.yonetici import VeritabaniYoneticisi
from arayuz.ana_menu import AnaMenu

class GirisEkrani:
    def __init__(self):
        self.pencere = tk.Tk()
        self.pencere.title("Kütüphane Sistemi - Giriş")
        self.pencere.geometry("350x450")
        self.pencere.configure(bg="#2c3e50")
        self.db = VeritabaniYoneticisi()
        self.arayuz_olustur()

    def arayuz_olustur(self):
        tk.Label(self.pencere, text="KÜTÜPHANE", font=("Segoe UI", 20, "bold"), bg="#2c3e50", fg="#3498db").pack(pady=(50, 10))
        
        frm = tk.Frame(self.pencere, bg="#2c3e50")
        frm.pack(pady=20)

        tk.Label(frm, text="Kullanıcı Adı", bg="#2c3e50", fg="white").pack(anchor="w")
        self.ent_kadi = tk.Entry(frm, font=("Arial", 12))
        self.ent_kadi.pack(pady=5, fill="x")

        tk.Label(frm, text="Şifre", bg="#2c3e50", fg="white").pack(anchor="w")
        self.ent_sifre = tk.Entry(frm, font=("Arial", 12), show="*")
        self.ent_sifre.pack(pady=5, fill="x")

        tk.Button(self.pencere, text="GİRİŞ YAP", bg="#3498db", fg="white", font=("Segoe UI", 12, "bold"),
                  relief="flat", command=self.giris_yap).pack(pady=30, padx=40, fill="x")

    def giris_yap(self):
        kadi = self.ent_kadi.get()
        sifre = self.ent_sifre.get()
        try:
            user = self.db.giris_kontrol(kadi, sifre)
            if user:
                Oturum.oturum_ac(user[1], user[3]) # Kullanıcı adı ve Rol
                self.pencere.destroy()
                app = AnaMenu() # Ana menüyü başlat
            else:
                messagebox.showerror("Hata", "Hatalı bilgi!")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def baslat(self):
        self.pencere.mainloop()