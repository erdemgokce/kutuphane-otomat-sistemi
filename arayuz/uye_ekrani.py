import tkinter as tk
from tkinter import ttk, messagebox
from veritabani.yonetici import VeritabaniYoneticisi

class UyeEkrani:
    def __init__(self):
        self.pencere = tk.Toplevel()
        self.pencere.title("Üye Yönetimi")
        self.pencere.geometry("1000x650")
        
        self.db = VeritabaniYoneticisi()
        self.arayuz_olustur()
        self.listele()

    def arayuz_olustur(self):
        # --- ÜST PANEL: Üye Ekleme / Güncelleme ---
        frame_ust = tk.LabelFrame(self.pencere, text=" Üye Bilgileri ", padx=10, pady=10, bg="#f8f9fa")
        frame_ust.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_ust, text="Ad:", bg="#f8f9fa").grid(row=0, column=0, padx=5)
        self.ent_ad = tk.Entry(frame_ust); self.ent_ad.grid(row=0, column=1, padx=5)

        tk.Label(frame_ust, text="Soyad:", bg="#f8f9fa").grid(row=0, column=2, padx=5)
        self.ent_soyad = tk.Entry(frame_ust); self.ent_soyad.grid(row=0, column=3, padx=5)

        tk.Label(frame_ust, text="Telefon:", bg="#f8f9fa").grid(row=1, column=0, padx=5, pady=5)
        self.ent_tel = tk.Entry(frame_ust); self.ent_tel.grid(row=1, column=1, padx=5)

        tk.Label(frame_ust, text="E-posta:", bg="#f8f9fa").grid(row=1, column=2, padx=5)
        self.ent_mail = tk.Entry(frame_ust); self.ent_mail.grid(row=1, column=3, padx=5)

        btn_frame = tk.Frame(frame_ust, bg="#f8f9fa")
        btn_frame.grid(row=0, column=4, rowspan=2, padx=20)

        tk.Button(btn_frame, text="YENİ ÜYE EKLE", bg="#27ae60", fg="white", font=("bold"), 
                  command=self.ekle, width=15).pack(pady=2)
        tk.Button(btn_frame, text="BİLGİ GÜNCELLE", bg="#2980b9", fg="white", font=("bold"), 
                  command=self.guncelle, width=15).pack(pady=2)

        # --- ORTA PANEL: Liste ve Arama ---
        frame_ara = tk.Frame(self.pencere)
        frame_ara.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_ara, text="Üye Ara (Ad/Soyad):").pack(side="left")
        self.ent_ara = tk.Entry(frame_ara)
        self.ent_ara.pack(side="left", padx=5)
        tk.Button(frame_ara, text="ARA", command=self.listele).pack(side="left")

        # Tablo
        cols = ("id", "ad", "soyad", "tel", "mail", "borc")
        self.tree = ttk.Treeview(self.pencere, columns=cols, show="headings")
        
        self.tree.heading("id", text="ID"); self.tree.column("id", width=40)
        self.tree.heading("ad", text="Ad"); self.tree.column("ad", width=120)
        self.tree.heading("soyad", text="Soyad"); self.tree.column("soyad", width=120)
        self.tree.heading("tel", text="Telefon"); self.tree.column("tel", width=100)
        self.tree.heading("mail", text="E-Posta"); self.tree.column("mail", width=150)
        self.tree.heading("borc", text="Toplam Borç"); self.tree.column("borc", width=100)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<ButtonRelease-1>", self.alanlari_doldur)

        # --- ALT PANEL: Silme ---
        tk.Button(self.pencere, text="SEÇİLİ ÜYEYİ SİSTEMDEN SİL", bg="#c0392b", fg="white", 
                  font=("Arial", 10, "bold"), pady=10, command=self.sil).pack(fill="x", padx=10, pady=10)

    def listele(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        arama = self.ent_ara.get()
        for u in self.db.uyeleri_getir(arama):
            self.tree.insert("", "end", values=u)

    def alanlari_doldur(self, event):
        secili = self.tree.selection()
        if not secili: return
        val = self.tree.item(secili[0])['values']
        self.ent_ad.delete(0, tk.END); self.ent_ad.insert(0, val[1])
        self.ent_soyad.delete(0, tk.END); self.ent_soyad.insert(0, val[2])
        self.ent_tel.delete(0, tk.END); self.ent_tel.insert(0, val[3])
        self.ent_mail.delete(0, tk.END); self.ent_mail.insert(0, val[4])

    def ekle(self):
        try:
            self.db.uye_ekle(self.ent_ad.get(), self.ent_soyad.get(), self.ent_tel.get(), self.ent_mail.get())
            messagebox.showinfo("Başarılı", "Üye kaydı oluşturuldu.")
            self.listele()
        except Exception as e: messagebox.showerror("Hata", str(e))

    def guncelle(self):
        secili = self.tree.selection()
        if not secili: return
        uye_id = self.tree.item(secili[0])['values'][0]
        try:
            self.db.uye_guncelle(uye_id, self.ent_ad.get(), self.ent_soyad.get(), self.ent_tel.get(), self.ent_mail.get())
            messagebox.showinfo("Başarılı", "Üye bilgileri güncellendi.")
            self.listele()
        except Exception as e: messagebox.showerror("Hata", str(e))

    def sil(self):
        secili = self.tree.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen silinecek üyeyi seçin.")
            return
        
        uye_id = self.tree.item(secili[0])['values'][0]
        borc = self.tree.item(secili[0])['values'][5]
        
        # 1. Kontrol: Aktif Ödünç Kitap Var mı?
        aktif_kitaplar = self.db.uye_aktif_kitaplarini_getir(uye_id)
        
        if len(aktif_kitaplar) > 0:
            messagebox.showerror("Hata", f"Üyenin iade etmediği {len(aktif_kitaplar)} adet kitap bulunmaktadır. Kitaplar iade edilmeden üye silinemez!")
            return

        # 2. Kontrol: Toplam Borç Var mı?
        if float(borc) > 0:
            messagebox.showerror("Hata", f"Üyenin {borc} TL borcu bulunmaktadır. Borç ödenmeden üye silinemez!")
            return

        # Şartlar uygunsa silme onayı iste
        if messagebox.askyesno("Onay", "Üye kaydı silinecek. Emin misiniz? Bakiyesiz ve kitapsız üye siliniyor."):
            try:
                self.db.uye_sil(uye_id)
                messagebox.showinfo("Başarılı", "Üye başarıyla silindi.")
                self.listele()
            except Exception as e:
                # Trigger'dan dönen hatayı yakalar
                messagebox.showerror("Veritabanı Engeli", str(e))