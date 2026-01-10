import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from veritabani.yonetici import VeritabaniYoneticisi

class DinamikSorguEkrani:
    def __init__(self):
        self.pencere = tk.Toplevel()
        self.pencere.title("Gelişmiş Kitap Arama (Dinamik SQL)")
        self.pencere.geometry("1000x750")
        self.db = VeritabaniYoneticisi()
        self.arayuz_olustur()

    def arayuz_olustur(self):
        filter_frame = tk.LabelFrame(self.pencere, text=" Filtreler & Sıralama ", padx=10, pady=10)
        filter_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Metin Filtreleri
        tk.Label(filter_frame, text="Kitap Adı:").pack(anchor="w")
        self.ent_adi = tk.Entry(filter_frame); self.ent_adi.pack(fill="x")

        tk.Label(filter_frame, text="Yazar:").pack(anchor="w")
        self.ent_yazar = tk.Entry(filter_frame); self.ent_yazar.pack(fill="x")

        # Kategori (Combobox)
        tk.Label(filter_frame, text="Kategori:").pack(anchor="w")
        self.cmb_kat = ttk.Combobox(filter_frame, values=["Roman", "Bilim", "Tarih", "Yazılım", "Edebiyat"])
        self.cmb_kat.pack(fill="x")

        # Yıl Aralığı (Min - Max)
        tk.Label(filter_frame, text="Yıl Aralığı (Min - Max):").pack(anchor="w", pady=(10, 0))
        yil_frame = tk.Frame(filter_frame)
        yil_frame.pack(fill="x")
        self.ent_yil_min = tk.Entry(yil_frame, width=10); self.ent_yil_min.pack(side="left", padx=2)
        self.ent_yil_max = tk.Entry(yil_frame, width=10); self.ent_yil_max.pack(side="left", padx=2)

        # Stok Durumu (Checkbox)
        self.var_mevcut = tk.BooleanVar()
        tk.Checkbutton(filter_frame, text="Sadece Stokta Olanlar", variable=self.var_mevcut).pack(anchor="w", pady=10)

        # Sıralama Seçenekleri
        tk.Label(filter_frame, text="--- Sıralama ---", fg="blue").pack(pady=(15, 5))
        
        tk.Label(filter_frame, text="Sıralama Sütunu:").pack(anchor="w")
        self.cmb_sort_col = ttk.Combobox(filter_frame, values=["KitapAdi", "Yazar", "BasimYili", "MevcutAdet"])
        self.cmb_sort_col.current(0) 
        self.cmb_sort_col.pack(fill="x")

        tk.Label(filter_frame, text="Yön:").pack(anchor="w")
        self.cmb_sort_dir = ttk.Combobox(filter_frame, values=["Artan (ASC)", "Azalan (DESC)"])
        self.cmb_sort_dir.current(0)
        self.cmb_sort_dir.pack(fill="x")

        # Butonlar
        tk.Button(filter_frame, text="DİNAMİK ARA", bg="#3498db", fg="white", 
                  command=self.dinamik_ara).pack(fill="x", ipady=5, pady=20)
        
        tk.Button(filter_frame, text="EXCEL İNDİR", bg="#27ae60", fg="white", 
                  command=self.excel_indir).pack(fill="x", pady=5)

        self.tree = ttk.Treeview(self.pencere, show="headings")
        self.tree.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def sorgu_hazirla(self):
        # TEKNİK: "WHERE 1=1" sayesinde her koşulun başına "AND" ekleyebiliyoruz.
        query = "SELECT * FROM KITAP WHERE 1=1"
        params = []

        # Kitap Adı (LIKE)
        if self.ent_adi.get().strip():
            query += " AND KitapAdi LIKE %s"
            params.append(f"%{self.ent_adi.get().strip()}%")

        # Yazar (LIKE)
        if self.ent_yazar.get().strip():
            query += " AND Yazar LIKE %s"
            params.append(f"%{self.ent_yazar.get().strip()}%")

        # Kategori (EŞİTTİR)
        if self.cmb_kat.get():
            query += " AND Kategori = %s"
            params.append(self.cmb_kat.get())

        # Yıl Aralığı (BÜYÜKTÜR / KÜÇÜKTÜR)
        if self.ent_yil_min.get().strip():
            query += " AND BasimYili >= %s"
            params.append(self.ent_yil_min.get().strip())
        
        if self.ent_yil_max.get().strip():
            query += " AND BasimYili <= %s"
            params.append(self.ent_yil_max.get().strip())

        # Checkbox (BOOLEAN MANTIK)
        if self.var_mevcut.get():
            query += " AND MevcutAdet > 0"

        # Sıralama (ORDER BY)
        col_map = {"KitapAdi": "KitapAdi", "Yazar": "Yazar", "BasimYili": "BasimYili", "MevcutAdet": "MevcutAdet"}
        dir_map = {"Artan (ASC)": "ASC", "Azalan (DESC)": "DESC"}
        
        secilen_kolon = col_map.get(self.cmb_sort_col.get(), "KitapAdi")
        secilen_yon = dir_map.get(self.cmb_sort_dir.get(), "ASC")
        
        query += f" ORDER BY {secilen_kolon} {secilen_yon}"

        return query, params

    def dinamik_ara(self):
        query, params = self.sorgu_hazirla()
        try:
            conn = self.db.baglan()
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Dinamik Kolon Başlıkları
            if cursor.description:
                col_names = [i[0] for i in cursor.description]
            else:
                col_names = []
            
            conn.close()

            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = col_names
            for c in col_names: self.tree.heading(c, text=c)
            for r in rows: self.tree.insert("", "end", values=r)
            
        except Exception as e: messagebox.showerror("Hata", str(e))

    def excel_indir(self):
        query, params = self.sorgu_hazirla()
        try:
            conn = self.db.baglan()
            df = pd.read_sql(query, conn, params=params)
            conn.close()
            
            if df.empty:
                messagebox.showwarning("Uyarı", "Kriterlere uygun veri bulunamadı.")
                return

            dosya = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if dosya:
                df.to_excel(dosya, index=False)
                messagebox.showinfo("Başarılı", "Excel dosyası oluşturuldu.")
        except Exception as e: messagebox.showerror("Hata", str(e))