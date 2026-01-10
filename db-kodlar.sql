CREATE DATABASE  IF NOT EXISTS `kutuphane-otomat` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `kutuphane-otomat`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: kutuphane-otomat
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ceza`
--

DROP TABLE IF EXISTS `ceza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ceza` (
  `CezaID` int NOT NULL AUTO_INCREMENT,
  `OduncID` int DEFAULT NULL,
  `UyeID` int DEFAULT NULL,
  `GecikmeGun` int DEFAULT NULL,
  `Tutar` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`CezaID`),
  KEY `OduncID` (`OduncID`),
  KEY `UyeID` (`UyeID`),
  CONSTRAINT `ceza_ibfk_1` FOREIGN KEY (`OduncID`) REFERENCES `odunc` (`OduncID`),
  CONSTRAINT `ceza_ibfk_2` FOREIGN KEY (`UyeID`) REFERENCES `uye` (`UyeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ceza`
--

LOCK TABLES `ceza` WRITE;
/*!40000 ALTER TABLE `ceza` DISABLE KEYS */;
/*!40000 ALTER TABLE `ceza` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `TR_CEZA_INSERT` AFTER INSERT ON `ceza` FOR EACH ROW BEGIN
    -- 1. Üyenin borcunu güncelle
    UPDATE UYE SET ToplamBorc = ToplamBorc + NEW.Tutar WHERE UyeID = NEW.UyeID;
    
    -- 2. Log Yaz
    INSERT INTO LOG_ISLEM (TabloAdi, IslemTuru, Aciklama)
    VALUES ('CEZA', 'INSERT', CONCAT('Üyeye ', NEW.Tutar, ' TL ceza eklendi.'));
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `kitap`
--

DROP TABLE IF EXISTS `kitap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kitap` (
  `KitapID` int NOT NULL AUTO_INCREMENT,
  `KitapAdi` varchar(100) NOT NULL,
  `Yazar` varchar(100) DEFAULT NULL,
  `Kategori` varchar(50) DEFAULT NULL,
  `Yayinevi` varchar(50) DEFAULT NULL,
  `BasimYili` int DEFAULT NULL,
  `ToplamAdet` int NOT NULL,
  `MevcutAdet` int NOT NULL,
  PRIMARY KEY (`KitapID`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kitap`
--

