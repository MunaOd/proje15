import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QComboBox
import sqlite3

class KitapUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.baglantiyiOlustur()
        self.arayuzuOlustur()
        self.tabloyuOlustur()
        self.kitap_ve_yorumlari_goster()

    def arayuzuOlustur(self):
        self.setWindowTitle('KitapUygulamasi')
        self.setGeometry(100, 100, 600, 575)

        self.lbl_kullanici_adi = QLabel('Kullanıcı ID:', self)
        self.lbl_kullanici_adi.move(20, 20)
        self.txt_kullanici_adi = QLineEdit(self)
        self.txt_kullanici_adi.move(150, 20)

        self.lbl_sifre = QLabel('Şifre:', self)
        self.lbl_sifre.move(20, 60)
        self.txt_sifre = QLineEdit(self)
        self.txt_sifre.move(150, 60)
        self.txt_sifre.setEchoMode(QLineEdit.Password)

        self.btn_giris = QPushButton('Giriş Yap', self)
        self.btn_giris.move(150, 100)
        self.btn_giris.clicked.connect(self.girisYap)

        self.lbl_kitap_adi = QLabel('Kitap Adı:', self)
        self.lbl_kitap_adi.move(20, 155)
        self.combo_kitap_adi = QComboBox(self)
        self.combo_kitap_adi.move(130, 150)
        self.combo_kitap_adi.addItems(["Benim Adım Kırmızı", "Tutunamayanlar", "Masumiyet Müzesi", "Kürk Mantolu Madonna",
                                       "Aşk", "Saatleri Ayarlama Enstitüsü", "İstanbul Hatırası", "Bit Palas",
                                       "Gölgesizler", "Yaban"])

        self.lbl_yazar = QLabel('Yazar:', self)
        self.lbl_yazar.move(20, 195)
        self.combo_yazar = QComboBox(self)
        self.combo_yazar.move(130, 190)
        self.combo_yazar.addItems(["Orhan Pamuk", "Oğuz Atay", "Sabahattin Ali", "Elif Şafak",
                                   "Ahmet Hamdi Tanpınar", "Ahmet Ümit",
                                   "Hasan Ali Toptaş", "Yakup Kadri Karaosmanoğlu"])

        self.lbl_yayinevi = QLabel('Yayınevi:', self)
        self.lbl_yayinevi.move(20, 235)
        self.combo_yayinevi = QComboBox(self) 
        self.combo_yayinevi.move(130, 230)
        self.combo_yayinevi.addItems(["Yapı Kredi Yayınları", "İletişim Yayınevi", "Can Yayınları", 
                                      "Doğan Kitap", "Everest Yayınları"])

        self.btn_kitap_ekle = QPushButton('Kitap Ekle', self)
        self.btn_kitap_ekle.move(150, 270)
        self.btn_kitap_ekle.clicked.connect(self.kitapEkle)

        self.lbl_yorum = QLabel('Yorum Metni:', self)
        self.lbl_yorum.move(20, 340)
        self.txt_yorum = QTextEdit(self)
        self.txt_yorum.setGeometry(130, 340, 180, 100)

        self.btn_yorum_ekle = QPushButton('Yorum Ekle', self)
        self.btn_yorum_ekle.move(150, 450)
        self.btn_yorum_ekle.clicked.connect(self.yorumEkle)

        self.lbl_added_info = QLabel('Eklenen Bilgiler:', self)
        self.lbl_added_info.move(350, 20)
        self.txt_added_info = QTextEdit(self)
        self.txt_added_info.setGeometry(350, 40, 230, 400)

        self.lbl_delete = QLabel('Silinecek Kitap ID:', self)
        self.lbl_delete.move(350, 510)
        self.txt_delete = QLineEdit(self)
        self.txt_delete.setGeometry(480, 510, 100, 20)

        self.btn_delete = QPushButton('Kitap Sil', self)
        self.btn_delete.move(400, 530)
        self.btn_delete.clicked.connect(self.kitapSil)

        self.lbl_delete_yorum = QLabel('Silinecek Yorum ID:', self)
        self.lbl_delete_yorum.move(350, 450)
        self.txt_delete_yorum = QLineEdit(self)
        self.txt_delete_yorum.setGeometry(480, 450, 100, 20)

        self.btn_delete_yorum = QPushButton('Yorum Sil', self)
        self.btn_delete_yorum.move(400, 470)
        self.btn_delete_yorum.clicked.connect(self.yorumSil)

        self.lbl_secilen_kitap = QLabel('Yorum Yapılan Kitap ID:', self)
        self.lbl_secilen_kitap.move(20, 700)
        self.combo_secilen_kitap = QComboBox(self)
        self.combo_secilen_kitap.move(180, 700)

        self.populateKitapIDComboList()

    def populateKitapIDComboList(self):
        self.combo_secilen_kitap.clear()

        self.cursor.execute('''SELECT id FROM kitaplar''')
        kitaplar = self.cursor.fetchall()

        for kitap in kitaplar:
            self.combo_secilen_kitap.addItem(str(kitap[0]))

    def baglantiyiOlustur(self):
        self.baglanti = sqlite3.connect('kitap_veritabani.db')
        self.cursor = self.baglanti.cursor()

    def tabloyuOlustur(self):
        self.cursor.execute('''DROP TABLE IF EXISTS kitaplar''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kitaplar (
                            id INTEGER PRIMARY KEY,
                            ad TEXT,
                            yazar TEXT,
                            yayinevi TEXT)''')
        self.cursor.execute('''DROP TABLE IF EXISTS yorumlar''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS yorumlar (
                            id INTEGER PRIMARY KEY,
                            yorum TEXT,
                            yorum_yapan TEXT,
                            kitap_id INTEGER,
                            FOREIGN KEY(kitap_id) REFERENCES kitaplar(id))''')
        self.baglanti.commit()

    def girisYap(self):
        kullanici_adi = self.txt_kullanici_adi.text()
        sifre = self.txt_sifre.text()

        if kullanici_adi == "admin" and sifre == "admin":
            QMessageBox.information(self, 'Giriş Başarılı', 'Hoş geldiniz!')
        else:
            QMessageBox.warning(self, 'Hata', 'Geçersiz kullanıcı adı veya şifre!')

    def kitapEkle(self):
        kitap_adi = self.combo_kitap_adi.currentText()
        yazar = self.combo_yazar.currentText() 
        yayinevi = self.combo_yayinevi.currentText() 
        self.cursor.execute('''INSERT INTO kitaplar (ad, yazar, yayinevi) VALUES (?, ?, ?)''', (kitap_adi, yazar, yayinevi))
        self.baglanti.commit()
        self.cursor.execute('''SELECT MAX(id) FROM kitaplar''')
        latest_kitap_id = self.cursor.fetchone()[0]
        
        self.combo_secilen_kitap.addItem(str(latest_kitap_id))
        self.kitap_ve_yorumlari_goster()

    def yorumEkle(self):
        yorum = self.txt_yorum.toPlainText()
        yorum_yapan = self.txt_kullanici_adi.text() 
        kitap_id = self.combo_secilen_kitap.currentText() 
        self.cursor.execute('''INSERT INTO yorumlar (yorum, yorum_yapan, kitap_id) VALUES (?, ?, ?)''', (yorum, yorum_yapan, kitap_id))
        self.baglanti.commit()
        self.txt_yorum.clear()
        self.kitap_ve_yorumlari_goster()

    def yorumSil(self):
        yorum_id = self.txt_delete_yorum.text()
        self.cursor.execute('''DELETE FROM yorumlar WHERE id = ?''', (yorum_id,))
        self.baglanti.commit()
        self.kitap_ve_yorumlari_goster()

    def kitapSil(self):
        kitap_id = self.txt_delete.text()
        self.cursor.execute('''DELETE FROM kitaplar WHERE id = ?''', (kitap_id,))
        self.baglanti.commit()
        self.kitap_ve_yorumlari_goster()

    def kitap_ve_yorumlari_goster(self):
        self.txt_added_info.clear()
        self.cursor.execute('''SELECT * FROM kitaplar''')
        kitaplar = self.cursor.fetchall()
        self.cursor.execute('''SELECT * FROM yorumlar''')
        yorumlar = self.cursor.fetchall()

        self.txt_added_info.append("              ---- KİTAPLAR ----  ")
        for kitap in kitaplar:
            self.txt_added_info.append(f"ID: {kitap[0]}, Ad: {kitap[1]}, Yazar: {kitap[2]}, Yayınevi: {kitap[3]}")

        self.txt_added_info.append("\n\n\n\n\n\n\n\n\n\n           ---- YORUMLAR ----")
        for yorum in yorumlar:
            self.txt_added_info.append(f"Yorum ID: {yorum[0]}, Yorum: {yorum[1]}, Yapan: {yorum[2]}, Kitap ID: {yorum[3]}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KitapUygulamasi()
    ex.show()
    sys.exit(app.exec_())