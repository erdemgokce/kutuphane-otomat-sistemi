import tkinter as tk
from tkinter import ttk, messagebox
from veritabani.yonetici import VeritabaniYoneticisi

class KitapEkrani:
    def __init__(self):
        self.pencere = tk.Toplevel()
        self.pencere.title("Kitap Yönetimi")
        self.pencere.geometry("1000x700")
        self.db = VeritabaniYoneticisi()
        
        self.arayuz_olustur()
        self.listele()

    def arayuz_olustur(self):
        # --- GİRİŞ PANELİ (Ekleme & Güncelleme) ---
        input_frame = tk.LabelFrame(self.pencere, text=" Kitap Bilgileri ", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        fields = [("Kitap Adı:", "ent_ad"), ("Yazar:", "ent_yazar"), ("Yayınevi:", "ent_yayin"), 
                  ("Basım Yılı:", "ent_yil"), ("Toplam Adet:", "ent_adet")]
        
        self.inputs = {}
        for i, (label, attr) in enumerate(fields):
            tk.Label(input_frame, text=label).grid(row=i//3, column=(i%3)*2, sticky="e", pady=5)
            entry = tk.Entry(input_frame)
            entry.grid(row=i//3, column=(i%3)*2+1, padx=5, pady=5)
            self.inputs[attr] = entry

        tk.Label(input_frame, text="Kategori:").grid(row=1, column=4, sticky="e")
        self.cmb_kat = ttk.Combobox(input_frame, values=["Roman", "Bilim", "Tarih", "Yazılım", "Edebiyat", "Felsefe"])
        self.cmb_kat.grid(row=1, column=5, padx=5)

        # Butonlar
        btn_frame = tk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, columnspan=6, pady=10)

        tk.Button(btn_frame, text="✨ YENİ EKLE", bg="#27ae60", fg="white", width=15, command=self.ekle).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🔄 GÜNCELLE", bg="#2980b9", fg="white", width=15, command=self.guncelle).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🧹 TEMİZLE", command=self.temizle).pack(side="left", padx=5)

        # --- ARAMA PANELİ ---
        search_frame = tk.Frame(self.pencere)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(search_frame, text="Hızlı Ara (Kitap/Yazar):").pack(side="left")
        self.ent_ara = tk.Entry(search_frame)
        self.ent_ara.pack(side="left", padx=5)
        tk.Button(search_frame, text="🔍 ARA", command=self.listele).pack(side="left")

        # --- TABLO ---
        cols = ("id", "ad", "yazar", "kat", "yayin", "yil", "toplam", "mevcut")
        self.tree = ttk.Treeview(self.pencere, columns=cols, show="headings")
        
        headers = ["ID", "Kitap Adı", "Yazar", "Kategori", "Yayınevi", "Yıl", "T.Adet", "M.Adet"]
        for i, col in enumerate(cols):
            self.tree.heading(col, text=headers[i])
            self.tree.column(col, width=100 if i!=0 else 40)
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.alanlari_doldur)

        # --- SİLME BUTONU ---
        tk.Button(self.pencere, text="🗑️ SEÇİLİ KİTABI SİL", bg="#c0392b", fg="white", 
                  font=("bold"), command=self.sil).pack(fill="x", padx=10, pady=10)

    def alanlari_doldur(self, event):
        sel = self.tree.selection()
        if not sel: return
        val = self.tree.item(sel[0])['values']
        
        # Giriş kutularını seçilen satırla doldur
        self.temizle()
        self.inputs["ent_ad"].insert(0, val[1])
        self.inputs["ent_yazar"].insert(0, val[2])
        self.cmb_kat.set(val[3])
        self.inputs["ent_yayin"].insert(0, val[4])
        self.inputs["ent_yil"].insert(0, val[5])
        self.inputs["ent_adet"].insert(0, val[6])

    def listele(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for k in self.db.kitaplari_getir(self.ent_ara.get()):
            self.tree.insert("", "end", values=k)

    def ekle(self):
        data = {k: v.get() for k, v in self.inputs.items()}
        if not data["ent_ad"] or not data["ent_adet"]:
            messagebox.showwarning("Uyarı", "Kitap adı ve adet zorunludur!")
            return
        
        try:
            self.db.kitap_ekle(data["ent_ad"], data["ent_yazar"], self.cmb_kat.get(),
                               data["ent_yayin"], data["ent_yil"], data["ent_adet"])
            messagebox.showinfo("Başarılı", "Kitap eklendi. Mevcut adet toplam adete eşitlendi.")
            self.listele(); self.temizle()
        except Exception as e: messagebox.showerror("Hata", str(e))

    def guncelle(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Uyarı", "Lütfen güncellenecek kitabı seçin!")
            return
        
        kitap_id = self.tree.item(sel[0])['values'][0]
        data = {k: v.get() for k, v in self.inputs.items()}
        
        try:
            self.db.kitap_guncelle(kitap_id, data["ent_ad"], data["ent_yazar"], self.cmb_kat.get(),
                                   data["ent_yayin"], data["ent_yil"], data["ent_adet"])
            messagebox.showinfo("Başarılı", "Kitap bilgileri güncellendi.")
            self.listele()
        except Exception as e: messagebox.showerror("Hata", str(e))

    def sil(self):
        sel = self.tree.selection()
        if not sel: return
        
        kitap_id = self.tree.item(sel[0])['values'][0]
        kitap_adi = self.tree.item(sel[0])['values'][1]

        if self.db.kitap_oduncte_mi(kitap_id):
            messagebox.showerror("Hata", f"'{kitap_adi}' şu an bir üyede ödünç olarak görünüyor. İade edilmeden silinemez!")
            return

        if messagebox.askyesno("Onay", f"'{kitap_adi}' kalıcı olarak silinecek. Emin misiniz?"):
            try:
                self.db.kitap_sil(kitap_id)
                messagebox.showinfo("Başarılı", "Kitap silindi.")
                self.listele()
            except Exception as e: messagebox.showerror("Hata", str(e))

    def temizle(self):
        for e in self.inputs.values(): e.delete(0, tk.END)
        self.cmb_kat.set("")