LOCK TABLES `kitap` WRITE;
/*!40000 ALTER TABLE `kitap` DISABLE KEYS */;
INSERT INTO `kitap` VALUES (1,'Nutuk','Mustafa Kemal Atatürk','Tarih','Yapı Kredi Yayınları',1927,10,6),(2,'Sefiller','Victor Hugo','Roman','Can Yayınları',1862,5,4),(3,'Suç ve Ceza','Fyodor Dostoyevski','Roman','İş Bankası Yayınları',1866,8,7),(4,'1984','George Orwell','Bilim Kurgu','Can Yayınları',1949,12,10),(5,'Hayvan Çiftliği','George Orwell','Edebiyat','Can Yayınları',1945,15,14),(6,'Saatleri Ayarlama Enstitüsü','Ahmet Hamdi Tanpınar','Edebiyat','Dergah Yayınları',1961,6,5),(7,'Kürk Mantolu Madonna','Sabahattin Ali','Edebiyat','YKY',1943,20,19),(8,'İnce Memed 1','Yaşar Kemal','Roman','Yapı Kredi Yayınları',1955,7,5),(9,'Tutunamayanlar','Oğuz Atay','Edebiyat','İletişim Yayınları',1971,5,4),(10,'Simyacı','Paulo Coelho','Roman','Can Yayınları',1988,25,24),(11,'Küçük Prens','Antoine de Saint-Exupéry','Edebiyat','Can Yayınları',1943,30,28),(12,'Yüzyıllık Yalnızlık','Gabriel García Márquez','Roman','Can Yayınları',1967,4,4),(13,'Uçurtma Avcısı','Khaled Hosseini','Roman','Everest Yayınları',2003,10,9),(14,'Dune','Frank Herbert','Bilim Kurgu','İthaki Yayınları',1965,9,9),(15,'Fahrenheit 451','Ray Bradbury','Bilim Kurgu','İthaki Yayınları',1953,11,8),(16,'Sapiens','Yuval Noah Harari','Bilim','Kolektif Kitap',2011,14,14),(17,'Kozmos','Carl Sagan','Bilim','Altın Kitaplar',1980,3,0),(18,'Zamanın Kısa Tarihi','Stephen Hawking','Bilim','Alfa Yayınları',1988,6,5),(19,'Tüfek, Mikrop ve Çelik','Jared Diamond','Tarih','Pegasus Yayınları',1997,5,4),(20,'İlber Ortaylı - Türklerin Tarihi','İlber Ortaylı','Tarih','Timaş Yayınları',2015,12,10),(21,'Devlet','Platon','Felsefe','İş Bankası Yayınları',-375,8,8),(22,'Böyle Buyurdu Zerdüşt','Friedrich Nietzsche','Felsefe','İş Bankası Yayınları',1883,7,6),(23,'Dönüşüm','Franz Kafka','Edebiyat','Can Yayınları',1915,18,17),(24,'Sherlock Holmes - Kızıl Dosya','Arthur Conan Doyle','Roman','Ren Kitap',1887,10,10),(25,'Yüzüklerin Efendisi - Yüzük Kardeşliği','J.R.R. Tolkien','Roman','Metis Yayınları',1954,6,5),(26,'Harry Potter ve Felsefe Taşı','J.K. Rowling','Roman','YKY',1997,15,14),(27,'Algoritmalara Giriş','Thomas H. Cormen','Yazılım','Palme Yayıncılık',1990,4,2),(28,'Python ile Veri Analizi','Wes McKinney','Yazılım','Buzdağı Yayınevi',2012,7,7),(29,'Yabancı','Albert Camus','Edebiyat','Can Yayınları',1942,9,8),(30,'Körlük','José Saramago','Roman','Can Yayınları',1995,8,6);
/*!40000 ALTER TABLE `kitap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kullanici`
--

DROP TABLE IF EXISTS `kullanici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kullanici` (
  `KullaniciID` int NOT NULL AUTO_INCREMENT,
  `KullaniciAdi` varchar(50) NOT NULL,
  `Sifre` varchar(100) NOT NULL,
  `Rol` enum('Admin','Görevli') NOT NULL,
  PRIMARY KEY (`KullaniciID`),
  UNIQUE KEY `KullaniciAdi` (`KullaniciAdi`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kullanici`
--

LOCK TABLES `kullanici` WRITE;
/*!40000 ALTER TABLE `kullanici` DISABLE KEYS */;
INSERT INTO `kullanici` VALUES (1,'admin','1234','Admin');
/*!40000 ALTER TABLE `kullanici` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kullanicilar`
--

DROP TABLE IF EXISTS `kullanicilar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kullanicilar` (
  `KullaniciID` int NOT NULL AUTO_INCREMENT,
  `KullaniciAdi` varchar(255) NOT NULL,
  `Sifre` varchar(255) NOT NULL,
  `Rol` varchar(50) NOT NULL,
  PRIMARY KEY (`KullaniciID`),
  UNIQUE KEY `KullaniciAdi` (`KullaniciAdi`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kullanicilar`
--

LOCK TABLES `kullanicilar` WRITE;
/*!40000 ALTER TABLE `kullanicilar` DISABLE KEYS */;
INSERT INTO `kullanicilar` VALUES (1,'admin','1234','Yonetici'),(2,'gorevli1','1234','Personel');
/*!40000 ALTER TABLE `kullanicilar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_islem`
--

DROP TABLE IF EXISTS `log_islem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_islem` (
  `LogID` int NOT NULL AUTO_INCREMENT,
  `TabloAdi` varchar(50) DEFAULT NULL,
  `IslemTuru` varchar(20) DEFAULT NULL,
  `Aciklama` text,
  `IslemZamani` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`LogID`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_islem`
--

LOCK TABLES `log_islem` WRITE;
/*!40000 ALTER TABLE `log_islem` DISABLE KEYS */;
INSERT INTO `log_islem` VALUES (1,'ODUNC','INSERT','Üye 7 Kitap 6 ödünç aldı.','2026-01-05 16:48:20'),(2,'ODUNC','INSERT','Üye 4 Kitap 11 ödünç aldı.','2026-01-05 16:48:22'),(3,'ODUNC','INSERT','Üye 7 Kitap 8 ödünç aldı.','2026-01-05 16:48:27'),(4,'ODUNC','INSERT','Üye 12 Kitap 15 ödünç aldı.','2026-01-05 16:48:30'),(5,'ODUNC','INSERT','Üye 19 Kitap 20 ödünç aldı.','2026-01-05 16:48:35'),(6,'ODUNC','INSERT','Üye 28 Kitap 27 ödünç aldı.','2026-01-05 16:48:39'),(7,'ODUNC','INSERT','Üye 32 Kitap 17 ödünç aldı.','2026-01-05 16:48:43'),(8,'ODUNC','INSERT','Üye 9 Kitap 15 ödünç aldı.','2026-01-05 16:48:48'),(9,'ODUNC','INSERT','Üye 1 Kitap 22 ödünç aldı.','2026-01-05 16:48:53'),(10,'ODUNC','INSERT','Üye 2 Kitap 11 ödünç aldı.','2026-01-05 16:48:57'),(11,'ODUNC','INSERT','Üye 3 Kitap 13 ödünç aldı.','2026-01-05 16:49:01'),(12,'ODUNC','INSERT','Üye 5 Kitap 19 ödünç aldı.','2026-01-05 16:49:08'),(13,'ODUNC','INSERT','Üye 7 Kitap 23 ödünç aldı.','2026-01-05 16:49:12'),(14,'ODUNC','INSERT','Üye 8 Kitap 27 ödünç aldı.','2026-01-05 16:49:16'),(15,'ODUNC','INSERT','Üye 10 Kitap 29 ödünç aldı.','2026-01-05 16:49:22'),(16,'ODUNC','INSERT','Üye 11 Kitap 25 ödünç aldı.','2026-01-05 16:49:31'),(17,'ODUNC','INSERT','Üye 13 Kitap 18 ödünç aldı.','2026-01-05 16:49:38'),(18,'ODUNC','INSERT','Üye 14 Kitap 17 ödünç aldı.','2026-01-05 16:49:44'),(19,'ODUNC','INSERT','Üye 15 Kitap 7 ödünç aldı.','2026-01-05 16:49:50'),(20,'ODUNC','INSERT','Üye 16 Kitap 3 ödünç aldı.','2026-01-05 16:49:55'),(21,'ODUNC','INSERT','Üye 17 Kitap 4 ödünç aldı.','2026-01-05 16:50:00'),(22,'ODUNC','INSERT','Üye 18 Kitap 5 ödünç aldı.','2026-01-05 16:50:04'),(23,'ODUNC','INSERT','Üye 20 Kitap 10 ödünç aldı.','2026-01-05 16:50:10'),(24,'ODUNC','INSERT','Üye 21 Kitap 1 ödünç aldı.','2026-01-05 16:50:14'),(25,'ODUNC','INSERT','Üye 22 Kitap 1 ödünç aldı.','2026-01-05 16:50:18'),(26,'ODUNC','INSERT','Üye 23 Kitap 1 ödünç aldı.','2026-01-05 16:50:25'),(27,'ODUNC','INSERT','Üye 24 Kitap 1 ödünç aldı.','2026-01-05 16:50:32'),(28,'ODUNC','INSERT','Üye 25 Kitap 2 ödünç aldı.','2026-01-05 16:50:38'),(29,'ODUNC','INSERT','Üye 26 Kitap 9 ödünç aldı.','2026-01-05 16:50:42'),(30,'ODUNC','INSERT','Üye 27 Kitap 17 ödünç aldı.','2026-01-05 16:50:45'),(31,'ODUNC','INSERT','Üye 28 Kitap 30 ödünç aldı.','2026-01-05 16:50:49'),(32,'ODUNC','INSERT','Üye 29 Kitap 30 ödünç aldı.','2026-01-05 16:50:54'),(33,'ODUNC','INSERT','Üye 30 Kitap 20 ödünç aldı.','2026-01-05 16:51:00'),(34,'ODUNC','INSERT','Üye 31 Kitap 15 ödünç aldı.','2026-01-05 16:51:03'),(35,'ODUNC','INSERT','Üye 32 Kitap 26 ödünç aldı.','2026-01-05 16:51:07'),(36,'ODUNC','INSERT','Üye 1 Kitap 8 ödünç aldı.','2026-01-09 22:46:11'),(37,'ODUNC','INSERT','Üye 8 Kitap 4 ödünç aldı.','2026-01-09 22:46:21');
/*!40000 ALTER TABLE `log_islem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `odunc`
--

DROP TABLE IF EXISTS `odunc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `odunc` (
  `OduncID` int NOT NULL AUTO_INCREMENT,
  `UyeID` int DEFAULT NULL,
  `KitapID` int DEFAULT NULL,
  `KullaniciID` int DEFAULT NULL,
  `OduncTarihi` date DEFAULT (curdate()),
  `SonTeslimTarihi` date DEFAULT NULL,
  `TeslimTarihi` date DEFAULT NULL,
  PRIMARY KEY (`OduncID`),
  KEY `UyeID` (`UyeID`),
  KEY `KitapID` (`KitapID`),
  KEY `KullaniciID` (`KullaniciID`),
  CONSTRAINT `odunc_ibfk_1` FOREIGN KEY (`UyeID`) REFERENCES `uye` (`UyeID`),
  CONSTRAINT `odunc_ibfk_2` FOREIGN KEY (`KitapID`) REFERENCES `kitap` (`KitapID`),
  CONSTRAINT `odunc_ibfk_3` FOREIGN KEY (`KullaniciID`) REFERENCES `kullanicilar` (`KullaniciID`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `odunc`
--

LOCK TABLES `odunc` WRITE;
/*!40000 ALTER TABLE `odunc` DISABLE KEYS */;
INSERT INTO `odunc` VALUES (1,7,6,1,'2026-01-05','2026-01-20',NULL),(2,4,11,1,'2026-01-05','2026-01-20',NULL),(3,7,8,1,'2026-01-05','2026-01-20',NULL),(4,12,15,1,'2026-01-05','2026-01-20',NULL),(5,19,20,1,'2026-01-05','2026-01-20',NULL),(6,28,27,1,'2026-01-05','2026-01-20',NULL),(7,32,17,1,'2026-01-05','2026-01-20',NULL),(8,9,15,1,'2026-01-05','2026-01-20',NULL),(9,1,22,1,'2026-01-05','2026-01-20',NULL),(10,2,11,1,'2026-01-05','2026-01-20',NULL),(11,3,13,1,'2026-01-05','2026-01-20',NULL),(12,5,19,1,'2026-01-05','2026-01-20',NULL),(13,7,23,1,'2026-01-05','2026-01-20',NULL),(14,8,27,1,'2026-01-05','2026-01-20',NULL),(15,10,29,1,'2026-01-05','2026-01-20',NULL),(16,11,25,1,'2026-01-05','2026-01-20',NULL),(17,13,18,1,'2026-01-05','2026-01-20',NULL),(18,14,17,1,'2026-01-05','2026-01-20',NULL),(19,15,7,1,'2026-01-05','2026-01-20',NULL),(20,16,3,1,'2026-01-05','2026-01-20',NULL),(21,17,4,1,'2026-01-05','2026-01-20',NULL),(22,18,5,1,'2026-01-05','2026-01-20',NULL),(23,20,10,1,'2026-01-05','2026-01-20',NULL),(24,21,1,1,'2026-01-05','2026-01-20',NULL),(25,22,1,1,'2026-01-05','2026-01-20',NULL),(26,23,1,1,'2026-01-05','2026-01-20',NULL),(27,24,1,1,'2026-01-05','2026-01-20',NULL),(28,25,2,1,'2026-01-05','2026-01-20',NULL),(29,26,9,1,'2026-01-05','2026-01-20',NULL),(30,27,17,1,'2026-01-05','2026-01-20',NULL),(31,28,30,1,'2026-01-05','2026-01-20',NULL),(32,29,30,1,'2026-01-05','2026-01-20',NULL),(33,30,20,1,'2026-01-05','2026-01-20',NULL),(34,31,15,1,'2026-01-05','2026-01-20',NULL),(35,32,26,1,'2026-01-05','2026-01-20',NULL),(36,1,8,1,'2026-01-10','2026-01-25',NULL),(37,8,4,1,'2026-01-10','2026-01-25',NULL);
/*!40000 ALTER TABLE `odunc` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `TR_ODUNC_INSERT` AFTER INSERT ON `odunc` FOR EACH ROW BEGIN
    -- 1. Stok Düşür (Hocanın şartı: Trigger yapmalı)
    UPDATE KITAP SET MevcutAdet = MevcutAdet - 1 WHERE KitapID = NEW.KitapID;
    
    -- 2. Log Yaz
    INSERT INTO LOG_ISLEM (TabloAdi, IslemTuru, Aciklama)
    VALUES ('ODUNC', 'INSERT', CONCAT('Üye ', NEW.UyeID, ' Kitap ', NEW.KitapID, ' ödünç aldı.'));
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `TR_ODUNC_UPDATE_TESLIM` AFTER UPDATE ON `odunc` FOR EACH ROW BEGIN
    -- Eğer kitap iade edildiyse (TeslimTarihi NULL'dan Dolu'ya döndüyse)
    IF OLD.TeslimTarihi IS NULL AND NEW.TeslimTarihi IS NOT NULL THEN
        -- 1. Stok Artır (Hocanın şartı: Trigger yapmalı)
        UPDATE KITAP SET MevcutAdet = MevcutAdet + 1 WHERE KitapID = NEW.KitapID;
        
        -- 2. Log Yaz
        INSERT INTO LOG_ISLEM (TabloAdi, IslemTuru, Aciklama)
        VALUES ('ODUNC', 'UPDATE', CONCAT('OduncID ', NEW.OduncID, ' iade edildi.'));
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `uye`
--

DROP TABLE IF EXISTS `uye`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uye` (
  `UyeID` int NOT NULL AUTO_INCREMENT,
  `Ad` varchar(50) NOT NULL,
  `Soyad` varchar(50) NOT NULL,
  `Telefon` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `ToplamBorc` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`UyeID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uye`
--

LOCK TABLES `uye` WRITE;
/*!40000 ALTER TABLE `uye` DISABLE KEYS */;
INSERT INTO `uye` VALUES (1,'erdem','gökçe','5079393574','erdemgoekche@gmail.com',0.00),(2,'emirhan','sağlam','q','emirhansaglam@gmail.com',0.00),(3,'yasemin','dağ','w','yasemin.dag@gmail.com',0.00),(4,'duru','eken','e','durueken@gmail.com',0.00),(5,'elanur','demircioğlu','r','elanurdemirci@gmail.com',0.00),(6,'tuğçe','üstün','t','tugceustun@gmail.com',0.00),(7,'esranur','akbulut','u','esranurakbulut@gmail.com',0.00),(8,'efe','sekili','ı','efe.sekili@gmail.com',0.00),(9,'yavuz selim','sağlam','o','yavuz.saglam@gmail.com',0.00),(10,'mustafaa','bozkurt','p','mbozkurt@gmail.com',0.00),(11,'melisa','ince','ğ','melisaince@gmail.com',0.00),(12,'betül','yağlı','ü','betul.yagli@gmail.com',0.00),(13,'acelya','talya','a','acelya.talya@gmail.com',0.00),(14,'enes kaan','afacan','s','kaan.afacan@gmail.com',0.00),(15,'yasir','ağabeyoğlu','s','yasir.agabey@gmail.com',0.00),(16,'ahmet','temiztürk','d','ahmet.temizturk@gmail.com',0.00),(17,'akif','okumuş','f','akif.okumus@gmail.com',0.00),(18,'ali berk','korumaz','g','aliberk@gmail.com',0.00),(19,'ali turab','rızaoğlu','h','aturab@gmail.com',0.00),(20,'hakan','aydemir','k','hakan.aydemir@gmail.com',0.00),(21,'serkan','kaçalın','l','serkan.kacalin@gmail.com',0.00),(22,'ömer','güçlü','ş','omer.guclu@gmail.com',0.00),(23,'furkan','zorlu','i','furkan.zorlu@gmail.com',0.00),(24,'sebiha','ciğer','z','sebiha.ciger@gmail.com',0.00),(25,'yusuf emir','baysal','x','yusuf.baysal@gmail.com',0.00),(26,'alperen','demir','c','alperen.demir@gmail.com',0.00),(27,'dilara','koca','v','dilara.koca@gmail.com',0.00),(28,'ibrahim','elma','b','ibrahim.elma@gmail.com',0.00),(29,'cansu','abaci','n','cansu.abaci@gmail.com',0.00),(30,'nisa nur','cansarı','m','nisacansari@gmail.com',0.00),(31,'emir','avan','ö','emir.avan@gmail.com',0.00),(32,'mehmet','erben','ç','mehmet.erben@gmail.com',0.00),(33,'Mustafa','KEMAL','12312313124','mustafakemal@gmail.com',0.00);
/*!40000 ALTER TABLE `uye` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `TR_UYE_DELETE_BLOCK` BEFORE DELETE ON `uye` FOR EACH ROW BEGIN
    DECLARE aktif_odunc INT;
    
    -- Üyenin elinde kitap var mı?
    SELECT COUNT(*) INTO aktif_odunc FROM ODUNC WHERE UyeID = OLD.UyeID AND TeslimTarihi IS NULL;
    
    -- Eğer elinde kitap varsa VEYA borcu 0'dan büyükse engelle
    IF aktif_odunc > 0 OR OLD.ToplamBorc > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'UYARI: Borcu veya iade etmediği kitabı olan üye silinemez!';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Dumping events for database 'kutuphane-otomat'
--

--
-- Dumping routines for database 'kutuphane-otomat'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_KitapTeslimAl` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_KitapTeslimAl`(IN p_OduncID INT)
BEGIN
    DECLARE v_UyeID INT;
    DECLARE v_KitapID INT;
    DECLARE gecikme INT;
    DECLARE ceza_tutari DECIMAL(10,2);
    DECLARE v_SonTeslim DATE;

    SELECT UyeID, KitapID, SonTeslimTarihi INTO v_UyeID, v_KitapID, v_SonTeslim
    FROM ODUNC WHERE OduncID = p_OduncID;

    -- SADECE TARİHİ GÜNCELLİYORUZ. STOK ARTIRMA İŞİNİ TRIGGER YAPACAK.
    UPDATE ODUNC SET TeslimTarihi = CURDATE() WHERE OduncID = p_OduncID;

    -- Ceza Hesaplama
    SET gecikme = DATEDIFF(CURDATE(), v_SonTeslim);

    IF gecikme > 0 THEN
        SET ceza_tutari = gecikme * 5.00;
        -- Ceza eklenince borç artırma işini de TRIGGER yapacak.
        INSERT INTO CEZA (OduncID, UyeID, GecikmeGun, Tutar) VALUES (p_OduncID, v_UyeID, gecikme, ceza_tutari);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_UyeOzetRapor` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_UyeOzetRapor`(IN p_UyeID INT)
BEGIN
    SELECT 
        (SELECT COUNT(*) FROM ODUNC WHERE UyeID = p_UyeID) AS ToplamKitap,
        (SELECT COUNT(*) FROM ODUNC WHERE UyeID = p_UyeID AND TeslimTarihi IS NULL) AS EldekiKitap,
        ToplamBorc
    FROM UYE WHERE UyeID = p_UyeID;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_YeniOduncVer` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_YeniOduncVer`(IN p_UyeID INT, IN p_KitapID INT, IN p_KullaniciID INT)
BEGIN
    DECLARE aktif_odunc INT;
    DECLARE stok_durumu INT;

    SELECT COUNT(*) INTO aktif_odunc FROM ODUNC WHERE UyeID = p_UyeID AND TeslimTarihi IS NULL;
    SELECT MevcutAdet INTO stok_durumu FROM KITAP WHERE KitapID = p_KitapID;

    IF aktif_odunc >= 5 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Üye limitine ulaştı (Max 5 kitap)!';
    ELSEIF stok_durumu <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Kitap stokta yok!';
    ELSE
        -- SADECE INSERT YAPIYORUZ. STOK DÜŞME İŞİNİ TRIGGER YAPACAK.
        INSERT INTO ODUNC (UyeID, KitapID, KullaniciID, OduncTarihi, SonTeslimTarihi)
        VALUES (p_UyeID, p_KitapID, p_KullaniciID, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY));
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-10  3:50:02
