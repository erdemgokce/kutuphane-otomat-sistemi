import tkinter as tk
from tkinter import ttk, messagebox
from veritabani.yonetici import VeritabaniYoneticisi
from datetime import date, timedelta

class RaporEkrani:
    def __init__(self):
        self.pencere = tk.Toplevel()
        self.pencere.title("Gelişmiş Raporlama Merkezi")
        self.pencere.geometry("1000x700")
        
        # Backend bağlantısı
        self.db = VeritabaniYoneticisi()
        
        # Sekmeli Yapı
        self.notebook = ttk.Notebook(self.pencere)
        self.tab1 = tk.Frame(self.notebook, bg="#f4f7f6")
        self.tab2 = tk.Frame(self.notebook, bg="#f4f7f6")
        self.tab3 = tk.Frame(self.notebook, bg="#f4f7f6")
        
        self.notebook.add(self.tab1, text=" 📅 Tarih Aralığı Raporu ")
        self.notebook.add(self.tab2, text=" ⚠️ Geciken Kitaplar ")
        self.notebook.add(self.tab3, text=" 🏆 En Popüler Kitaplar ")
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.kur_tab1()
        self.kur_tab2()
        self.kur_tab3()

    # --- TAB 1 ---
    def kur_tab1(self):
        frm = tk.LabelFrame(self.tab1, text=" Parametreler ", padx=10, pady=10, bg="white")
        frm.pack(fill="x", padx=10, pady=10)
        
        bugun = date.today()
        gecen_ay = bugun - timedelta(days=30)

        tk.Label(frm, text="Başlangıç (YYYY-MM-DD):", bg="white").grid(row=0, column=0, padx=5)
        self.ent_t1_bas = tk.Entry(frm); self.ent_t1_bas.grid(row=0, column=1, padx=5)
        self.ent_t1_bas.insert(0, str(gecen_ay))

        tk.Label(frm, text="Bitiş:", bg="white").grid(row=0, column=2, padx=5)
        self.ent_t1_bit = tk.Entry(frm); self.ent_t1_bit.grid(row=0, column=3, padx=5)
        self.ent_t1_bit.insert(0, str(bugun))

        tk.Label(frm, text="Üye Adı:", bg="white").grid(row=1, column=0, padx=5, pady=10)
        self.ent_t1_uye = tk.Entry(frm); self.ent_t1_uye.grid(row=1, column=1, padx=5)

        tk.Label(frm, text="Kategori:", bg="white").grid(row=1, column=2, padx=5)
        self.cmb_t1_kat = ttk.Combobox(frm, values=["", "Roman", "Bilim", "Tarih", "Yazılım", "Edebiyat"])
        self.cmb_t1_kat.grid(row=1, column=3, padx=5)

        tk.Button(frm, text="RAPORLA", bg="#3498db", fg="white", font=("bold"), 
                  command=self.calistir_tab1).grid(row=0, column=4, rowspan=2, padx=20, ipadx=10, ipady=10)

        cols = ("Üye", "Kitap", "Veriliş Tarihi", "Teslim Tarihi", "Durum")
        self.tree1 = ttk.Treeview(self.tab1, columns=cols, show="headings")
        for c in cols: self.tree1.heading(c, text=c)
        self.tree1.pack(fill="both", expand=True, padx=10, pady=10)

    def calistir_tab1(self):
        try:
            # Backend'deki fonksiyonu çağırıyoruz
            veriler = self.db.rapor_tarih_araligi(
                self.ent_t1_bas.get(), self.ent_t1_bit.get(),
                self.ent_t1_uye.get(), self.cmb_t1_kat.get()
            )
            self.tree1.delete(*self.tree1.get_children())
            for v in veriler: self.tree1.insert("", "end", values=v)
        except Exception as e: messagebox.showerror("Hata", str(e))

    # --- TAB 2 ---
    def kur_tab2(self):
        frm = tk.Frame(self.tab2, pady=10, bg="#f4f7f6")
        frm.pack(fill="x")
        
        tk.Button(frm, text="GECİKENLERİ LİSTELE", bg="#c0392b", fg="white", font=("bold"),
                  command=self.calistir_tab2).pack(side="right", padx=20)

        cols = ("Üye", "Kitap", "Veriliş", "Son Teslim", "Gecikme (Gün)")
        self.tree2 = ttk.Treeview(self.tab2, columns=cols, show="headings")
        for c in cols: self.tree2.heading(c, text=c)
        self.tree2.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.calistir_tab2()

    def calistir_tab2(self):
        try:
            veriler = self.db.rapor_gecikenler_detayli()
            self.tree2.delete(*self.tree2.get_children())
            for v in veriler: self.tree2.insert("", "end", values=v)
        except Exception as e: messagebox.showerror("Hata", str(e))

    # --- TAB 3 ---
    def kur_tab3(self):
        frm = tk.LabelFrame(self.tab3, text=" Tarih Aralığı ", padx=10, pady=10, bg="white")
        frm.pack(fill="x", padx=10, pady=10)

        bugun = date.today()
        yil_basi = date(bugun.year, 1, 1)

        tk.Label(frm, text="Başlangıç:", bg="white").pack(side="left", padx=5)
        self.ent_t3_bas = tk.Entry(frm); self.ent_t3_bas.pack(side="left", padx=5)
        self.ent_t3_bas.insert(0, str(yil_basi))

        tk.Label(frm, text="Bitiş:", bg="white").pack(side="left", padx=5)
        self.ent_t3_bit = tk.Entry(frm); self.ent_t3_bit.pack(side="left", padx=5)
        self.ent_t3_bit.insert(0, str(bugun))

        tk.Button(frm, text="ANALİZ ET", bg="#f39c12", fg="white", font=("bold"),
                  command=self.calistir_tab3).pack(side="left", padx=20)

        cols = ("Kitap Adı", "Yazar", "Kategori", "Ödünç Sayısı")
        self.tree3 = ttk.Treeview(self.tab3, columns=cols, show="headings")
        for c in cols: self.tree3.heading(c, text=c)
        self.tree3.pack(fill="both", expand=True, padx=10, pady=10)

    def calistir_tab3(self):
        try:
            veriler = self.db.rapor_populer_kitaplar(self.ent_t3_bas.get(), self.ent_t3_bit.get())
            self.tree3.delete(*self.tree3.get_children())
            for v in veriler: self.tree3.insert("", "end", values=v)
        except Exception as e: messagebox.showerror("Hata", str(e))