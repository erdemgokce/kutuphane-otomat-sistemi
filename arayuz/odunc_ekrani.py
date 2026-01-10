import tkinter as tk
from tkinter import ttk, messagebox
from veritabani.yonetici import VeritabaniYoneticisi

class OduncEkrani:
    def __init__(self):
        self.pencere = tk.Toplevel()
        self.pencere.title("Ödünç & İade İşlemleri")
        self.pencere.geometry("1100x700")
        self.db = VeritabaniYoneticisi()
        
        self.notebook = ttk.Notebook(self.pencere)
        self.tab_ver = tk.Frame(self.notebook, bg="white")
        self.tab_al = tk.Frame(self.notebook)
        
        self.notebook.add(self.tab_ver, text=" 📖 Kitap Ödünç Ver ")
        self.notebook.add(self.tab_al, text=" ↩️ Kitap İade Al ")
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.arayuz_ver()
        self.arayuz_al()

    def arayuz_ver(self):
        # --- SOL PANEL: GİRİŞ, BUTON VE [BONUS] BİLGİ EKRANI ---
        left_frame = tk.Frame(self.tab_ver, bg="white", padx=10, pady=10)
        left_frame.place(x=0, y=0, width=320, height=650) # Genişliği biraz artırdık
        
        tk.Label(left_frame, text="Seçilen Üye ID:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.ent_uye_id = tk.Entry(left_frame, font=("Arial", 12), bg="#ecf0f1")
        self.ent_uye_id.pack(fill="x", pady=5)
        
        tk.Label(left_frame, text="Seçilen Kitap ID:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.ent_kitap_id = tk.Entry(left_frame, font=("Arial", 12), bg="#ecf0f1")
        self.ent_kitap_id.pack(fill="x", pady=5)
        
        tk.Button(left_frame, text="ÖDÜNÇ VER", bg="#8e44ad", fg="white", font=("Arial", 12, "bold"),
                  command=self.odunc_ver_islem).pack(pady=20, fill="x", ipady=10)

        # Sol alta, seçilen kişinin elindeki kitapları gösteren mini tablo
        tk.Label(left_frame, text="--- Üyenin Üzerindeki Kitaplar ---", fg="#c0392b", font=("Arial", 9, "bold")).pack(pady=(20, 5))
        
        self.tree_uye_detay = ttk.Treeview(left_frame, columns=("kitap", "tarih"), show="headings", height=8)
        self.tree_uye_detay.heading("kitap", text="Kitap Adı")
        self.tree_uye_detay.column("kitap", width=120)
        self.tree_uye_detay.heading("tarih", text="Son Teslim")
        self.tree_uye_detay.column("tarih", width=80)
        self.tree_uye_detay.pack(fill="x")

        # --- SAĞ PANEL: LİSTELER (ÜYELER VE KİTAPLAR) ---
        right_frame = tk.Frame(self.tab_ver)
        right_frame.place(x=330, y=0, width=760, height=650)

        # Üst: Üyeler
        tk.Label(right_frame, text="Üye Seçimi", bg="#bdc3c7").pack(fill="x")
        self.tree_uyeler = ttk.Treeview(right_frame, columns=("id", "ad", "soyad"), show="headings", height=10)
        self.tree_uyeler.heading("id", text="ID"); self.tree_uyeler.column("id", width=50)
        self.tree_uyeler.heading("ad", text="Ad"); self.tree_uyeler.column("ad", width=100)
        self.tree_uyeler.heading("soyad", text="Soyad")
        self.tree_uyeler.pack(fill="both", expand=True)
        self.tree_uyeler.bind("<ButtonRelease-1>", self.uye_sec) # Seçim olayı

        # Alt: Kitaplar
        tk.Label(right_frame, text="Kitap Seçimi (Sadece Stokta Olanlar)", bg="#bdc3c7").pack(fill="x")
        self.tree_kitaplar = ttk.Treeview(right_frame, columns=("id", "ad", "stok"), show="headings", height=10)
        self.tree_kitaplar.heading("id", text="ID"); self.tree_kitaplar.column("id", width=50)
        self.tree_kitaplar.heading("ad", text="Kitap Adı")
        self.tree_kitaplar.heading("stok", text="Stok"); self.tree_kitaplar.column("stok", width=50)
        self.tree_kitaplar.pack(fill="both", expand=True)
        self.tree_kitaplar.bind("<ButtonRelease-1>", self.kitap_sec) 

        self.listeleri_guncelle()

    def listeleri_guncelle(self):
        # Üyeleri Doldur
        self.tree_uyeler.delete(*self.tree_uyeler.get_children())
        for u in self.db.uyeleri_getir():
            self.tree_uyeler.insert("", "end", values=(u[0], u[1], u[2]))
        
        # Stoktaki Kitapları Doldur
        conn = self.db.baglan()
        cursor = conn.cursor()
        cursor.execute("SELECT KitapID, KitapAdi, MevcutAdet FROM KITAP WHERE MevcutAdet > 0")
        self.tree_kitaplar.delete(*self.tree_kitaplar.get_children())
        for k in cursor.fetchall():
            self.tree_kitaplar.insert("", "end", values=k)
        conn.close()

    def uye_sec(self, event):
        sel = self.tree_uyeler.selection()
        if sel:
            val = self.tree_uyeler.item(sel)['values']
            uye_id = val[0]
            
            # 1. ID Kutusunu Doldur
            self.ent_uye_id.delete(0, tk.END)
            self.ent_uye_id.insert(0, uye_id)
            
            # --- [BONUS] ---
            # 2. Seçili üyenin üzerindeki kitapları getirir ve sol alttaki tabloya basar
            self.tree_uye_detay.delete(*self.tree_uye_detay.get_children()) # Temizle
            aktif_kitaplar = self.db.uye_aktif_kitaplarini_getir(uye_id)
            for kitap in aktif_kitaplar:
                self.tree_uye_detay.insert("", "end", values=kitap)

    def kitap_sec(self, event):
        sel = self.tree_kitaplar.selection()
        if sel:
            val = self.tree_kitaplar.item(sel)['values']
            self.ent_kitap_id.delete(0, tk.END)
            self.ent_kitap_id.insert(0, val[0])

    def arayuz_al(self):
        # İade Alma Sekmesi Tasarımı
        top_frame = tk.Frame(self.tab_al)
        top_frame.pack(fill="x", pady=5)
        
        tk.Button(top_frame, text="SEÇİLİ KİTABI TESLİM AL", bg="#d35400", fg="white", 
                  command=self.iade_al_islem).pack(side="right", padx=10)
        
        cols = ("ID", "Üye", "Kitap", "Veriliş", "Son Teslim")
        self.tree_odunc = ttk.Treeview(self.tab_al, columns=cols, show="headings")
        for col in cols: self.tree_odunc.heading(col, text=col)
        self.tree_odunc.pack(fill="both", expand=True)
        
        self.listele_aktif_odunc()

    def listele_aktif_odunc(self):
        self.tree_odunc.delete(*self.tree_odunc.get_children())
        veriler = self.db.aktif_odunclari_getir()
        for v in veriler:
            self.tree_odunc.insert("", "end", values=v)

    def odunc_ver_islem(self):
        try:
            self.db.odunc_ver(self.ent_uye_id.get(), self.ent_kitap_id.get())
            messagebox.showinfo("Başarılı", "Kitap ödünç verildi.")
            self.ent_uye_id.delete(0, tk.END)
            self.ent_kitap_id.delete(0, tk.END)
            self.tree_uye_detay.delete(*self.tree_uye_detay.get_children()) # Bonus tabloyu temizle
            self.listele_aktif_odunc()
            self.listeleri_guncelle() 
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def iade_al_islem(self):
        secili = self.tree_odunc.selection()
        if not secili: return
        oid = self.tree_odunc.item(secili)['values'][0]
        
        if messagebox.askyesno("Onay", "Kitap iade alınıyor mu?"):
            try:
                self.db.iade_al(oid)
                messagebox.showinfo("Başarılı", "İade işlemi tamamlandı.")
                self.listele_aktif_odunc()
                self.listeleri_guncelle() 
            except Exception as e:
                messagebox.showerror("Hata", str(e))