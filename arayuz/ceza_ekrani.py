import tkinter as tk
from tkinter import ttk, messagebox
from veritabani.yonetici import VeritabaniYoneticisi

class CezaEkrani:
    def __init__(self):
        self.pencere = tk.Toplevel()
        self.pencere.title("Ceza Takip Sistemi")
        self.pencere.geometry("900x600")
        self.db = VeritabaniYoneticisi()
        self.arayuz_olustur()

    def arayuz_olustur(self):
        # Filtre Paneli
        filter_frame = tk.LabelFrame(self.pencere, text="Filtreleme", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(filter_frame, text="Üye Adı:").pack(side="left")
        self.ent_uye = tk.Entry(filter_frame); self.ent_uye.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Başlangıç (YYYY-MM-DD):").pack(side="left")
        self.ent_bas = tk.Entry(filter_frame); self.ent_bas.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Bitiş:").pack(side="left")
        self.ent_bit = tk.Entry(filter_frame); self.ent_bit.pack(side="left", padx=5)

        tk.Button(filter_frame, text="FİLTRELE", bg="#e74c3c", fg="white", command=self.filtrele).pack(side="left", padx=20)

        # Liste
        self.tree = ttk.Treeview(self.pencere, columns=("id", "uye", "kitap", "gun", "tutar"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("uye", text="Üye")
        self.tree.heading("kitap", text="Kitap")
        self.tree.heading("gun", text="Gecikme (Gün)")
        self.tree.heading("tutar", text="Ceza Tutarı (TL)")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Toplam Borç Alanı
        self.lbl_toplam = tk.Label(self.pencere, text="Listelenen Toplam Ceza: 0.00 TL", font=("Arial", 14, "bold"), fg="#c0392b")
        self.lbl_toplam.pack(pady=10)

        self.filtrele() # İlk açılışta hepsini getir

    def filtrele(self):
        veriler = self.db.cezalari_getir(self.ent_uye.get(), self.ent_bas.get(), self.ent_bit.get())
        
        self.tree.delete(*self.tree.get_children())
        toplam = 0.0
        for v in veriler:
            self.tree.insert("", "end", values=v)
            if v[4]: # Tutar sütunu
                toplam += float(v[4])
        
        self.lbl_toplam.config(text=f"Listelenen Toplam Ceza: {toplam:.2f} TL")