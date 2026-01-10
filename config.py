class Ayarlar:
    # Veritabanı bağlantı bilgilerini buraya yaz
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASS = "admin"  # <-- Kendi MySQL şifreni buraya yaz
    DB_NAME = "kutuphane-otomat"

class Oturum:
    # Anlık giriş yapan kullanıcının verileri burada tutulur
    mevcut_kullanici = None
    mevcut_rol = None  # 'Yönetici' veya 'Personel'

    @staticmethod
    def oturum_ac(kadi, rol):
        Oturum.mevcut_kullanici = kadi
        Oturum.mevcut_rol = rol

    @staticmethod
    def oturum_kapat():
        Oturum.mevcut_kullanici = None
        Oturum.mevcut_rol = None