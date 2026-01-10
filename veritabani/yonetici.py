import mysql.connector
from config import Ayarlar
from config import Oturum

class VeritabaniYoneticisi:
    def __init__(self):
        self.config = {
            "host": Ayarlar.DB_HOST,
            "user": Ayarlar.DB_USER,
            "password": Ayarlar.DB_PASS,
            "database": Ayarlar.DB_NAME
        }

    def baglan(self):
        return mysql.connector.connect(**self.config)

    # --- GİRİŞ ---
    def giris_kontrol(self, kadi, sifre):
        conn = self.baglan()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM KULLANICILAR WHERE KullaniciAdi=%s AND Sifre=%s", (kadi, sifre))
        user = cursor.fetchone()
        conn.close()
        return user

    # --- ÜYE İŞLEMLERİ ---
    def uyeleri_getir(self, arama=""):
        conn = self.baglan()
        cursor = conn.cursor()
        if arama:
            sql = "SELECT * FROM UYE WHERE Ad LIKE %s OR Soyad LIKE %s"
            cursor.execute(sql, (f'%{arama}%', f'%{arama}%'))
        else:
            cursor.execute("SELECT * FROM UYE")
        veriler = cursor.fetchall()
        conn.close()
        return veriler

    def uye_ekle(self, ad, soyad, tel, email):
        conn = self.baglan()
        cursor = conn.cursor()
        sql = "INSERT INTO UYE (Ad, Soyad, Telefon, Email) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (ad, soyad, tel, email))
        conn.commit()
        conn.close()

    def uye_sil(self, uye_id):
        conn = self.baglan()
        cursor = conn.cursor()
        # Eğer borcu varsa SQL hata fırlatacak
        cursor.execute("DELETE FROM UYE WHERE UyeID = %s", (uye_id,))
        conn.commit()
        conn.close()
        
    def uye_guncelle(self, uye_id, ad, soyad, tel, email):
        conn = self.baglan()
        cursor = conn.cursor()
        sql = "UPDATE UYE SET Ad=%s, Soyad=%s, Telefon=%s, Email=%s WHERE UyeID=%s"
        cursor.execute(sql, (ad, soyad, tel, email, uye_id))
        conn.commit()
        conn.close()

    # --- KİTAP İŞLEMLERİ
    def kitaplari_getir(self, arama=""):
        conn = self.baglan()
        cursor = conn.cursor()
        if arama:
            sql = "SELECT * FROM KITAP WHERE KitapAdi LIKE %s OR Yazar LIKE %s"
            cursor.execute(sql, (f'%{arama}%', f'%{arama}%'))
        else:
            cursor.execute("SELECT * FROM KITAP")
        veriler = cursor.fetchall()
        conn.close()
        return veriler

    def kitap_ekle(self, ad, yazar, kat, yayin, yil, adet):
        conn = self.baglan()
        cursor = conn.cursor()
        # Yeni kitap eklenirken MevcutAdet = ToplamAdet olur
        sql = """INSERT INTO KITAP (KitapAdi, Yazar, Kategori, Yayinevi, BasimYili, ToplamAdet, MevcutAdet) 
                 VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (ad, yazar, kat, yayin, yil, adet, adet))
        conn.commit()
        conn.close()

    def kitap_sil(self, kitap_id):
        conn = self.baglan()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM KITAP WHERE KitapID = %s", (kitap_id,))
        conn.commit()
        conn.close()

    # Kitap Silme Öncesi Kontrol: Aktif ödünç var mı?
    def kitap_oduncte_mi(self, kitap_id):
        conn = self.baglan()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM ODUNC WHERE KitapID = %s AND TeslimTarihi IS NULL"
        cursor.execute(sql, (kitap_id,))
        sayi = cursor.fetchone()[0]
        conn.close()
        return sayi > 0

    # Kitap Güncelleme (Hocanın istediği kategori, stok vb. alanlar dahil)
    def kitap_guncelle(self, kitap_id, ad, yazar, kat, yayin, yil, toplam_adet):
        conn = self.baglan()
        cursor = conn.cursor()
        # Not: Toplam adet değişirse mevcut adeti de orantılı güncellemek gerekir 
        # ama en basit haliyle toplam adeti güncelliyoruz.
        sql = """UPDATE KITAP SET KitapAdi=%s, Yazar=%s, Kategori=%s, Yayinevi=%s, 
                 BasimYili=%s, ToplamAdet=%s WHERE KitapID=%s"""
        cursor.execute(sql, (ad, yazar, kat, yayin, yil, toplam_adet, kitap_id))
        conn.commit()
        conn.close()
    # --- ÖDÜNÇ & İADE (GÜNCELLENMİŞ VERSİYON) ---
    def odunc_ver(self, uye_id, kitap_id):
        conn = self.baglan()
        cursor = conn.cursor()
        
        # 1. Personel ID Bulma
        kadi = Oturum.mevcut_kullanici
        try:
            cursor.execute("SELECT KullaniciID FROM KULLANICILAR WHERE KullaniciAdi = %s", (kadi,))
            res = cursor.fetchone()
            personel_id = res[0] if res else 1
        except:
            personel_id = 1
            
        # 2. SP Çağırma
        cursor.callproc('sp_YeniOduncVer', (uye_id, kitap_id, personel_id))
        conn.commit()
        conn.close()

    def iade_al(self, odunc_id):
        conn = self.baglan()
        cursor = conn.cursor()
        cursor.callproc('sp_KitapTeslimAl', (odunc_id,))
        conn.commit()
        conn.close()

    def aktif_odunclari_getir(self):
        conn = self.baglan()
        cursor = conn.cursor()
        sql = """SELECT O.OduncID, CONCAT(U.Ad, ' ', U.Soyad), K.KitapAdi, O.OduncTarihi, O.SonTeslimTarihi
                 FROM ODUNC O JOIN UYE U ON O.UyeID = U.UyeID JOIN KITAP K ON O.KitapID = K.KitapID
                 WHERE O.TeslimTarihi IS NULL"""
        cursor.execute(sql)
        veriler = cursor.fetchall()
        conn.close()
        return veriler
        
    def uye_aktif_kitaplarini_getir(self, uye_id):
        conn = self.baglan()
        cursor = conn.cursor()
        sql = """SELECT K.KitapAdi, O.SonTeslimTarihi FROM ODUNC O 
                 JOIN KITAP K ON O.KitapID = K.KitapID 
                 WHERE O.UyeID = %s AND O.TeslimTarihi IS NULL"""
        cursor.execute(sql, (uye_id,))
        veriler = cursor.fetchall()
        conn.close()
        return veriler

    # --- CEZALAR ---
    def cezalari_getir(self, uye_adi="", tarih_bas="", tarih_bit=""):
        conn = self.baglan()
        cursor = conn.cursor()
        sql = """SELECT C.CezaID, CONCAT(U.Ad, ' ', U.Soyad), K.KitapAdi, C.GecikmeGun, C.Tutar 
                 FROM CEZA C JOIN UYE U ON C.UyeID = U.UyeID 
                 JOIN ODUNC O ON C.OduncID = O.OduncID
                 JOIN KITAP K ON O.KitapID = K.KitapID
                 WHERE 1=1"""
        params = []
        if uye_adi:
            sql += " AND (U.Ad LIKE %s OR U.Soyad LIKE %s)"
            params.append(f"%{uye_adi}%"); params.append(f"%{uye_adi}%")
        if tarih_bas:
            sql += " AND O.TeslimTarihi >= %s"
            params.append(tarih_bas)
        if tarih_bit:
            sql += " AND O.TeslimTarihi <= %s"
            params.append(tarih_bit)
        cursor.execute(sql, params)
        veriler = cursor.fetchall()
        conn.close()
        return veriler

    # --- RAPORLAR ---
    def rapor_tarih_araligi(self, baslangic, bitis, uye_adi="", kategori=""):
        conn = self.baglan()
        cursor = conn.cursor()
        sql = """SELECT CONCAT(U.Ad, ' ', U.Soyad), K.KitapAdi, O.OduncTarihi, O.TeslimTarihi,
                 CASE WHEN O.TeslimTarihi IS NOT NULL THEN 'Teslim Edildi'
                      WHEN O.SonTeslimTarihi < CURDATE() THEN 'GECİKTİ'
                      ELSE 'Devam Ediyor' END 
                 FROM ODUNC O JOIN UYE U ON O.UyeID = U.UyeID JOIN KITAP K ON O.KitapID = K.KitapID
                 WHERE (O.OduncTarihi BETWEEN %s AND %s)"""
        params = [baslangic, bitis]
        if uye_adi:
            sql += " AND (U.Ad LIKE %s OR U.Soyad LIKE %s)"
            params.extend([f"%{uye_adi}%", f"%{uye_adi}%"])
        if kategori:
            sql += " AND K.Kategori = %s"
            params.append(kategori)
        sql += " ORDER BY O.OduncTarihi DESC"
        cursor.execute(sql, params)
        veriler = cursor.fetchall()
        conn.close()
        return veriler

    def rapor_gecikenler_detayli(self):
        conn = self.baglan()
        cursor = conn.cursor()
        sql = """SELECT CONCAT(U.Ad, ' ', U.Soyad), K.KitapAdi, O.OduncTarihi, O.SonTeslimTarihi,
                 DATEDIFF(CURDATE(), O.SonTeslimTarihi) 
                 FROM ODUNC O JOIN UYE U ON O.UyeID = U.UyeID JOIN KITAP K ON O.KitapID = K.KitapID
                 WHERE O.SonTeslimTarihi < CURDATE() AND O.TeslimTarihi IS NULL ORDER BY 5 DESC"""
        cursor.execute(sql)
        veriler = cursor.fetchall()
        conn.close()
        return veriler

    def rapor_populer_kitaplar(self, baslangic, bitis):
        conn = self.baglan()
        cursor = conn.cursor()
        sql = """SELECT K.KitapAdi, K.Yazar, K.Kategori, COUNT(O.OduncID) 
                 FROM ODUNC O JOIN KITAP K ON O.KitapID = K.KitapID
                 WHERE O.OduncTarihi BETWEEN %s AND %s
                 GROUP BY K.KitapID ORDER BY 4 DESC LIMIT 20"""
        cursor.execute(sql, (baslangic, bitis))
        veriler = cursor.fetchall()
        conn.close()
        return veriler