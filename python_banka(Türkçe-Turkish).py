"""
Programın çalışması için windows cmd ekranına teker teker;

pip install PyQt5
pip install requests
pip install BeatifulSoup4
pip install sip

yazılarak kütüphaneler indirilmelidir.
"""
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
import sys
import sqlite3
import time
from datetime import datetime
import locale
import random
import requests
from bs4 import BeautifulSoup
import sip

#giriş yapmak ve kayıt silmek için hesap numarasının global değişken olarak tutulması gerekiyor.
giris_hesapno = list()
kayit_sil_hesapno = list()

#verilen site urlsinden döviz bilgilerini çekmek için kullanılır.
dolar_url = "https://kur.doviz.com"
response = requests.get(dolar_url)
html_icerigi = response.content
soup = BeautifulSoup(html_icerigi,"html.parser")
liste = soup.find_all("td",{"class":"text-bold"})
ana_sayfa_dolar_bilgi = liste[0].text
ana_sayfa_euro_bilgi = liste[3].text
ana_sayfa_sterlin_bilgi = liste[6].text
dolar_bilgi = float(liste[0].text.replace(",","."))
euro_bilgi = float(liste[3].text.replace(",","."))
sterlin_bilgi = float(liste[6].text.replace(",","."))
isvicre_frangi_bilgi = float(liste[9].text.replace(",","."))
kanada_dolari_bilgi = float(liste[12].text.replace(",","."))
rus_rublesi_bilgi = float(liste[15].text.replace(",","."))
isvec_kronu_bilgi = float(liste[28].text.replace(",","."))
japon_yeni_bilgi = float(liste[34].text.replace(",","."))
kuveyt_dinari_bilgi = float(liste[37].text.replace(",","."))
cin_yuani_bilgi = float(liste[88].text.replace(",","."))
doviz_degerleri_listesi = [["Dolar",dolar_bilgi],["Euro",euro_bilgi],["İngiliz Sterlini",sterlin_bilgi],["İsviçre Frangı",isvicre_frangi_bilgi],["Kanada Doları",kanada_dolari_bilgi],["Rus Rublesi",rus_rublesi_bilgi],["İsveç Kronu",isvec_kronu_bilgi],["Japon Yeni",japon_yeni_bilgi],["Kuveyt Dinarı",kuveyt_dinari_bilgi],["Çin Yuanı",cin_yuani_bilgi]]

#verilen site urlsinden hisse bilgilerini çekmek için kullanılır.
yatırım_url = "https://finans.mynet.com/borsa/hisseler/"
response = requests.get(yatırım_url)
html_icerigi = response.content
soup = BeautifulSoup(html_icerigi,"html.parser")
liste1 = soup.find_all("td",{"class":"text-center"})
acsel_bilgi = float(liste1[1].text.replace(",","."))
adel_bilgi = float(liste1[6].text.replace(",","."))
adese_bilgi = float(liste1[11].text.replace(",","."))
aefes_bilgi = float(liste1[16].text.replace(",","."))
afyon_bilgi = float(liste1[21].text.replace(",","."))
aghol_bilgi = float(liste1[26].text.replace(",","."))
agyo_bilgi = float(liste1[31].text.replace(",","."))
akbnk_bilgi = float(liste1[36].text.replace(",","."))
akcns_bilgi = float(liste1[41].text.replace(",","."))
akenr_bilgi = float(liste1[46].text.replace(",","."))
hisse_degerleri_listesi = [["ACSEL",acsel_bilgi],["ADEL",adel_bilgi],["ADESE",adese_bilgi],["AEFES",aefes_bilgi],["AFYON",afyon_bilgi],["AGHOL",aghol_bilgi],["AGYO",agyo_bilgi],["AKBNK",akbnk_bilgi],["AKCNS",akcns_bilgi],["AKENR",akenr_bilgi]]

locale.setlocale(locale.LC_ALL,"")

class Ana_Menu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_giris_sayfasi()
        self.setWindowTitle("Alize Bankası")
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QtGui.QIcon("logo.png"))

    def bilgileri_al(self):
        #Giriş yapılan hesabın hesap numarasına göre veritabanından tüm bilgilerini alarak bunları değişkenlere atanmasını yapar.
        self.bağlantı = sqlite3.connect("database.db")
        self.cursor = self.bağlantı.cursor()
        self.cursor.execute("select * from BANKA_MUSTERILERI where Hesap_No = ?",(giris_hesapno[0],))
        bilgi_liste = self.cursor.fetchall()
        self.hesapisim = bilgi_liste[0][0]
        self.hesapbakiye = bilgi_liste[0][3]
        self.hesapbakiye = round(self.hesapbakiye,2)
        self.hesapborc = float(bilgi_liste[0][4])
        self.hesapborc = round(self.hesapborc,2)
        self.cursor.execute("select * from DOVIZ where Hesap_No = ?",(giris_hesapno[0],))
        doviz_liste = self.cursor.fetchall()
        self.hesapdolar = doviz_liste[0][1]
        self.hesapeuro = doviz_liste[0][2]
        self.hesapsterlin = doviz_liste[0][3]
        self.hesapisvicrefrangi = doviz_liste[0][4]
        self.hesapkanadadolari = doviz_liste[0][5]
        self.hesaprusrublesi = doviz_liste[0][6]
        self.hesapisveckronu = doviz_liste[0][7]
        self.hesapjaponyeni = doviz_liste[0][8]
        self.hesapkuveytdinari = doviz_liste[0][9]
        self.hesapcinyuani = doviz_liste[0][10]
        self.cursor.execute("select * from YATIRIM where Hesap_No = ?",(giris_hesapno[0],))
        yatırım_liste = self.cursor.fetchall()
        self.hesapacsel = yatırım_liste[0][1]
        self.hesapadel = yatırım_liste[0][2]
        self.hesapadese = yatırım_liste[0][3]
        self.hesapaefes = yatırım_liste[0][4]
        self.hesapafyon = yatırım_liste[0][5]
        self.hesapaghol = yatırım_liste[0][6]
        self.hesapagyo = yatırım_liste[0][7]
        self.hesapakbnk = yatırım_liste[0][8]
        self.hesapakcns= yatırım_liste[0][9]
        self.hesapakenr = yatırım_liste[0][10]

        self.toplam_doviz_bakiye = (self.hesapdolar+self.hesapeuro+self.hesapsterlin+self.hesapisvicrefrangi+self.hesapkanadadolari+self.hesaprusrublesi+self.hesapisveckronu+self.hesapjaponyeni+self.hesapkuveytdinari+self.hesapcinyuani)
        self.toplam_doviz_bakiye = round(self.toplam_doviz_bakiye,2)
        #Hesap bilgilerinde döviz bakiyesinin gözükmesi için tüm döviz bilgileri toplar

        self.toplam_hisse_bakiye = (self.hesapacsel+self.hesapadel+self.hesapadese+self.hesapaefes+self.hesapafyon+self.hesapaghol+self.hesapagyo+self.hesapakbnk+self.hesapakcns+self.hesapakenr)
        self.toplam_hisse_bakiye = round(self.toplam_hisse_bakiye,2)
        #Hesap bilgilerinde yatırım bakiyesinin gözükmesi için tüm yatırım bilgileri toplar

    def sag_hesap_widgetlari_ekle(self):
        """
        Kullanıcın bakiye borç gibi bilgilerinin gözüktüğü ekranı yaratır. Kullanıcı herhangi bir işlemi yaptıktan sonra hesap bilgilerinin gösterildiği 
        ekrana dönmesi için bu fonksiyon kullanılır.
        """
        self.sag_widgetlari_kaldir()
        self.bilgileri_al()
        self.bakiye = QtWidgets.QLabel()
        self.bakiye.setText("Bakiye: "+str(self.hesapbakiye)+" TL")
        self.bakiye.setFont(QtGui.QFont("arial",20))
        self.borc = QtWidgets.QLabel()
        self.borc.setText("Borç: "+str(self.hesapborc)+" TL")
        self.borc.setFont(QtGui.QFont("arial",20))
        self.doviz = QtWidgets.QLabel()
        self.doviz.setText("Döviz Bakiye: "+str(self.toplam_doviz_bakiye) + " TL")
        self.doviz.setFont(QtGui.QFont("arial",20))
        self.yatirim = QtWidgets.QLabel()
        self.yatirim.setText("Yatırım Bakiye: "+str(self.toplam_hisse_bakiye) + " TL")
        self.yatirim.setFont(QtGui.QFont("arial",20))
        self.hata= QtWidgets.QLabel()
        self.hata.setFont(QtGui.QFont("arial",11))
        self.hata.setStyleSheet("color:red;")
        self.bilgibox.addStretch()
        self.bilgibox.addWidget(self.bakiye)
        self.bilgibox.addWidget(self.borc)
        self.bilgibox.addWidget(self.doviz)
        self.bilgibox.addWidget(self.yatirim)
        self.bilgibox.addWidget(self.hata)
        self.bilgibox.addStretch()

    def sayı_mı(self,test):
        #Verilen değerin sadece sayıdan oluşup oluşmadığını kontrol eden fonksiyon
        a=0
        for i in list(test.text()):
            if(i=="-"):
                return 2
            if((i>="0" and i<="9") or i=="."):
                a+=1
            else:
                a=0
        if(a == len(test.text())):
            return 1
        else:
            return 0

    def sag_widgetlari_kaldir(self):
        #Qui'nin sağ tarafında hem hesap bilgileri hemde işlemler gözükmekte.Bu işlemlerle kullanıcının işi bittiğinde yerine başka elemanlar doldurulucağı için sağ layoutu temizler.
        for i in reversed(range(self.bilgibox.count())):
            layoutItem = self.bilgibox.takeAt(i)
            if layoutItem.widget() is not None:
                widgetToRemove = layoutItem.widget()
                widgetToRemove.setParent(None)
                self.bilgibox.removeWidget(widgetToRemove)
        try:
            for i in reversed(range(self.plaka_h_box.count())):
                    layoutItem = self.plaka_h_box.takeAt(i)
                    if layoutItem.widget() is not None:
                        widgetToRemove = layoutItem.widget()
                        widgetToRemove.setParent(None)
                        self.plaka_h_box.removeWidget(widgetToRemove)
        except:
            pass
            
    def sag_widget_icerigi_olustur(self):
        #Bazı işlemlerin elemanları aynı o yüzden hepsinde kullanılmak için bu fonksiyonda yaratılmakta.
        self.islem_miktar = QtWidgets.QLineEdit()
        self.islem_miktar.setMinimumSize(280,35)
        self.islem_yazisi = QtWidgets.QLabel()
        self.islem_yazisi.setFont(QtGui.QFont("arial",13))
        self.islem_yazisi.setStyleSheet("color:green;")
        self.hata_yazisi = QtWidgets.QLabel()
        self.hata_yazisi.setFont(QtGui.QFont("arial",11))
        self.hata_yazisi.setStyleSheet("color:red;")
        self.butonspacer = QtWidgets.QLabel()
        self.islem_buton.setStyleSheet("background-color:green;color:white;")
        self.islem_buton.setFont(QtGui.QFont("arial",10))
        self.islem_buton.setMinimumSize(300,35)
        self.bilgibox.addStretch()
        self.bilgibox.addWidget(self.islem_yazisi)
        self.bilgibox.addWidget(self.islem_miktar)
        self.bilgibox.addWidget(self.butonspacer)
        self.bilgibox.addWidget(self.islem_buton)
        self.bilgibox.addWidget(self.hata_yazisi)
        self.bilgibox.addStretch()
    
    def hesap_bilgileri(self):
        #sağ layouttaki elemanları silerek yerine hesap bilgilerinin tutulduğu elemanları ekler
        self.sag_widgetlari_kaldir()
        self.sag_hesap_widgetlari_ekle()

    def para_yatir(self):
        """
        Öncelikle sağ layotu boşaltarak yerine bu işlem için kullanılıcak elemanları atar.
        Daha sonra yatırmak istenilen tutarın verilen kurallara uygun olup olmadığı kontrol eder.
        İşlem doğrulanırsa kullanıcının bakiye kısmını güncelleyerek hesaba parayı yatırmış olur.
        """
        self.sag_widgetlari_kaldir()

        def kontrol():
            x = self.sayı_mı(self.islem_miktar)
            if(x==0):
                self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")
            elif(x==2):
                self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**")
            elif(x==1): 
                if(len(self.islem_miktar.text())==0):
                    self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                else:
                    if(self.islem_miktar.text()=="0"):
                        self.hata_yazisi.setText("**Lütfen '0' dışında bir değer giriniz.**")
                    elif(int(self.islem_miktar.text())%10!=0):
                        self.hata_yazisi.setText("**Lütfen 10 ve katları bir değer giriniz.**")
                    elif(int(self.islem_miktar.text())>100000):
                        self.hata_yazisi.setText("**Tek seferde maksimum 100.000TL\nyatırılabilinir.**")
                    else:
                        yatir()

        def yatir():
            yeni_bakiye = self.hesapbakiye + float(self.islem_miktar.text())
            self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(yeni_bakiye,giris_hesapno[0]))
            self.bağlantı.commit()
            
            self.sag_widgetlari_kaldir()
            self.sag_hesap_widgetlari_ekle()

        self.islem_buton = QtWidgets.QPushButton("Para Yatır")
        self.sag_widget_icerigi_olustur()
        self.islem_yazisi.setText("Hesaba yatırmak istediğiniz bakiye:")

        self.islem_buton.clicked.connect(kontrol)

    def para_cek(self):
        """
        Öncelikle hesapta çekilebilinecek bir bakiye olup olmadığını kontrol eder. Eğer yoksa fonksiyona hiç girmez.
        Sonra sağ layotu boşaltarak yerine bu işlem için kullanılıcak elemanları atar.
        Daha sonra çekmek istenilen tutarın verilen kurallara uygun olup olmadığı kontrol eder.
        İşlem doğrulanırsa kullanıcının bakiye kısmını güncelleyerek hesabtan parayı çekmiş olur.
        Eğerki çekmek istenen tutar bakiyede yoksa,işlem gerçekleşmez.
        """
        if(self.hesapbakiye ==0):
            self.sag_widgetlari_kaldir()
            self.sag_hesap_widgetlari_ekle()
            self.hata.setText("**Çekebileceğiniz bir bakiyeniz\nbulunmamaktadır.**")
        else:
            self.sag_widgetlari_kaldir()
            def kontrol():
                x = self.sayı_mı(self.islem_miktar)
                if(x==0):
                    self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")  
                elif(x==2):
                    self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**") 
                elif(x==1): 
                    if(len(self.islem_miktar.text())==0):
                        self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                    else:
                        if(self.islem_miktar.text()=="0"):
                            self.hata_yazisi.setText("**Lütfen '0' dışında bir değer giriniz.**")
                        elif(int(self.islem_miktar.text())%10!=0):
                            self.hata_yazisi.setText("**Lütfen 10 ve katları bir değer giriniz.**")
                        else:
                            cek()

            def cek():
                if(float(self.islem_miktar.text())>self.hesapbakiye):
                    self.hata_yazisi.setText("**Çekmek istediğiniz tutar mevcut\nbakiyeden fazla.**")
                else:
                    yeni_bakiye = self.hesapbakiye - float(self.islem_miktar.text())
                    self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(yeni_bakiye,giris_hesapno[0]))
                    self.bağlantı.commit()
                    
                    self.sag_widgetlari_kaldir()
                    self.sag_hesap_widgetlari_ekle()

            self.islem_buton = QtWidgets.QPushButton("Para Çek")
            self.sag_widget_icerigi_olustur()
            self.islem_yazisi.setText("Hesaptan çekmek istediğiniz bakiye:")

            self.islem_buton.clicked.connect(kontrol)

    def kredi_cek(self):
        """
        Öncelikle sağ layotu boşaltarak yerine bu işlem için kullanılıcak elemanları atar.
        Daha sonra kredi çekmek istenilen tutarın verilen kurallara uygun olup olmadığı kontrol eder.
        Girilen tutarın ödenmek istenen zamana göre faizlendirilerek bu değer borç kısmına yazılır.
        İşlem doğrulanırsa kullanıcının bakiye kısmını güncelleyerek hesaba parayı yatırır ve aynı zamanda borç kısmına da ekleme yapmış olur.
        """
        self.sag_widgetlari_kaldir()

        def kontrol():
            x = self.sayı_mı(self.islem_miktar)
            y = self.sayı_mı(self.ay_miktar)
            if(x==0 and y==0):
                self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")
            elif(x==2 and y==2):
                self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**")
            elif(x==1 and y==1): 
                if(len(self.islem_miktar.text())==0 or len(self.ay_miktar.text())==0):
                    self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                else:
                    if(self.islem_miktar.text()=="0" or self.ay_miktar.text()=="0"):
                        self.hata_yazisi.setText("**Lütfen '0' dışında bir değer giriniz.**")
                    elif(int(self.islem_miktar.text())<10000):
                        self.hata_yazisi.setText("**En az 10.000 TL kredi çekilebilinir.**")
                    elif(int(self.islem_miktar.text())%10!=0):
                        self.hata_yazisi.setText("**Lütfen 10 ve katları bir değer giriniz.**")
                    elif(int(self.ay_miktar.text())>60):
                        self.hata_yazisi.setText("**Kredi maksimum 5 yılda ödenecek\nşekilde çekilebilinir.**")
                    else:
                        cek(int(self.ay_miktar.text()))

        def cek(ay):
            if(ay>=1 and ay<=12):
                faizli_tutar = float(self.islem_miktar.text()) * 1.13
            elif(ay>=13 and ay<=36):
                faizli_tutar = float(self.islem_miktar.text()) * 1.21
            elif(ay>=37 and ay<=60):
                faizli_tutar = float(self.islem_miktar.text()) * 1.34
            faizli_tutar = round(faizli_tutar,3)
            aylik_tutar = round(faizli_tutar/ay,2)
            self.sag_widgetlari_kaldir()

            self.onayla_bilgi = QtWidgets.QLabel()
            self.onayla_bilgi.setFont(QtGui.QFont("arial",13))
            self.onayla_bilgi.setStyleSheet("color:green;")
            self.onayla_bilgi.setText("Hesaba yatacak para: "+str(self.islem_miktar.text())+"\nAylık ödenecek tutar: "+str(aylik_tutar)+"\nToplam ödenecek tutar: "+str(faizli_tutar)+"\n")

            self.onayla_yazi = QtWidgets.QLabel()
            self.onayla_yazi.setText("Onaylıyor Musunuz?")
            self.onayla_yazi.setFont(QtGui.QFont("arial",13))
            self.onayla_yazi.setStyleSheet("color:green;")

            self.onayla_buton = QtWidgets.QPushButton("Onayla")
            self.onayla_buton.setStyleSheet("background-color:green;color:white;")
            self.onayla_buton.setFont(QtGui.QFont("arial",10))
            self.onayla_buton.setMinimumSize(300,35) 

            self.geri_buton = QtWidgets.QPushButton("Geri")
            self.geri_buton.setStyleSheet("background-color:green;color:white;")
            self.geri_buton.setFont(QtGui.QFont("arial",10))
            self.geri_buton.setMinimumSize(300,35) 

            self.bosluk = QtWidgets.QLabel()

            self.bilgibox.addStretch()
            self.bilgibox.addWidget(self.onayla_bilgi)
            self.bilgibox.addWidget(self.onayla_yazi)
            self.bilgibox.addWidget(self.bosluk)
            self.bilgibox.addWidget(self.onayla_buton)
            self.bilgibox.addWidget(self.geri_buton)
            self.bilgibox.addStretch()
            
            def onayla():
                yeni_bakiye = self.hesapbakiye + float(self.islem_miktar.text())
                yeni_borc = self.hesapborc + faizli_tutar
                self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(yeni_bakiye,giris_hesapno[0]))
                self.bağlantı.commit()
                self.cursor.execute("update BANKA_MUSTERILERI set Borc = ? where Hesap_No = ?",(yeni_borc,giris_hesapno[0]))
                self.bağlantı.commit()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()
            def geri():
                self.sag_widgetlari_kaldir()
                self.kredi_cek()

            self.onayla_buton.clicked.connect(onayla)
            self.geri_buton.clicked.connect(geri)

        self.sag_widgetlari_kaldir()

        self.islem_yazisi = QtWidgets.QLabel()
        self.islem_yazisi.setFont(QtGui.QFont("arial",13))
        self.islem_yazisi.setStyleSheet("color:green;")
        self.islem_yazisi.setText("Kredi çekmek istediğiniz bakiye:")

        self.islem_miktar = QtWidgets.QLineEdit()
        self.islem_miktar.setMinimumSize(280,35)

        self.ay_yazisi = QtWidgets.QLabel()
        self.ay_yazisi.setFont(QtGui.QFont("arial",13))
        self.ay_yazisi.setStyleSheet("color:green;")
        self.ay_yazisi.setText("Kaç ayda ödemek istediğinizi giriniz:")

        self.ay_miktar = QtWidgets.QLineEdit()
        self.ay_miktar.setMinimumSize(280,35)

        self.islem_buton = QtWidgets.QPushButton("Kredi Çek")
        self.islem_buton.setStyleSheet("background-color:green;color:white;")
        self.islem_buton.setFont(QtGui.QFont("arial",10))
        self.islem_buton.setMinimumSize(300,35)

        self.hata_yazisi = QtWidgets.QLabel()
        self.hata_yazisi.setFont(QtGui.QFont("arial",11))
        self.hata_yazisi.setStyleSheet("color:red;")

        self.kredi_bilgilendirme = QtWidgets.QLabel()
        self.kredi_bilgilendirme.setFont(QtGui.QFont("arial",12))
        self.kredi_bilgilendirme.setStyleSheet("color:green;")
        self.kredi_bilgilendirme.setText("\nKredi faiz oranları:\n1-12 ay ~~ %1.13\n13-36 ay ~~ %1.21\n37-60 ay ~~ %1.34")

        self.butonspacer = QtWidgets.QLabel()
        self.butonspacer1 = QtWidgets.QLabel()

        self.bilgibox.addStretch()   
        self.bilgibox.addWidget(self.islem_yazisi)
        self.bilgibox.addWidget(self.islem_miktar)
        self.bilgibox.addWidget(self.butonspacer1)
        self.bilgibox.addWidget(self.ay_yazisi)
        self.bilgibox.addWidget(self.ay_miktar)
        self.bilgibox.addWidget(self.butonspacer)
        self.bilgibox.addWidget(self.islem_buton)
        self.bilgibox.addWidget(self.hata_yazisi)
        self.bilgibox.addWidget(self.kredi_bilgilendirme)
        self.bilgibox.addStretch()
            
        self.islem_buton.clicked.connect(kontrol)

    def borc_ode(self):
        """
        Öncelikle hesapta borcun olup olmadığını kontrol eder. Eğer yoksa fonksiyona hiç girmez.
        Sonra sağ layotu boşaltarak yerine bu işlem için kullanılıcak elemanları atar.
        Daha sonra ödenmek istenilen tutarın verilen kurallara uygun olup olmadığı kontrol eder.
        İşlem doğrulanırsa kullanıcının borç kısmını güncelleyerek ödenilen tutar kadar borcu azaltmış olur.
        Bu fonksiyonda ödenmek istenen tutarın, borcun tamamına eşit olup olmadığı sorularak kontrol edilir ona göre işlem yapılır.
        Eğerki ödenmek istenen tutar bakiyede yoksa ödeme işlemi gerçekleşmez.
        """
        if(self.hesapborc==0):
            self.sag_widgetlari_kaldir()
            self.sag_hesap_widgetlari_ekle()
            self.hata.setText("\n**Borcunuz bulunmamakta.**")
        else:
            self.sag_widgetlari_kaldir()

            def kontrol():
                x = self.sayı_mı(self.islem_miktar)
                if(x==0):
                    self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")
                elif(x==2):
                    self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**")
                elif(x==1): 
                    if(len(self.islem_miktar.text())==0):
                        self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                    elif(self.islem_miktar.text()=="0"):
                        self.hata_yazisi.setText("**Lütfen 0'dan farklı bir değer giriniz.**")
                    else:
                        if(float(self.islem_miktar.text())> self.hesapborc):
                            self.hata_yazisi.setText("**Ödemek istediğiniz tutar mevcut\nborçtan fazladır**")
                        else:
                            ode()

            def ode():
                yeni_borc = self.hesapborc - float(self.islem_miktar.text())
                yeni_bakiye = self.hesapbakiye - float(self.islem_miktar.text())
                self.cursor.execute("update BANKA_MUSTERILERI set Borc = ? where Hesap_No = ?",(yeni_borc,giris_hesapno[0]))
                self.bağlantı.commit()
                self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(yeni_bakiye,giris_hesapno[0]))
                self.bağlantı.commit()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()

            def hepsini_ode():
                yeni_borc = 0
                yeni_bakiye = self.hesapbakiye - self.hesapborc
                self.cursor.execute("update BANKA_MUSTERILERI set Borc = ? where Hesap_No = ?",(yeni_borc,giris_hesapno[0]))
                self.bağlantı.commit()
                self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(yeni_bakiye,giris_hesapno[0]))
                self.bağlantı.commit()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()

            def borcun_hepsini_odeme_kontrol():
                if(self.hesapbakiye<self.hesapborc):
                    self.hata_yazisi.setText("**Ödemek istediğiniz tutar hesap bakiyenizde\nbulunan tutardan yüksektir**")
                else:
                    hepsini_ode()

            def odeme_ekran_yarat():
                self.sag_widgetlari_kaldir()
                self.islem_buton = QtWidgets.QPushButton("Borç Öde")
                self.sag_widget_icerigi_olustur()
                self.islem_yazisi.setText("Ödemek istediğiniz bakiye:")
                self.islem_buton.clicked.connect(kontrol)

            self.toplam_borc = QtWidgets.QLabel()
            self.toplam_borc.setText("Hesap Bakiye: "+str(self.hesapbakiye)+"\nToplam borç: "+str(self.hesapborc)+"\n")
            self.toplam_borc.setFont(QtGui.QFont("arial",13))
            self.toplam_borc.setStyleSheet("color:green;")
            self.borcun_hepsi = QtWidgets.QPushButton("Borcun Hepsini Öde")
            self.borcun_hepsi.setStyleSheet("background-color:green;color:white;")
            self.borcun_hepsi.setFont(QtGui.QFont("arial",10))
            self.borcun_hepsi.setMinimumSize(300,35)
            self.borcun_belirli_miktari = QtWidgets.QPushButton("Borcun Belirli Miktarını Öde")
            self.borcun_belirli_miktari.setStyleSheet("background-color:green;color:white;")
            self.borcun_belirli_miktari.setFont(QtGui.QFont("arial",10))
            self.borcun_belirli_miktari.setMinimumSize(300,35)
            self.hata_yazisi = QtWidgets.QLabel()
            self.hata_yazisi.setFont(QtGui.QFont("arial",11))
            self.hata_yazisi.setStyleSheet("color:red;")

            self.bilgibox.addStretch()
            self.bilgibox.addWidget(self.toplam_borc)
            self.bilgibox.addWidget(self.borcun_hepsi)
            self.bilgibox.addWidget(self.borcun_belirli_miktari)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            self.borcun_belirli_miktari.clicked.connect(odeme_ekran_yarat)
            self.borcun_hepsi.clicked.connect(borcun_hepsini_odeme_kontrol)

    def para_gonder(self):
        """
        Öncelikle veritabanında para gönderilebilecek bir kullanıcı olup olmadığını kontrol eder.Yok ise fonksiyona girmez.
        Sonra sağ layotu boşaltarak yerine bu işlem için kullanılıcak elemanları atar.
        Para gönderilebilinecek hesapları bir tabloda gösterir.
        Bu tablodan bakılarak gönderilecek hesabın hesap numarası ve gönderilmek istenen bakiye bilgisi girilmesi istenir.
        Bu hesap numarasının doğru girilip girilmediği kontrol edilir.
        Daha sonra gönderilmek istenilen tutarın verilen kurallara uygun olup olmadığı kontrol eder.
        İşlem doğrulanırsa veritabanında,gönderen kullanıcının bakiye kısmından parayı azaltarak gönderilen hesabın bakiye kısmına ekleme yapar.
        Eğerki gönderilmek istenen tutar bakiyede yoksa para gönderme işlemi gerçekleşmez.
        """
        self.cursor.execute("select * from BANKA_MUSTERILERI")
        kisiler = self.cursor.fetchall()
        if(len(kisiler)==1):
            self.sag_widgetlari_kaldir()
            self.sag_hesap_widgetlari_ekle()
            self.hata.setText("\n**Para gönderebileceğiniz herhangi\nbir hesap bulunmamakta**")
        else:
            self.sag_widgetlari_kaldir()

            def kontrol():
                x = self.sayı_mı(self.secim_number)
                y = self.sayı_mı(self.secim_para)
                if(x==0 or y==0):
                    self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")
                elif(x==2 or y==2):
                    self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**")
                elif(x==1 or y==1): 
                    if(len(self.secim_number.text())==0 or len(self.secim_para.text())==0):
                        self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                    else:
                        if(len(self.secim_number.text())!=5):
                            self.hata_yazisi.setText("**Lütfen hesap numarası kısmına\n5 haneli bir sayı giriniz.**")
                        elif(self.secim_number.text()=="0" or self.secim_para.text()=="0"):
                            self.hata_yazisi.setText("**Lütfen '0' dışında bir değer giriniz.**")    
                        else:
                            if(int(self.secim_number.text()) in self.kisiler_hesapno):
                                if(self.hesapbakiye<float(self.secim_para.text())):
                                    self.hata_yazisi.setText("**Göndermek istediğiniz miktarda\nbakiye bulunmamakta.**") 
                                else:
                                    gonder()
                            else:
                                self.hata_yazisi.setText("**Girmiş olduğunuz hesap numarası\nbulunmamakta.**") 

            def gonder():
                yeni_bakiye = self.hesapbakiye - float(self.secim_para.text())
                self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(yeni_bakiye,giris_hesapno[0]))
                self.bağlantı.commit()
                self.cursor.execute("select * from BANKA_MUSTERILERI where Hesap_No = ?",(int(self.secim_number.text()),))
                liste = self.cursor.fetchall()
                gonderim_bakiye = float(liste[0][3])
                gonderim_yeni_bakiye = gonderim_bakiye + float(self.secim_para.text())
                gonderim_hesap_no = float(liste[0][5])
                self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(gonderim_yeni_bakiye,gonderim_hesap_no))
                self.bağlantı.commit()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()

            kisiler_isim = list()
            self.kisiler_hesapno = list()
            for i in range(len(kisiler)):
                kisiler_isim.append(kisiler[i][0])
                self.kisiler_hesapno.append(kisiler[i][5])
            kisiler_isim.remove(self.hesapisim)
            self.kisiler_hesapno.remove(giris_hesapno[0])
            self.tablo = QtWidgets.QTableWidget()
            self.tablo.setRowCount(len(kisiler_isim))
            self.tablo.setColumnCount(2)
            for i in range(len(kisiler_isim)):
                self.tablo.setItem(i,0,QTableWidgetItem(kisiler_isim[i]))
                self.tablo.setItem(i,1,QTableWidgetItem(str(self.kisiler_hesapno[i])))
            columns = ['İsim', 'Hesap No']
            self.tablo.setHorizontalHeaderLabels(columns)
            self.secim = QtWidgets.QLabel()
            self.secim.setText("\nPara göndermek istediginiz hesap\nnumarasını giriniz:")
            self.secim.setFont(QtGui.QFont("arial",13))
            self.secim.setStyleSheet("color:green;")
            self.secim_number = QtWidgets.QLineEdit()
            self.secim_number.setMinimumSize(280,35)
            self.secim_buton = QtWidgets.QPushButton("Para Gönder")
            self.secim_buton.setStyleSheet("background-color:green;color:white;")
            self.secim_buton.setFont(QtGui.QFont("arial",10))
            self.secim_buton.setMinimumSize(300,35)
            self.hata_yazisi = QtWidgets.QLabel()
            self.hata_yazisi.setFont(QtGui.QFont("arial",11))
            self.hata_yazisi.setStyleSheet("color:red;")

            self.secim_yazisi = QtWidgets.QLabel()
            self.secim_yazisi.setText("\nGöndermek istediğiniz parayı giriniz:")
            self.secim_yazisi.setFont(QtGui.QFont("arial",13))
            self.secim_yazisi.setStyleSheet("color:green;")
            self.secim_para = QtWidgets.QLineEdit()
            self.secim_para.setMinimumSize(280,35)

            self.bilgibox.addStretch()
            self.bilgibox.addWidget(self.tablo)
            self.bilgibox.addWidget(self.secim)
            self.bilgibox.addWidget(self.secim_number)
            self.bilgibox.addWidget(self.secim_yazisi)
            self.bilgibox.addWidget(self.secim_para)
            self.bilgibox.addWidget(self.secim_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            self.secim_buton.clicked.connect(kontrol)

    def doviz_islem(self):
        """
        Öncelikle internetten çekilen döviz bilgilerinin bir tabloya yazılması sağlanır.
        Bu tablodan seçilecek döviz ile ne kadarlık işlem yapılmak istendiği sorulur.
        Bu girilen değerlerin kurallara uyup uymadığı kontrol edilir.
        İşlem doğrulanırsa veritabanında kişinin bakiyesinden düşerek,alınan döviz kuruna göre işlem yapılıp veritabanına yazılır.
        Eğerki almak istenen tutar bakiyede yoksa döviz alma işlemi gerçekleşmez.
        Döviz sata girerken,hesapta dövizin olup olmadığı kontrol edilir. Hesapta hiç döviz yoksa satış işlemine girmez.
        """
        def doviz_al_kontrol():
            x = self.sayı_mı(self.secim_number)
            y = self.sayı_mı(self.secim_para)
            if(x==0 or y==0):
                self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")
            elif(x==2 or y==2):
                self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**")
            elif(x==1 and y==1): 
                if(len(self.secim_number.text())==0 or len(self.secim_para.text())==0):
                    self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                else:
                    if(self.secim_number.text()=="0" or self.secim_para.text()=="0"):
                        self.hata_yazisi.setText("**Lütfen '0' dışında bir değer giriniz.**")
                    elif(int(self.secim_number.text())>0 and int(self.secim_number.text())<11):
                        self.hata_yazisi.setText("")
                        doviz_al_islemi_karsilastir()
                    else:
                        self.hata_yazisi.setText("**Lütfen belirtilen değerler arasında bir\nsayı giriniz**")

        def doviz_sat_kontrol():
            x = self.sayı_mı(self.secim_number)
            y = self.sayı_mı(self.secim_para)
            if(x==0 and y==0):
                self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")
            elif(x==2 and y==2):
                self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**")
            elif(x==1 and y==1): 
                if(len(self.secim_number.text())==0 or len(self.secim_para.text())==0):
                    self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                else:
                    if(self.secim_number.text()=="0" or self.secim_para.text()=="0"):
                        self.hata_yazisi.setText("**Lütfen '0' dışında bir değer giriniz.**")
                    elif(int(self.secim_number.text())>0 and int(self.secim_number.text())<11):
                        self.hata_yazisi.setText("")
                        doviz_sat_islemi_karsilastir()
                    else:
                        self.hata_yazisi.setText("**Lütfen belirtilen değerler arasında bir\nsayı giriniz**")

        def doviz_al_islemi_karsilastir():
            if(self.secim_number.text()=="1"):
                toplam = dolar_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapdolar+=toplam
                    self.cursor.execute("update DOVIZ set Dolar = ? where Hesap_No = ?",(self.hesapdolar,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="2"):
                toplam = euro_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapeuro+=toplam
                    self.cursor.execute("update DOVIZ set Euro = ? where Hesap_No = ?",(self.hesapeuro,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="3"):
                toplam = sterlin_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapsterlin+=toplam
                    self.cursor.execute("update DOVIZ set Sterlin = ? where Hesap_No = ?",(self.hesapsterlin,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="4"):
                toplam = isvicre_frangi_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapisvicrefrangi+=toplam
                    self.cursor.execute("update DOVIZ set Isvicre_Frangi = ? where Hesap_No = ?",(self.hesapisvicrefrangi,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="5"):
                toplam = kanada_dolari_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapkanadadolari+=toplam
                    self.cursor.execute("update DOVIZ set Kanada_Dolari = ? where Hesap_No = ?",(self.hesapkanadadolari,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="6"):
                toplam = rus_rublesi_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesaprusrublesi+=toplam
                    self.cursor.execute("update DOVIZ set Rus_Rublesi = ? where Hesap_No = ?",(self.hesaprusrublesi,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="7"):
                toplam = isvec_kronu_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapisveckronu+=toplam
                    self.cursor.execute("update DOVIZ set Isvec_Kronu = ? where Hesap_No = ?",(self.hesapisveckronu,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="8"):
                toplam = japon_yeni_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapjaponyeni+=toplam
                    self.cursor.execute("update DOVIZ set Japon_Yeni = ? where Hesap_No = ?",(self.hesapjaponyeni,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="9"):
                toplam = kuveyt_dinari_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapkuveytdinari+=toplam
                    self.cursor.execute("update DOVIZ set Kuveyt_Dinari = ? where Hesap_No = ?",(self.hesapkuveytdinari,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="10"):
                toplam = cin_yuani_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapcinyuani+=toplam
                    self.cursor.execute("update DOVIZ set Cin_Yuani = ? where Hesap_No = ?",(self.hesapcinyuani,giris_hesapno[0]))
                    self.bağlantı.commit()
            else:
                pass
            if(x==1):
                ana_parayi_degis()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()

        def doviz_sat_islemi_karsilastir():
            x=0
            if(self.secim_number.text()=="1"):
                if(float(self.secim_para.text())>float(self.hesapdolar)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\ndöviziniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapdolar-=float(self.secim_para.text())
                    self.cursor.execute("update DOVIZ set Dolar = ? where Hesap_No = ?",(self.hesapdolar,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="2"):
                if(float(self.secim_para.text())>float(self.hesapeuro)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\ndöviziniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapeuro-=float(self.secim_para.text())
                    self.cursor.execute("update DOVIZ set Euro = ? where Hesap_No = ?",(self.hesapeuro,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="3"):
                if(float(self.secim_para.text())>float(self.hesapsterlin)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\ndöviziniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapsterlin-=float(self.secim_para.text())
                    self.cursor.execute("update DOVIZ set Sterlin = ? where Hesap_No = ?",(self.hesapsterlin,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="4"):
                if(float(self.secim_para.text())>float(self.hesapisvicrefrangi)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\ndöviziniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapisvicrefrangi-=float(self.secim_para.text())
                    self.cursor.execute("update DOVIZ set Isvicre_Frangi = ? where Hesap_No = ?",(self.hesapisvicrefrangi,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="5"):
                if(float(self.secim_para.text())>float(self.hesapkanadadolari)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\ndöviziniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapkanadadolari-=float(self.secim_para.text())
                    self.cursor.execute("update DOVIZ set Kanada_Dolari = ? where Hesap_No = ?",(self.hesapkanadadolari,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="6"):
                if(float(self.secim_para.text())>float(self.hesaprusrublesi)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\ndöviziniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesaprusrublesi-=float(self.secim_para.text())
                    self.cursor.execute("update DOVIZ set Rus_Rublesi = ? where Hesap_No = ?",(self.hesaprusrublesi,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="7"):
                if(float(self.secim_para.text())>float(self.hesapisveckronu)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\ndöviziniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapisveckronu-=float(self.secim_para.text())
                    self.cursor.execute("update DOVIZ set Isvec_Kronu = ? where Hesap_No = ?",(self.hesapisveckronu,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="8"):
                if(float(self.secim_para.text())>float(self.hesapjaponyeni)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\ndöviziniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapjaponyeni-=float(self.secim_para.text())
                    self.cursor.execute("update DOVIZ set Japon_Yeni = ? where Hesap_No = ?",(self.hesapjaponyeni,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="9"):
                if(float(self.secim_para.text())>float(self.hesapkuveytdinari)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\ndöviziniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapkuveytdinari-=float(self.secim_para.text())
                    self.cursor.execute("update DOVIZ set Kuveyt_Dinari = ? where Hesap_No = ?",(self.hesapkuveytdinari,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="10"):
                if(float(self.secim_para.text())>float(self.hesapcinyuani)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\ndöviziniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapcinyuani-=float(self.secim_para.text())
                    self.cursor.execute("update DOVIZ set Cin_Yuani = ? where Hesap_No = ?",(self.hesapcinyuani,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            else:
                pass
            if(x==1):
                ana_parayi_degis()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()

        def bakiye_yeterlimi(toplam):
            if(self.hesapbakiye<toplam):
                self.hata_yazisi.setText("**Bakiye yeterli değil.**")
            else:
                return 1

        def ana_parayi_degis():
            self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(self.hesapbakiye,giris_hesapno[0]))
            self.bağlantı.commit()

        def doviz_al():
            self.sag_widgetlari_kaldir()
            self.secim_buton = QtWidgets.QPushButton("Döviz Al")
            self.secim_buton.setStyleSheet("background-color:green;color:white;")
            self.secim_buton.setFont(QtGui.QFont("arial",10))
            self.secim_buton.setMinimumSize(300,35)
            self.secim.setText("\nAlmak istediğiniz dövizin numarasını\ngiriniz:")
            self.secim_yazisi.setText("\nNe kadar almak istiyorsunuz:")
            self.hata_yazisi.setText("")
            tablo = QtWidgets.QTableWidget()
            tablo.setRowCount(len(doviz_degerleri_listesi))
            tablo.setColumnCount(2)
            for i in range(len(doviz_degerleri_listesi)):
                tablo.setItem(i,0,QTableWidgetItem(doviz_degerleri_listesi[i][0]))
                tablo.setItem(i,1,QTableWidgetItem(str(doviz_degerleri_listesi[i][1])))
            columns = ['Döviz', 'Birim Fiyat']
            tablo.setHorizontalHeaderLabels(columns)
            self.bilgibox.addStretch()
            self.bilgibox.addWidget(tablo)
            self.bilgibox.addWidget(self.secim)
            self.bilgibox.addWidget(self.secim_number)
            self.bilgibox.addWidget(self.secim_yazisi)
            self.bilgibox.addWidget(self.secim_para)
            self.bilgibox.addWidget(self.secim_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()
            self.secim_buton.clicked.connect(doviz_al_kontrol)
        
        def doviz_sat():
            if(int(self.toplam_doviz_bakiye)<0):
                self.hata_yazisi.setText("**Satacak döviziniz bulunmamaktadır.**")
            else:
                self.sag_widgetlari_kaldir()
                self.secim_buton = QtWidgets.QPushButton("Döviz Sat")
                self.secim_buton.setStyleSheet("background-color:green;color:white;")
                self.secim_buton.setFont(QtGui.QFont("arial",10))
                self.secim_buton.setMinimumSize(300,35)
                self.secim.setText("\nSatmak istediğiniz dövizin numarasını\ngiriniz:")
                self.secim_yazisi.setText("\nNe kadarlık satmak istiyorsunuz:")
                tablo = QtWidgets.QTableWidget()
                tablo.setRowCount(len(doviz_degerleri_listesi))
                tablo.setColumnCount(3)
                for i in range(len(doviz_degerleri_listesi)):
                    tablo.setItem(i,0,QTableWidgetItem(doviz_degerleri_listesi[i][0]))
                    tablo.setItem(i,1,QTableWidgetItem(str(doviz_degerleri_listesi[i][1])))
                self.bilgileri_al()
                tablo.setItem(0,2,QTableWidgetItem(str(round(self.hesapdolar,2))))
                tablo.setItem(1,2,QTableWidgetItem(str(round(self.hesapeuro,2))))
                tablo.setItem(2,2,QTableWidgetItem(str(round(self.hesapsterlin,2))))
                tablo.setItem(3,2,QTableWidgetItem(str(round(self.hesapisvicrefrangi,2))))
                tablo.setItem(4,2,QTableWidgetItem(str(round(self.hesapkanadadolari,2))))
                tablo.setItem(5,2,QTableWidgetItem(str(round(self.hesaprusrublesi,2))))
                tablo.setItem(6,2,QTableWidgetItem(str(round(self.hesapisveckronu,2))))
                tablo.setItem(7,2,QTableWidgetItem(str(round(self.hesapjaponyeni,2))))
                tablo.setItem(8,2,QTableWidgetItem(str(round(self.hesapkuveytdinari,2))))
                tablo.setItem(9,2,QTableWidgetItem(str(round(self.hesapcinyuani,2))))
                columns = ['Döviz', 'Birim Fiyat','Mevcut Bakiye']
                tablo.setHorizontalHeaderLabels(columns)
                self.bilgibox.addStretch()
                self.bilgibox.addWidget(tablo)
                self.bilgibox.addWidget(self.secim)
                self.bilgibox.addWidget(self.secim_number)
                self.bilgibox.addWidget(self.secim_yazisi)
                self.bilgibox.addWidget(self.secim_para)
                self.bilgibox.addWidget(self.secim_buton)
                self.bilgibox.addWidget(self.hata_yazisi)
                self.bilgibox.addStretch()
                self.secim_buton.clicked.connect(doviz_sat_kontrol)

        self.sag_widgetlari_kaldir()  
        self.secim = QtWidgets.QLabel()
        self.secim.setText("\nAlmak istediğiniz dövizin numarasını\ngiriniz:")
        self.secim.setFont(QtGui.QFont("arial",13))
        self.secim.setStyleSheet("color:green;")
        self.secim_number = QtWidgets.QLineEdit()
        self.secim_number.setMinimumSize(280,35)
        self.hata_yazisi = QtWidgets.QLabel()
        self.hata_yazisi.setFont(QtGui.QFont("arial",11))
        self.hata_yazisi.setStyleSheet("color:red;")
        self.secim_yazisi = QtWidgets.QLabel()
        self.secim_yazisi.setFont(QtGui.QFont("arial",13))
        self.secim_yazisi.setStyleSheet("color:green;")
        self.secim_para = QtWidgets.QLineEdit()
        self.secim_para.setMinimumSize(280,35)

        self.doviz_al_buton = QtWidgets.QPushButton("Döviz Al")
        self.doviz_al_buton.setStyleSheet("background-color:green;color:white;")
        self.doviz_al_buton.setFont(QtGui.QFont("arial",10))
        self.doviz_al_buton.setMinimumSize(300,35)
        self.doviz_sat_buton = QtWidgets.QPushButton("Döviz Sat")
        self.doviz_sat_buton.setStyleSheet("background-color:green;color:white;")
        self.doviz_sat_buton.setFont(QtGui.QFont("arial",10))
        self.doviz_sat_buton.setMinimumSize(300,35)
        self.geri_buton = QtWidgets.QPushButton("Geri")
        self.geri_buton.setStyleSheet("background-color:green;color:white;")
        self.geri_buton.setFont(QtGui.QFont("arial",10))
        self.geri_buton.setMinimumSize(300,35)

        self.bilgibox.addStretch()
        self.bilgibox.addWidget(self.doviz_al_buton)
        self.bilgibox.addWidget(self.doviz_sat_buton)
        self.bilgibox.addWidget(self.geri_buton)
        self.bilgibox.addWidget(self.hata_yazisi)
        self.bilgibox.addStretch()

        self.doviz_al_buton.clicked.connect(doviz_al)
        self.doviz_sat_buton.clicked.connect(doviz_sat)
        self.geri_buton.clicked.connect(self.sag_hesap_widgetlari_ekle)

    def yatirim_islem(self):
        """
        Öncelikle internetten çekilen hisse senedi bilgilerinin bir tabloya yazılması sağlanır.
        Bu tablodan seçilecek hisse senedi ile ne kadarlık işlem yapılmak istendiği sorulur.
        Bu girilen değerlerin kurallara uyup uymadığı kontrol edilir.
        İşlem doğrulanırsa veritabanında kişinin bakiyesinden düşerek,alınan hisse senedine göre işlem yapılıp veritabanına yazılır.
        Eğerki almak istenen tutar bakiyede yoksa hisse senedi alma işlemi gerçekleşmez.
        Hisse senedi sata girerken,hesapta hissenin olup olmadığı kontrol edilir. Hesapta hiç hisse senedi yoksa satış işlemine girmez.
        """
        def hisse_al_kontrol():
            x = self.sayı_mı(self.secim_number)
            y = self.sayı_mı(self.secim_para)
            if(x==0 or y==0):
                self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")
            elif(x==2 or y==2):
                self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**")
            elif(x==1 and y==1): 
                if(len(self.secim_number.text())==0 or len(self.secim_para.text())==0):
                    self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                else:
                    if(self.secim_number.text()=="0" or self.secim_para.text()=="0"):
                        self.hata_yazisi.setText("**Lütfen '0' dışında bir değer giriniz.**")
                    elif(int(self.secim_number.text())>0 and int(self.secim_number.text())<11):
                        self.hata_yazisi.setText("")
                        hisse_al_islemi_karsilastir()
                    else:
                        self.hata_yazisi.setText("**Lütfen belirtilen değerler arasında bir\nsayı giriniz**")

        def hisse_sat_kontrol():
            x = self.sayı_mı(self.secim_number)
            y = self.sayı_mı(self.secim_para)
            if(x==0 and y==0):
                self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")
            elif(x==2 and y==2):
                self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**")
            elif(x==1 and y==1): 
                if(len(self.secim_number.text())==0 or len(self.secim_para.text())==0):
                    self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                else:
                    if(self.secim_number.text()=="0" or self.secim_para.text()=="0"):
                        self.hata_yazisi.setText("**Lütfen '0' dışında bir değer giriniz.**")
                    elif(int(self.secim_number.text())>0 and int(self.secim_number.text())<11):
                        self.hata_yazisi.setText("")
                        hisse_sat_islemi_karsilastir()
                    else:
                        self.hata_yazisi.setText("**Lütfen belirtilen değerler arasında bir\nsayı giriniz**")

        def hisse_al_islemi_karsilastir():
            if(self.secim_number.text()=="1"):
                toplam = acsel_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapacsel+=toplam
                    self.cursor.execute("update YATIRIM set ACSEL = ? where Hesap_No = ?",(self.hesapacsel,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="2"):
                toplam = adel_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapadel+=toplam
                    self.cursor.execute("update YATIRIM set ADEL = ? where Hesap_No = ?",(self.hesapadel,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="3"):
                toplam = adese_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapadese+=toplam
                    self.cursor.execute("update YATIRIM set ADESE = ? where Hesap_No = ?",(self.hesapadese,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="4"):
                toplam = aefes_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapaefes+=toplam
                    self.cursor.execute("update YATIRIM set AEFES = ? where Hesap_No = ?",(self.hesapaefes,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="5"):
                toplam = afyon_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapafyon+=toplam
                    self.cursor.execute("update YATIRIM set AFYON = ? where Hesap_No = ?",(self.hesapafyon,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="6"):
                toplam = aghol_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapaghol+=toplam
                    self.cursor.execute("update YATIRIM set AGHOL = ? where Hesap_No = ?",(self.hesapaghol,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="7"):
                toplam = agyo_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapagyo+=toplam
                    self.cursor.execute("update YATIRIM set AGYO = ? where Hesap_No = ?",(self.hesapagyo,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="8"):
                toplam = akbnk_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapakbnk+=toplam
                    self.cursor.execute("update YATIRIM set AKBNK = ? where Hesap_No = ?",(self.hesapakbnk,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="9"):
                toplam = akcns_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapakcns+=toplam
                    self.cursor.execute("update YATIRIM set AKCNS = ? where Hesap_No = ?",(self.hesapakcns,giris_hesapno[0]))
                    self.bağlantı.commit()
            elif(self.secim_number.text()=="10"):
                toplam = akenr_bilgi*int(self.secim_para.text())
                x = bakiye_yeterlimi(toplam)
                if(x==1):
                    self.hesapbakiye-=toplam
                    self.hesapakenr+=toplam
                    self.cursor.execute("update YATIRIM set AKENR = ? where Hesap_No = ?",(self.hesapakenr,giris_hesapno[0]))
                    self.bağlantı.commit()
            else:
                pass
            if(x==1):
                ana_parayi_degis()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()

        def hisse_sat_islemi_karsilastir():
            x=0
            if(self.secim_number.text()=="1"):
                if(float(self.secim_para.text())>float(self.hesapacsel)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\nhisse bakiyeniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapacsel-=float(self.secim_para.text())
                    self.cursor.execute("update YATIRIM set ACSEL = ? where Hesap_No = ?",(self.hesapacsel,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="2"):
                if(float(self.secim_para.text())>float(self.hesapadel)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\nhisse bakiyeniz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapadel-=float(self.secim_para.text())
                    self.cursor.execute("update YATIRIM set ADEL = ? where Hesap_No = ?",(self.hesapadel,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="3"):
                if(float(self.secim_para.text())>float(self.hesapadese)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\nlotunuz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapadese-=float(self.secim_para.text())
                    self.cursor.execute("update YATIRIM set ADESE = ? where Hesap_No = ?",(self.hesapadese,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="4"):
                if(float(self.secim_para.text())>float(self.hesapaefes)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\nlotunuz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapaefes-=float(self.secim_para.text())
                    self.cursor.execute("update YATIRIM set AEFES = ? where Hesap_No = ?",(self.hesapaefes,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="5"):
                if(float(self.secim_para.text())>float(self.hesapafyon)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\nlotunuz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapafyon-=float(self.secim_para.text())
                    self.cursor.execute("update YATIRIM set AFYON = ? where Hesap_No = ?",(self.hesapafyon,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="6"):
                if(float(self.secim_para.text())>float(self.hesapaghol)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\nlotunuz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapaghol-=float(self.secim_para.text())
                    self.cursor.execute("update YATIRIM set AGHOL = ? where Hesap_No = ?",(self.hesapaghol,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="7"):
                if(float(self.secim_para.text())>float(self.hesapagyo)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\nlotunuz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapagyo-=float(self.secim_para.text())
                    self.cursor.execute("update YATIRIM set AGYO = ? where Hesap_No = ?",(self.hesapagyo,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="8"):
                if(float(self.secim_para.text())>float(self.hesapakbnk)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\nlotunuz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapakbnk-=float(self.secim_para.text())
                    self.cursor.execute("update YATIRIM set AKBNK = ? where Hesap_No = ?",(self.hesapakbnk,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="9"):
                if(float(self.secim_para.text())>float(self.hesapakcns)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\nlotunuz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapakcns-=float(self.secim_para.text())
                    self.cursor.execute("update YATIRIM set AKCNS = ? where Hesap_No = ?",(self.hesapakcns,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            elif(self.secim_number.text()=="10"):
                if(float(self.secim_para.text())>float(self.hesapakenr)):
                    self.hata_yazisi.setText("**Bu işlemi yapmak için yeterli\nlotunuz bulunmamaktadır.**")
                else:
                    self.hesapbakiye+=float(self.secim_para.text())
                    self.hesapakenr-=float(self.secim_para.text())
                    self.cursor.execute("update YATIRIM set AKENR = ? where Hesap_No = ?",(self.hesapakenr,giris_hesapno[0]))
                    self.bağlantı.commit()
                    x=1
            else:
                pass
            if(x==1):
                ana_parayi_degis()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()

        def bakiye_yeterlimi(toplam):
            if(self.hesapbakiye<toplam):
                self.hata_yazisi.setText("**Bakiye yeterli değil.**")
            else:
                return 1

        def ana_parayi_degis():
            self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(self.hesapbakiye,giris_hesapno[0]))
            self.bağlantı.commit()

        def hisse_al():
            self.sag_widgetlari_kaldir()
            self.secim_buton = QtWidgets.QPushButton("Hisse Al")
            self.secim_buton.setStyleSheet("background-color:green;color:white;")
            self.secim_buton.setFont(QtGui.QFont("arial",10))
            self.secim_buton.setMinimumSize(300,35)
            self.secim.setText("\nAlmak istediğiniz hissenin numarasını\ngiriniz:")
            self.secim_yazisi.setText("\nKaç lot almak istiyorsunuz:")
            self.hata_yazisi.setText("")
            tablo = QtWidgets.QTableWidget()
            tablo.setRowCount(len(hisse_degerleri_listesi))
            tablo.setColumnCount(2)
            for i in range(len(hisse_degerleri_listesi)):
                tablo.setItem(i,0,QTableWidgetItem(hisse_degerleri_listesi[i][0]))
                tablo.setItem(i,1,QTableWidgetItem(str(hisse_degerleri_listesi[i][1])))
            columns = ['Hisse Kodu', 'Lot Fiyatı']
            tablo.setHorizontalHeaderLabels(columns)
            self.bilgibox.addStretch()
            self.bilgibox.addWidget(tablo)
            self.bilgibox.addWidget(self.secim)
            self.bilgibox.addWidget(self.secim_number)
            self.bilgibox.addWidget(self.secim_yazisi)
            self.bilgibox.addWidget(self.secim_para)
            self.bilgibox.addWidget(self.secim_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()
            self.secim_buton.clicked.connect(hisse_al_kontrol)
        
        def hisse_sat():
            if(int(self.toplam_doviz_bakiye)<0):
                self.hata_yazisi.setText("**Satacak hisseniz bulunmamaktadır.**")
            else:
                self.sag_widgetlari_kaldir()
                self.secim_buton = QtWidgets.QPushButton("Hisse Sat")
                self.secim_buton.setStyleSheet("background-color:green;color:white;")
                self.secim_buton.setFont(QtGui.QFont("arial",10))
                self.secim_buton.setMinimumSize(300,35)
                self.secim.setText("\nSatmak istediğiniz hissenin numarasını\ngiriniz:")
                self.secim_yazisi.setText("\nNe kadarlık satmak istiyorsunuz:")
                tablo = QtWidgets.QTableWidget()
                tablo.setRowCount(len(hisse_degerleri_listesi))
                tablo.setColumnCount(3)
                for i in range(len(hisse_degerleri_listesi)):
                    tablo.setItem(i,0,QTableWidgetItem(hisse_degerleri_listesi[i][0]))
                    tablo.setItem(i,1,QTableWidgetItem(str(hisse_degerleri_listesi[i][1])))
                self.bilgileri_al()
                tablo.setItem(0,2,QTableWidgetItem(str(round(self.hesapacsel,2))))
                tablo.setItem(1,2,QTableWidgetItem(str(round(self.hesapadel,2))))
                tablo.setItem(2,2,QTableWidgetItem(str(round(self.hesapadese,2))))
                tablo.setItem(3,2,QTableWidgetItem(str(round(self.hesapaefes,2))))
                tablo.setItem(4,2,QTableWidgetItem(str(round(self.hesapafyon,2))))
                tablo.setItem(5,2,QTableWidgetItem(str(round(self.hesapaghol,2))))
                tablo.setItem(6,2,QTableWidgetItem(str(round(self.hesapagyo,2))))
                tablo.setItem(7,2,QTableWidgetItem(str(round(self.hesapakbnk,2))))
                tablo.setItem(8,2,QTableWidgetItem(str(round(self.hesapakcns,2))))
                tablo.setItem(9,2,QTableWidgetItem(str(round(self.hesapakenr,2))))
                columns = ['Hisse Kodu', 'Lot Fiyat','Mevcut Bakiye']
                tablo.setHorizontalHeaderLabels(columns)
                self.bilgibox.addStretch()
                self.bilgibox.addWidget(tablo)
                self.bilgibox.addWidget(self.secim)
                self.bilgibox.addWidget(self.secim_number)
                self.bilgibox.addWidget(self.secim_yazisi)
                self.bilgibox.addWidget(self.secim_para)
                self.bilgibox.addWidget(self.secim_buton)
                self.bilgibox.addWidget(self.hata_yazisi)
                self.bilgibox.addStretch()
                self.secim_buton.clicked.connect(hisse_sat_kontrol)

        self.sag_widgetlari_kaldir()  
        self.secim = QtWidgets.QLabel()
        self.secim.setFont(QtGui.QFont("arial",13))
        self.secim.setStyleSheet("color:green;")
        self.secim_number = QtWidgets.QLineEdit()
        self.secim_number.setMinimumSize(280,35)
        self.hata_yazisi = QtWidgets.QLabel()
        self.hata_yazisi.setFont(QtGui.QFont("arial",11))
        self.hata_yazisi.setStyleSheet("color:red;")
        self.secim_yazisi = QtWidgets.QLabel()
        self.secim_yazisi.setFont(QtGui.QFont("arial",13))
        self.secim_yazisi.setStyleSheet("color:green;")
        self.secim_para = QtWidgets.QLineEdit()
        self.secim_para.setMinimumSize(280,35)

        self.hisse_al_buton = QtWidgets.QPushButton("Hisse Al")
        self.hisse_al_buton.setStyleSheet("background-color:green;color:white;")
        self.hisse_al_buton.setFont(QtGui.QFont("arial",10))
        self.hisse_al_buton.setMinimumSize(300,35)
        self.hisse_sat_buton = QtWidgets.QPushButton("Hisse Sat")
        self.hisse_sat_buton.setStyleSheet("background-color:green;color:white;")
        self.hisse_sat_buton.setFont(QtGui.QFont("arial",10))
        self.hisse_sat_buton.setMinimumSize(300,35)
        self.geri_buton = QtWidgets.QPushButton("Geri")
        self.geri_buton.setStyleSheet("background-color:green;color:white;")
        self.geri_buton.setFont(QtGui.QFont("arial",10))
        self.geri_buton.setMinimumSize(300,35)

        self.bilgibox.addStretch()
        self.bilgibox.addWidget(self.hisse_al_buton)
        self.bilgibox.addWidget(self.hisse_sat_buton)
        self.bilgibox.addWidget(self.geri_buton)
        self.bilgibox.addWidget(self.hata_yazisi)
        self.bilgibox.addStretch()

        self.hisse_al_buton.clicked.connect(hisse_al)
        self.hisse_sat_buton.clicked.connect(hisse_sat)
        self.geri_buton.clicked.connect(self.sag_hesap_widgetlari_ekle)

    def fatura_islem(self):
        """
        Öncelikle işlem yapılacak fatura türünün seçmesi istenir.
        Girilen fatura işlemine göre ekrana elemanlar eklenir.
        Örneğin telefona girildiğinde bir telefon numarası ister ve bu girilen değerin kurallara uyup uymadığını kontrol eder.Örneğin; sayılardan oluşması gerekir vb.
        Daha sonra bu telefon numarasına daha önce bir ödeme yapılmamışsa, random olarak bir fatura tutarı atar ve ödenmesini isteyip istemediğini sorar.
        Kullanıcı ödemeye çalışır fakat bakiyesinde o tutar yoksa ödeme işlemi gerçekleşmez.
        Ödeyebilirse veritabanında kullanıcı bakiyesinden fatura tutarı düşer ve ödenen telefon numarası veritabanındaki FATURALAR tablosuna yazılarak tekrar ödenmesinin önüne geçilmiş olur.
        """
        def telefon_sorgulama_ekrani():
            self.sag_widgetlari_kaldir()
            faturano_yazı = QtWidgets.QLabel()
            faturano_yazı.setFont(QtGui.QFont("arial",13))
            faturano_yazı.setStyleSheet("color:green;")
            faturano_yazı.setText("Telefon numarasını giriniz:")
            self.faturano = QtWidgets.QLineEdit()
            self.faturano.setMinimumSize(280,35)
            fatura_ode_buton = QtWidgets.QPushButton("Öde")
            fatura_ode_buton.setStyleSheet("background-color:green;color:white;")
            fatura_ode_buton.setFont(QtGui.QFont("arial",10))
            fatura_ode_buton.setMinimumSize(300,35)
            self.faturatutar = random.randint(50,150)

            self.bilgibox.addStretch()
            self.bilgibox.addWidget(faturano_yazı)
            self.bilgibox.addWidget(self.faturano)
            self.bilgibox.addWidget(fatura_ode_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            fatura_ode_buton.clicked.connect(telefon_karsilastir)

        def kimlik_no_sorgulama_ekrani():
            self.sag_widgetlari_kaldir()
            faturano_yazı = QtWidgets.QLabel()
            faturano_yazı.setFont(QtGui.QFont("arial",13))
            faturano_yazı.setStyleSheet("color:green;")
            faturano_yazı.setText("TC kimlik numarasını giriniz:")
            self.faturano = QtWidgets.QLineEdit()
            self.faturano.setMinimumSize(280,35)
            fatura_ode_buton = QtWidgets.QPushButton("Öde")
            fatura_ode_buton.setStyleSheet("background-color:green;color:white;")
            fatura_ode_buton.setFont(QtGui.QFont("arial",10))
            fatura_ode_buton.setMinimumSize(300,35)
            self.faturatutar = random.randint(80,200)

            self.bilgibox.addStretch()
            self.bilgibox.addWidget(faturano_yazı)
            self.bilgibox.addWidget(self.faturano)
            self.bilgibox.addWidget(fatura_ode_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            fatura_ode_buton.clicked.connect(kimlik_no_karsilastir)

        def fatura_sorgulama_ekrani():
            self.sag_widgetlari_kaldir()
            faturano_yazı = QtWidgets.QLabel()
            faturano_yazı.setFont(QtGui.QFont("arial",13))
            faturano_yazı.setStyleSheet("color:green;")
            faturano_yazı.setText("Fatura numarasını giriniz:\n(Örn;A23212,G21232)\n")
            self.faturano = QtWidgets.QLineEdit()
            self.faturano.setMinimumSize(280,35)
            fatura_ode_buton = QtWidgets.QPushButton("Öde")
            fatura_ode_buton.setStyleSheet("background-color:green;color:white;")
            fatura_ode_buton.setFont(QtGui.QFont("arial",10))
            fatura_ode_buton.setMinimumSize(300,35)
            self.faturatutar = random.randint(50,150)

            self.bilgibox.addStretch()
            self.bilgibox.addWidget(faturano_yazı)
            self.bilgibox.addWidget(self.faturano)
            self.bilgibox.addWidget(fatura_ode_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            fatura_ode_buton.clicked.connect(fatura_karsilastir)
    
        def telefon_karsilastir():
            x = self.sayı_mı(self.faturano)
            if(x==0):
                self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")
            elif(x==2):
                self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**")
            elif(x==1): 
                if(len(self.faturano.text())==0):
                    self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                elif(len(self.faturano.text())!=10):
                    self.hata_yazisi.setText("**Telefon numarası 10 rakamdan oluşmalıdır.**")
                elif(self.faturano.text()[0]=="0"):
                    self.hata_yazisi.setText("**Numarayı başında 0 olmadan yazınız.**")
                else:
                    odenmis_mi()

        def kimlik_no_karsilastir():
            x = self.sayı_mı(self.faturano)
            if(x==0):
                self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")
            elif(x==2):
                self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**")
            elif(x==1): 
                if(len(self.faturano.text())==0):
                    self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                elif(len(self.faturano.text())!=11):
                    self.hata_yazisi.setText("**TCKN 11 rakamdan oluşmalıdır.**")
                else:
                    odenmis_mi()

        def fatura_karsilastir():
            fatura = self.faturano.text()
            a=0
            if(len(self.faturano.text())==0):
                    self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
            elif(len(self.faturano.text())!=6):
                self.hata_yazisi.setText("**Fatura no 6 karakterden oluşmalıdır**")
            for i in range(1,len(fatura)):
                if(fatura[i]>="0" and fatura[i]<="9"):
                    a+=1
                else:
                    self.hata_yazisi.setText("**Lütfen fatura numarasını doğru giriniz.**")
            if(a==(len(fatura)-1)):
                if((fatura[0]>="a" and fatura[0]<="z") or (fatura[0]>="A" and fatura[0]<="Z")):
                    odenmis_mi()

        def odeme_ekrani():
            self.sag_widgetlari_kaldir()
            self.hata_yazisi.setText("")
            faturano = QtWidgets.QLabel()
            faturano.setFont(QtGui.QFont("arial",13))
            faturano.setStyleSheet("color:green;")
            faturano.setText("Fatura numarası = {}\n".format(self.faturano.text().upper())) 
            hesapbakiye = QtWidgets.QLabel()
            hesapbakiye.setFont(QtGui.QFont("arial",13))
            hesapbakiye.setStyleSheet("color:green;")
            hesapbakiye.setText("Hesap Bakiye = {} TL\n".format(self.hesapbakiye)) 
            faturatutar = QtWidgets.QLabel()
            faturatutar.setFont(QtGui.QFont("arial",13))
            faturatutar.setStyleSheet("color:green;")
            faturatutar.setText("Fatura Tutarı = {} TL\n".format(self.faturatutar))
            fatura_ode_buton = QtWidgets.QPushButton("Öde")
            fatura_ode_buton.setStyleSheet("background-color:green;color:white;")
            fatura_ode_buton.setFont(QtGui.QFont("arial",10))
            fatura_ode_buton.setMinimumSize(300,35)
            geri_buton = QtWidgets.QPushButton("Çıkış")
            geri_buton.setStyleSheet("background-color:green;color:white;")
            geri_buton.setFont(QtGui.QFont("arial",10))
            geri_buton.setMinimumSize(300,35)

            self.bilgibox.addStretch()
            self.bilgibox.addWidget(faturano)
            self.bilgibox.addWidget(hesapbakiye)
            self.bilgibox.addWidget(faturatutar)
            self.bilgibox.addWidget(fatura_ode_buton)
            self.bilgibox.addWidget(geri_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            fatura_ode_buton.clicked.connect(öde)
            geri_buton.clicked.connect(self.sag_hesap_widgetlari_ekle)

        def odenmis_mi():
            fatura = self.faturano.text().upper()
            self.cursor.execute("select * from FATURALAR where Fatura_No = ?",(fatura,))
            liste = self.cursor.fetchall()
            if(len(liste)==0):
                odeme_ekrani()
            else:
                self.hata_yazisi.setText("Bu numaraya daha önce ödeme yapılmıştır.")

        def öde():
            if(self.hesapbakiye<self.faturatutar):
                self.hata_yazisi.setText("**Yeterli bakiye bulunmamaktadır.**")
            else:
                fatura = self.faturano.text().upper()
                yeni_bakiye = self.hesapbakiye - self.faturatutar
                self.cursor.execute("insert into FATURALAR VALUES(?)",(fatura,))
                self.bağlantı.commit()
                self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(yeni_bakiye,giris_hesapno[0]))
                self.bağlantı.commit()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()

        self.sag_widgetlari_kaldir()
        self.telefon = QtWidgets.QPushButton("Cep Telefonu")
        self.telefon.setStyleSheet("background-color:green;color:white;")
        self.telefon.setFont(QtGui.QFont("arial",10))
        self.telefon.setMinimumSize(300,35)
        self.internet = QtWidgets.QPushButton("İnternet")
        self.internet.setStyleSheet("background-color:green;color:white;")
        self.internet.setFont(QtGui.QFont("arial",10))
        self.internet.setMinimumSize(300,35)
        self.dogalgaz = QtWidgets.QPushButton("Doğalgaz")
        self.dogalgaz.setStyleSheet("background-color:green;color:white;")
        self.dogalgaz.setFont(QtGui.QFont("arial",10))
        self.dogalgaz.setMinimumSize(300,35)
        self.su = QtWidgets.QPushButton("Su")
        self.su.setStyleSheet("background-color:green;color:white;")
        self.su.setFont(QtGui.QFont("arial",10))
        self.su.setMinimumSize(300,35)
        self.elektrik = QtWidgets.QPushButton("Elektrik")
        self.elektrik.setStyleSheet("background-color:green;color:white;")
        self.elektrik.setFont(QtGui.QFont("arial",10))
        self.elektrik.setMinimumSize(300,35)
        self.geri_buton = QtWidgets.QPushButton("Geri")
        self.geri_buton.setStyleSheet("background-color:green;color:white;")
        self.geri_buton.setFont(QtGui.QFont("arial",10))
        self.geri_buton.setMinimumSize(300,35)
        self.hata_yazisi = QtWidgets.QLabel()
        self.hata_yazisi.setFont(QtGui.QFont("arial",11))
        self.hata_yazisi.setStyleSheet("color:red;")

        self.bilgibox.addStretch()
        self.bilgibox.addWidget(self.telefon)
        self.bilgibox.addWidget(self.internet)
        self.bilgibox.addWidget(self.elektrik)
        self.bilgibox.addWidget(self.dogalgaz)
        self.bilgibox.addWidget(self.su)
        self.bilgibox.addWidget(self.geri_buton)
        self.bilgibox.addWidget(self.hata_yazisi)
        self.bilgibox.addStretch()

        self.telefon.clicked.connect(telefon_sorgulama_ekrani)
        self.internet.clicked.connect(kimlik_no_sorgulama_ekrani)
        self.su.clicked.connect(fatura_sorgulama_ekrani)
        self.elektrik.clicked.connect(fatura_sorgulama_ekrani)
        self.dogalgaz.clicked.connect(fatura_sorgulama_ekrani)
        self.geri_buton.clicked.connect(self.sag_hesap_widgetlari_ekle)

    def sigorta_islem(self):
        """
        Öncelikle işlem yapılacak sigorta türünün seçmesi istenir.
        Girilen sigorta işlemine göre ekrana elemanlar eklenir.
        Örneğin sağlık sigortasına girildiğinde bir TCKN ister ve bu girilen değerin kurallara uyup uymadığını kontrol eder.Örneğin; sayılardan oluşması gerekir vb.
        Daha sonra bu TCKN'na daha önce bir ödeme yapılmamışsa, random olarak bir sigorta tutarı atar ve ödenmesini isteyip istemediğini sorar.
        Kullanıcı ödemeye çalışır fakat bakiyesinde o tutar yoksa ödeme işlemi gerçekleşmez.
        Ödeyebilirse veritabanında kullanıcı bakiyesinden sigorta tutarı düşer ve ödenen TCKN veritabanındaki SIGORTALAR tablosuna yazılarak tekrar ödenmesinin önüne geçilmiş olur.
        """
        def kimlik_no_sorgulama_ekrani():
            self.sag_widgetlari_kaldir()
            sigorta_yazı = QtWidgets.QLabel()
            sigorta_yazı.setFont(QtGui.QFont("arial",13))
            sigorta_yazı.setStyleSheet("color:green;")
            sigorta_yazı.setText("TC kimlik numarasını giriniz:")
            self.sigortano = QtWidgets.QLineEdit()
            self.sigortano.setMinimumSize(280,35)
            sigorta_ode_buton = QtWidgets.QPushButton("Öde")
            sigorta_ode_buton.setStyleSheet("background-color:green;color:white;")
            sigorta_ode_buton.setFont(QtGui.QFont("arial",10))
            sigorta_ode_buton.setMinimumSize(300,35)
            self.sigortatutar = random.randint(500,1000)

            self.bilgibox.addStretch()
            self.bilgibox.addWidget(sigorta_yazı)
            self.bilgibox.addWidget(self.sigortano)
            self.bilgibox.addWidget(sigorta_ode_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            sigorta_ode_buton.clicked.connect(kimlik_no_karsilastir)

        def plaka_sorgulama_ekrani():
            self.sag_widgetlari_kaldir()
            sigorta_yazı = QtWidgets.QLabel()
            sigorta_yazı.setFont(QtGui.QFont("arial",13))
            sigorta_yazı.setStyleSheet("color:green;")
            sigorta_yazı.setText("Plakayı giriniz:\n")
            self.sol = QtWidgets.QLineEdit()
            self.sol.setMinimumSize(0,35)
            self.orta = QtWidgets.QLineEdit()
            self.orta.setMinimumSize(0,35)
            self.sag = QtWidgets.QLineEdit()
            self.sag.setMinimumSize(0,35)
            
            sigorta_ode_buton = QtWidgets.QPushButton("Plaka Sorgula")
            sigorta_ode_buton.setStyleSheet("background-color:green;color:white;")
            sigorta_ode_buton.setFont(QtGui.QFont("arial",10))
            sigorta_ode_buton.setMinimumSize(300,35)
            self.sigortatutar = random.randint(800,2000)

            self.plaka_h_box = QtWidgets.QHBoxLayout()
            self.plaka_h_box.addWidget(self.sol)
            self.plaka_h_box.addWidget(self.orta)
            self.plaka_h_box.addWidget(self.sag)

            self.bilgibox.addStretch()
            self.bilgibox.addWidget(sigorta_yazı)
            self.bilgibox.addLayout(self.plaka_h_box)
            self.bilgibox.addWidget(sigorta_ode_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            sigorta_ode_buton.clicked.connect(plaka_karsilastir)
    
        def adres_sorgulama_ekrani():
            self.sag_widgetlari_kaldir()
            il_yazı = QtWidgets.QLabel()
            il_yazı.setFont(QtGui.QFont("arial",13))
            il_yazı.setStyleSheet("color:green;")
            il_yazı.setText("İl giriniz:")
            ilce_yazı = QtWidgets.QLabel()
            ilce_yazı.setFont(QtGui.QFont("arial",13))
            ilce_yazı.setStyleSheet("color:green;")
            ilce_yazı.setText("\nİlçe giriniz:")
            mahalle_yazı = QtWidgets.QLabel()
            mahalle_yazı.setFont(QtGui.QFont("arial",13))
            mahalle_yazı.setStyleSheet("color:green;")
            mahalle_yazı.setText("\nMahalle giriniz:")

            self.il = QtWidgets.QLineEdit()
            self.il.setMinimumSize(280,35)
            self.ilce = QtWidgets.QLineEdit()
            self.ilce.setMinimumSize(280,35)
            self.mahalle = QtWidgets.QLineEdit()
            self.mahalle.setMinimumSize(280,35)
            sigorta_ode_buton = QtWidgets.QPushButton("Öde")
            sigorta_ode_buton.setStyleSheet("background-color:green;color:white;")
            sigorta_ode_buton.setFont(QtGui.QFont("arial",10))
            sigorta_ode_buton.setMinimumSize(300,35)
            self.sigortatutar = random.randint(1000,2000)

            self.bilgibox.addStretch()
            self.bilgibox.addWidget(il_yazı)
            self.bilgibox.addWidget(self.il)
            self.bilgibox.addWidget(ilce_yazı)
            self.bilgibox.addWidget(self.ilce)
            self.bilgibox.addWidget(mahalle_yazı)
            self.bilgibox.addWidget(self.mahalle)
            self.bilgibox.addWidget(sigorta_ode_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            sigorta_ode_buton.clicked.connect(adres_karsilastir)

        def kimlik_no_karsilastir():
            x = self.sayı_mı(self.sigortano)
            if(x==0):
                self.hata_yazisi.setText("**Lütfen sadece sayı giriniz.**")
            elif(x==2):
                self.hata_yazisi.setText("**Lütfen pozitif bir sayı giriniz.**")
            elif(x==1): 
                if(len(self.sigortano.text())==0):
                    self.hata_yazisi.setText("**Lütfen bir değer giriniz.**")
                elif(len(self.sigortano.text())!=11):
                    self.hata_yazisi.setText("**TCKN 11 rakamdan oluşmalıdır.**")
                else:
                    odenmis_mi()

        def adres_karsilastir():
            a=0
            b=0
            c=0
            if(len(self.il.text())==0 or len(self.ilce.text())==0 or len(self.mahalle.text())==0):
                self.hata_yazisi.setText("**Lütfen tüm boşlukları doldurunuz.**")
            else:
                for i in self.il.text():
                    if(i>="0" and i<="9"):
                        a=0
                        self.hata_yazisi.setText("**İl bölümünde rakam bulunmamalıdır.**")
                    elif(i==" "):
                        self.hata_yazisi.setText("**İl bölümünde boşluk bulunmamalıdır.**")
                    else:
                        a+=1

                for j in self.ilce.text():
                    if(j>="0" and j<="9"):
                        b=0
                        self.hata_yazisi.setText("**İlçe bölümünde rakam bulunmamalıdır.**")
                    elif(j==" "):
                        self.hata_yazisi.setText("**İlçe bölümünde boşluk bulunmamalıdır.**")
                    else:
                        b+=1

                for z in self.mahalle.text():
                    if(z>="0" and z<="9"):
                        c=0
                        self.hata_yazisi.setText("**Mahalle bölümünde rakam bulunmamalıdır.**")
                    else:
                        c+=1

                if(a == len(self.il.text()) and b == len(self.ilce.text()) and c == len(self.mahalle.text())):
                    self.adres = str(str(self.il.text())[:3]+"." + str(self.ilce.text())[:3]+"." + str(self.mahalle.text())[:3]+".").upper()    
                    adres_odenmis_mi()
                
        def plaka_karsilastir():
            a=0
            b=0
            c=0
            if(len(self.sol.text())==0 or len(self.orta.text())==0 or len(self.sag.text())==0):
                self.hata_yazisi.setText("**Lütfen tüm boşlukları doldurunuz.**")
            else:
                for i in self.sol.text():
                    if(i>="0" and i<="9"):
                        a+=1
                    else:
                        self.hata_yazisi.setText("**İl kodu rakamlardan oluşmalıdır.**")

                for j in self.orta.text():
                    if(j>="0" and j<="9"):
                        b+=1
                        self.hata_yazisi.setText("**Orta kısım sadece harflerden oluşmalıdır.**")
                    else:
                        pass

                for z in self.sag.text():
                    if(z>="0" and z<="9"):
                        c+=1
                    else:
                        self.hata_yazisi.setText("**Sayı bölümü rakamlardan oluşmalıdır.**")

                        
                if(c == len(self.sag.text()) and (int(self.sag.text())<10 or int(self.sag.text())>9999)):
                    self.hata_yazisi.setText("**Sayı bölümü 10-9999 arasında olmalıdır.**")

                elif(a == len(self.sol.text()) and (int(self.sol.text())<1 or int(self.sol.text())>81)):
                    self.hata_yazisi.setText("**İl kodu 1-81 arasında olmalıdır.**")

                elif(len(self.orta.text())>3):
                    self.hata_yazisi.setText("**Orta kısım maksimum 3 harften oluşmalıdır.**")
                        
                elif(a == len(self.sol.text()) and b == 0 and c == len(self.sag.text())):
                    if(len(self.sol.text())==1):
                        plaka_duzelt = self.sol.text()
                        plaka_duzelt = "0"+ plaka_duzelt
                        self.plaka = str(str(plaka_duzelt) + str(self.orta.text()) + str(self.sag.text())).upper()
                    else:
                        self.plaka = str(str(self.sol.text()) + str(self.orta.text()) + str(self.sag.text())).upper()
                    plaka_odenmis_mi()

        def odeme_ekrani():
            self.sag_widgetlari_kaldir()
            self.hata_yazisi.setText("")
            sigortano = QtWidgets.QLabel()
            sigortano.setFont(QtGui.QFont("arial",13))
            sigortano.setStyleSheet("color:green;")
            sigortano.setText("Sigorta numarası = {}\n".format(self.sigortano.text())) 
            hesapbakiye = QtWidgets.QLabel()
            hesapbakiye.setFont(QtGui.QFont("arial",13))
            hesapbakiye.setStyleSheet("color:green;")
            hesapbakiye.setText("Hesap Bakiye = {} TL\n".format(self.hesapbakiye)) 
            sigortatutar = QtWidgets.QLabel()
            sigortatutar.setFont(QtGui.QFont("arial",13))
            sigortatutar.setStyleSheet("color:green;")
            sigortatutar.setText("Sigorta Tutarı = {} TL\n".format(self.sigortatutar))
            sigorta_ode_buton = QtWidgets.QPushButton("Öde")
            sigorta_ode_buton.setStyleSheet("background-color:green;color:white;")
            sigorta_ode_buton.setFont(QtGui.QFont("arial",10))
            sigorta_ode_buton.setMinimumSize(300,35)
            geri_buton = QtWidgets.QPushButton("Çıkış")
            geri_buton.setStyleSheet("background-color:green;color:white;")
            geri_buton.setFont(QtGui.QFont("arial",10))
            geri_buton.setMinimumSize(300,35)

            self.bilgibox.addStretch()
            self.bilgibox.addWidget(sigortano)
            self.bilgibox.addWidget(hesapbakiye)
            self.bilgibox.addWidget(sigortatutar)
            self.bilgibox.addWidget(sigorta_ode_buton)
            self.bilgibox.addWidget(geri_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            sigorta_ode_buton.clicked.connect(öde)
            geri_buton.clicked.connect(self.sag_hesap_widgetlari_ekle)

        def plaka_odeme_ekrani():
            self.sag_widgetlari_kaldir()
            self.hata_yazisi.setText("")
            sigortano = QtWidgets.QLabel()
            sigortano.setFont(QtGui.QFont("arial",13))
            sigortano.setStyleSheet("color:green;")
            sigortano.setText("Plaka = {}\n".format(self.plaka)) 
            hesapbakiye = QtWidgets.QLabel()
            hesapbakiye.setFont(QtGui.QFont("arial",13))
            hesapbakiye.setStyleSheet("color:green;")
            hesapbakiye.setText("Hesap Bakiye = {} TL\n".format(self.hesapbakiye)) 
            sigortatutar = QtWidgets.QLabel()
            sigortatutar.setFont(QtGui.QFont("arial",13))
            sigortatutar.setStyleSheet("color:green;")
            sigortatutar.setText("Sigorta Tutarı = {} TL\n".format(self.sigortatutar))
            sigorta_ode_buton = QtWidgets.QPushButton("Öde")
            sigorta_ode_buton.setStyleSheet("background-color:green;color:white;")
            sigorta_ode_buton.setFont(QtGui.QFont("arial",10))
            sigorta_ode_buton.setMinimumSize(300,35)
            geri_buton = QtWidgets.QPushButton("Çıkış")
            geri_buton.setStyleSheet("background-color:green;color:white;")
            geri_buton.setFont(QtGui.QFont("arial",10))
            geri_buton.setMinimumSize(300,35)
            self.bilgibox.addStretch()
            self.bilgibox.addWidget(sigortano)
            self.bilgibox.addWidget(hesapbakiye)
            self.bilgibox.addWidget(sigortatutar)
            self.bilgibox.addWidget(sigorta_ode_buton)
            self.bilgibox.addWidget(geri_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            sigorta_ode_buton.clicked.connect(plaka_öde)
            geri_buton.clicked.connect(self.sag_hesap_widgetlari_ekle)

        def adres_odeme_ekrani():
            self.sag_widgetlari_kaldir()
            self.hata_yazisi.setText("")
            sigortano = QtWidgets.QLabel()
            sigortano.setFont(QtGui.QFont("arial",13))
            sigortano.setStyleSheet("color:green;")
            sigortano.setText("Adres = {}\n".format(self.adres)) 
            hesapbakiye = QtWidgets.QLabel()
            hesapbakiye.setFont(QtGui.QFont("arial",13))
            hesapbakiye.setStyleSheet("color:green;")
            hesapbakiye.setText("Hesap Bakiye = {} TL\n".format(self.hesapbakiye)) 
            sigortatutar = QtWidgets.QLabel()
            sigortatutar.setFont(QtGui.QFont("arial",13))
            sigortatutar.setStyleSheet("color:green;")
            sigortatutar.setText("Sigorta Tutarı = {} TL\n".format(self.sigortatutar))
            sigorta_ode_buton = QtWidgets.QPushButton("Öde")
            sigorta_ode_buton.setStyleSheet("background-color:green;color:white;")
            sigorta_ode_buton.setFont(QtGui.QFont("arial",10))
            sigorta_ode_buton.setMinimumSize(300,35)
            geri_buton = QtWidgets.QPushButton("Çıkış")
            geri_buton.setStyleSheet("background-color:green;color:white;")
            geri_buton.setFont(QtGui.QFont("arial",10))
            geri_buton.setMinimumSize(300,35)
            self.bilgibox.addStretch()
            self.bilgibox.addWidget(sigortano)
            self.bilgibox.addWidget(hesapbakiye)
            self.bilgibox.addWidget(sigortatutar)
            self.bilgibox.addWidget(sigorta_ode_buton)
            self.bilgibox.addWidget(geri_buton)
            self.bilgibox.addWidget(self.hata_yazisi)
            self.bilgibox.addStretch()

            sigorta_ode_buton.clicked.connect(adres_öde)
            geri_buton.clicked.connect(self.sag_hesap_widgetlari_ekle)

        def odenmis_mi():
            sigorta = self.sigortano.text().upper()
            self.cursor.execute("select * from SIGORTALAR where Sigorta_No = ?",(sigorta,))
            liste = self.cursor.fetchall()
            if(len(liste)==0):
                odeme_ekrani()
            else:
                self.hata_yazisi.setText("Bu numaraya daha önce ödeme yapılmıştır.")
        
        def plaka_odenmis_mi():
            self.cursor.execute("select * from SIGORTALAR where Sigorta_No = ?",(self.plaka,))
            liste = self.cursor.fetchall()
            if(len(liste)==0):
                plaka_odeme_ekrani()
            else:
                self.hata_yazisi.setText("Bu plakaya daha önce ödeme yapılmıştır.")

        def adres_odenmis_mi():
            self.cursor.execute("select * from SIGORTALAR where Sigorta_No = ?",(self.adres,))
            liste = self.cursor.fetchall()
            if(len(liste)==0):
                adres_odeme_ekrani()
            else:
                self.hata_yazisi.setText("Bu adrese daha önce ödeme yapılmıştır.")

        def öde():
            if(self.hesapbakiye<self.sigortatutar):
                self.hata_yazisi.setText("**Yeterli bakiye bulunmamaktadır.**")
            else:
                fatura = self.sigortano.text().upper()
                yeni_bakiye = self.hesapbakiye - self.sigortatutar
                self.cursor.execute("insert into SIGORTALAR VALUES(?)",(fatura,))
                self.bağlantı.commit()
                self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(yeni_bakiye,giris_hesapno[0]))
                self.bağlantı.commit()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()
        
        def plaka_öde():
            if(self.hesapbakiye<self.sigortatutar):
                self.hata_yazisi.setText("**Yeterli bakiye bulunmamaktadır.**")
            else:
                yeni_bakiye = self.hesapbakiye - self.sigortatutar
                self.cursor.execute("insert into SIGORTALAR VALUES(?)",(self.plaka,))
                self.bağlantı.commit()
                self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(yeni_bakiye,giris_hesapno[0]))
                self.bağlantı.commit()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()

        def adres_öde():
            if(self.hesapbakiye<self.sigortatutar):
                self.hata_yazisi.setText("**Yeterli bakiye bulunmamaktadır.**")
            else:
                yeni_bakiye = self.hesapbakiye - self.sigortatutar
                self.cursor.execute("insert into SIGORTALAR VALUES(?)",(self.adres,))
                self.bağlantı.commit()
                self.cursor.execute("update BANKA_MUSTERILERI set Bakiye = ? where Hesap_No = ?",(yeni_bakiye,giris_hesapno[0]))
                self.bağlantı.commit()
                self.sag_widgetlari_kaldir()
                self.sag_hesap_widgetlari_ekle()

        self.sag_widgetlari_kaldir()
        self.arac = QtWidgets.QPushButton("Araç Sigortası")
        self.arac.setStyleSheet("background-color:green;color:white;")
        self.arac.setFont(QtGui.QFont("arial",10))
        self.arac.setMinimumSize(300,35)
        self.konut = QtWidgets.QPushButton("Konut sigortası")
        self.konut.setStyleSheet("background-color:green;color:white;")
        self.konut.setFont(QtGui.QFont("arial",10))
        self.konut.setMinimumSize(300,35)
        self.saglik = QtWidgets.QPushButton("Sağlık Sigortası")
        self.saglik.setStyleSheet("background-color:green;color:white;")
        self.saglik.setFont(QtGui.QFont("arial",10))
        self.saglik.setMinimumSize(300,35)
        self.geri_buton = QtWidgets.QPushButton("Geri")
        self.geri_buton.setStyleSheet("background-color:green;color:white;")
        self.geri_buton.setFont(QtGui.QFont("arial",10))
        self.geri_buton.setMinimumSize(300,35)
        self.hata_yazisi = QtWidgets.QLabel()
        self.hata_yazisi.setFont(QtGui.QFont("arial",11))
        self.hata_yazisi.setStyleSheet("color:red;")

        self.bilgibox.addStretch()
        self.bilgibox.addWidget(self.arac)
        self.bilgibox.addWidget(self.konut)
        self.bilgibox.addWidget(self.saglik)
        self.bilgibox.addWidget(self.geri_buton)
        self.bilgibox.addWidget(self.hata_yazisi)
        self.bilgibox.addStretch()

        self.arac.clicked.connect(plaka_sorgulama_ekrani)
        self.saglik.clicked.connect(kimlik_no_sorgulama_ekrani)
        self.konut.clicked.connect(adres_sorgulama_ekrani)
        self.geri_buton.clicked.connect(self.sag_hesap_widgetlari_ekle)

    def cik(self):
        #Ana menü Qui'sini kapatıp açılış sayfasına geri dönüp,o Qui'yi açar
        giris_hesapno.clear()
        self.banka = Acilis_Sayfasi()
        self.close()
        self.banka.show()

    def init_giris_sayfasi(self):
        self.bilgileri_al()

        #Bilgisayarın tarih bilgilerinin alınması
        şuan = datetime.now()
        saat = şuan.hour
        dakika = şuan.minute
        gün = datetime.strftime(datetime.now(),"%D\n%A\n")
        if(len(str(dakika))==1):
            dakika = "0" + str(dakika)
        if(len(str(saat))==1):
            saat = "0"+str(saat)
        gün = gün +str(saat)+":"+str(dakika) 

        #Qui'nin elemanlarının yaratılması ve özelliklerinin atanması
        self.tarih = QtWidgets.QLabel()
        self.tarih.setText(gün)
        self.tarih.setFont(QtGui.QFont("arial",13))
        self.tarih.setStyleSheet("color:green")

        self.hesap_bilgileri_buton = QtWidgets.QPushButton("Hesap Bilgileri")
        self.hesap_bilgileri_buton.setStyleSheet("background-color:green;color:white;")
        self.hesap_bilgileri_buton.setFont(QtGui.QFont("arial",10))
        self.hesap_bilgileri_buton.setMinimumSize(300,35)

        self.para_yatirma_buton = QtWidgets.QPushButton("Para Yatır")
        self.para_yatirma_buton.setStyleSheet("background-color:green;color:white;")
        self.para_yatirma_buton.setFont(QtGui.QFont("arial",10))
        self.para_yatirma_buton.setMinimumSize(300,35)

        self.para_cekme_buton = QtWidgets.QPushButton("Para Çekme")
        self.para_cekme_buton.setStyleSheet("background-color:green;color:white;")
        self.para_cekme_buton.setFont(QtGui.QFont("arial",10))
        self.para_cekme_buton.setMinimumSize(300,35)

        self.kredi_cekme_buton = QtWidgets.QPushButton("Kredi Çekme")
        self.kredi_cekme_buton.setStyleSheet("background-color:green;color:white;")
        self.kredi_cekme_buton.setFont(QtGui.QFont("arial",10))
        self.kredi_cekme_buton.setMinimumSize(300,35)

        self.borc_odeme_buton = QtWidgets.QPushButton("Borç Ödeme")
        self.borc_odeme_buton.setStyleSheet("background-color:green;color:white;")
        self.borc_odeme_buton.setFont(QtGui.QFont("arial",10))
        self.borc_odeme_buton.setMinimumSize(300,35)

        self.para_gonderme_buton = QtWidgets.QPushButton("Para Gönderme")
        self.para_gonderme_buton.setStyleSheet("background-color:green;color:white;")
        self.para_gonderme_buton.setFont(QtGui.QFont("arial",10))
        self.para_gonderme_buton.setMinimumSize(300,35)

        self.doviz_islemleri_buton = QtWidgets.QPushButton("Döviz İşlemleri")
        self.doviz_islemleri_buton.setStyleSheet("background-color:green;color:white;")
        self.doviz_islemleri_buton.setFont(QtGui.QFont("arial",10))
        self.doviz_islemleri_buton.setMinimumSize(300,35)

        self.yatirim_islemleri_buton = QtWidgets.QPushButton("Yatırım İşlemleri")
        self.yatirim_islemleri_buton.setStyleSheet("background-color:green;color:white;")
        self.yatirim_islemleri_buton.setFont(QtGui.QFont("arial",10))
        self.yatirim_islemleri_buton.setMinimumSize(300,35)

        self.fatura_islemleri_buton = QtWidgets.QPushButton("Fatura İşlemleri")
        self.fatura_islemleri_buton.setStyleSheet("background-color:green;color:white;")
        self.fatura_islemleri_buton.setFont(QtGui.QFont("arial",10))
        self.fatura_islemleri_buton.setMinimumSize(300,35)

        self.sigorta_islemleri_buton = QtWidgets.QPushButton("Sigorta İşlemleri")
        self.sigorta_islemleri_buton.setStyleSheet("background-color:green;color:white;")
        self.sigorta_islemleri_buton.setFont(QtGui.QFont("arial",10))
        self.sigorta_islemleri_buton.setMinimumSize(300,35)

        self.cikis_buton = QtWidgets.QPushButton("Çıkış Yap")
        self.cikis_buton.setStyleSheet("background-color:green;color:white;")
        self.cikis_buton.setFont(QtGui.QFont("arial",10))
        self.cikis_buton.setMinimumSize(300,35)

        self.yukarılayoutSpacer = QtWidgets.QSpacerItem(0,5)
        
        self.bakiye = QtWidgets.QLabel()
        self.bakiye.setText("Bakiye: "+str(self.hesapbakiye)+" TL")
        self.bakiye.setFont(QtGui.QFont("arial",20))
        self.borc = QtWidgets.QLabel()
        self.borc.setText("Borç: "+str(self.hesapborc)+" TL")
        self.borc.setFont(QtGui.QFont("arial",20))
        self.doviz = QtWidgets.QLabel()
        self.doviz.setText("Döviz Bakiye: "+str(self.toplam_doviz_bakiye) + " TL")
        self.doviz.setFont(QtGui.QFont("arial",20))
        self.yatirim = QtWidgets.QLabel()
        self.yatirim.setText("Yatırım Bakiye: "+str(self.toplam_hisse_bakiye) + " TL")
        self.yatirim.setFont(QtGui.QFont("arial",20))
        self.hata= QtWidgets.QLabel()
        self.hata.setFont(QtGui.QFont("arial",11))
        self.hata.setStyleSheet("color:red;")

        #Qui penceresindeki elemanların yerlerini ayarlamak için layoutlar kullanılır.
        vboxislemler = QtWidgets.QVBoxLayout()
        vboxislemler.addItem(self.yukarılayoutSpacer)
        vboxislemler.addWidget(self.hesap_bilgileri_buton)
        vboxislemler.addItem(self.yukarılayoutSpacer)
        vboxislemler.addWidget(self.para_yatirma_buton)
        vboxislemler.addItem(self.yukarılayoutSpacer)
        vboxislemler.addWidget(self.para_cekme_buton)
        vboxislemler.addItem(self.yukarılayoutSpacer)
        vboxislemler.addWidget(self.kredi_cekme_buton)
        vboxislemler.addItem(self.yukarılayoutSpacer)
        vboxislemler.addWidget(self.borc_odeme_buton)
        vboxislemler.addItem(self.yukarılayoutSpacer)
        vboxislemler.addWidget(self.para_gonderme_buton)
        vboxislemler.addItem(self.yukarılayoutSpacer)
        vboxislemler.addWidget(self.doviz_islemleri_buton)
        vboxislemler.addItem(self.yukarılayoutSpacer)
        vboxislemler.addWidget(self.yatirim_islemleri_buton)
        vboxislemler.addItem(self.yukarılayoutSpacer)
        vboxislemler.addWidget(self.fatura_islemleri_buton)
        vboxislemler.addItem(self.yukarılayoutSpacer)
        vboxislemler.addWidget(self.sigorta_islemleri_buton)
        vboxislemler.addItem(self.yukarılayoutSpacer)
        vboxislemler.addWidget(self.cikis_buton)
        vboxislemler.addStretch()

        tarihbox =QtWidgets.QVBoxLayout()
        tarihbox.addWidget(self.tarih)
        tarihbox.addStretch()

        self.bilgibox = QtWidgets.QVBoxLayout()
        self.bilgibox.addStretch()
        self.bilgibox.addWidget(self.bakiye)
        self.bilgibox.addWidget(self.borc)
        self.bilgibox.addWidget(self.doviz)
        self.bilgibox.addWidget(self.yatirim)
        self.bilgibox.addWidget(self.hata)
        self.bilgibox.addStretch()

        sagvbox = QtWidgets.QHBoxLayout()
        sagvbox.addStretch()
        sagvbox.addLayout(self.bilgibox)
        sagvbox.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(vboxislemler)
        h_box.addStretch()
        h_box.addLayout(sagvbox)
        h_box.addStretch()
        h_box.addLayout(tarihbox)

        self.setFixedSize(900,500)
        self.setLayout(h_box)
        #Qui'nin ana layoutu ayarlanır
        
        self.hesap_bilgileri_buton.clicked.connect(self.hesap_bilgileri)
        self.para_yatirma_buton.clicked.connect(self.para_yatir)
        self.para_cekme_buton.clicked.connect(self.para_cek)
        self.kredi_cekme_buton.clicked.connect(self.kredi_cek)
        self.borc_odeme_buton.clicked.connect(self.borc_ode)
        self.para_gonderme_buton.clicked.connect(self.para_gonder)
        self.doviz_islemleri_buton.clicked.connect(self.doviz_islem)
        self.yatirim_islemleri_buton.clicked.connect(self.yatirim_islem)
        self.fatura_islemleri_buton.clicked.connect(self.fatura_islem)
        self.sigorta_islemleri_buton.clicked.connect(self.sigorta_islem)
        self.cikis_buton.clicked.connect(self.cik)
        #Buton elemanlarına basıldığında hangi fonksiyonlara gidileceğini belirtir
        
class Giris_Yap_Sayfasi(QtWidgets.QWidget):
    #Giriş yapma işlemine girildiğinde bu sayfanın Qui özelliklerinin tutulduğu class
    def __init__(self):
        super().__init__()
        self.init_giris()
        self.setWindowTitle("Alize Bankası")
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        
    def giris_karsilastir(self,isim,sifre):
        """
        Bu fonksiyon öncelikle giriş yapılabilinecek bir kullanıcı olup olmadığına bakar. Daha sonra giriş yapılmak istenen isimle kayıt edilmiş biri olup olmadığına bakar.
        En sonunda ise giriş yapılmak istenen kullanıcı ile verilen şifre uyuşuyormu diye kontrol eder. Eğer herhangi birinde sıkıntı yoksa giriş yapma işlemi onaylanabilinir.
        """
        try:
            self.bağlantı = sqlite3.connect("database.db")
            self.cursor = self.bağlantı.cursor()
            self.cursor.execute("select * from BANKA_MUSTERILERI")
            liste2 = self.cursor.fetchall()
            if(len(liste2)==0):
                return 0
        except:
            return 0
        try:
            self.bağlantı = sqlite3.connect("database.db")
            self.cursor = self.bağlantı.cursor()
            self.cursor.execute("select * from BANKA_MUSTERILERI where Isim_soyisim = ?",(str(isim).upper(),))
            liste = self.cursor.fetchall()
            if(len(liste)==0):
                return 3
        except:
            return 0
    
        giris_hesapno.append(liste[0][5])
        if(len(liste)==0):
            return 3
        elif(liste[0][1]!=sifre):
            return 2
        else:
            return 1
        
    def giris_basarili(self,):
        #Başarılı bir şekilde giriş yapılırsa bu Qui'yi kapatıp Ana menü Qui'sini açar
        self.giris = Ana_Menu()
        self.close()
        self.giris.show()

    def isim_sorgula(self,isim):
        #Girilen ismin verilen kurallara uyup uymadığına bakılır.Örneğin;sadece harflerde oluşması gerekir,isim ve soyisim arasında boşluk olması gerekir vb.
        a=0
        b=0
        for i in list(self.giris_ismi.text()):
            if ((i >="a" and i<="z") or (i >="A" and i<="Z") or (i == " ")):
                a+=1
            else:
                return "**İsim-Soyisim'de rakam veya özel karakter \nbulunamaz.**"
        for i in list(self.giris_ismi.text()):
            if (i ==" "):
                b+=1
            else:
                pass
        if(b==0):
            return "**Lütfen isim ve soyisminizin arasında boşluk\n olmayacak şekilde yazınız.**"
        if(len(self.giris_ismi.text())<6):
            return"**Lütfen isminizi doğru şekilde giriniz.**"
        return 1

    def sifre_sorgula(self,sifre):
        #Girilen şifrenin verilen kurallara uyup uymadığına bakılır.Örneğin;şifrenin uzunluğu,şifrenin sadece rakam içermesi vb.
        a=0
        if(len(sifre)<4 or len(sifre)>6):
            return "**Şifre 4-6 adet rakamdan oluşmalıdır.**"
        for i in list(sifre):
            if(i>="0" and i<="9"):
                a+=1
            else:
                a=0
        if(a != len(sifre)):
            return "**Şifre sadece rakamlardan oluşmalıdır.**"
        return 1  

    def giris_yap(self):
        """
        Öncelikle verilen şifre ve isim bilgisinin kurallara uyup uymadığını anlamak için sifre_sorgula ve isim_sorgula fonksiyonunlarına gönderilir.
        Eğerki bilgilerin hepsi kurallara uyuyorsa, böyle bir kullanıcının var olup olmadığını anlamak için giris_karsilastir fonksiyona gönderilir.
        Bu fonksiyonların hepsi sorunsuz aşılırsa giris_basarili fonksiyonuna yönlendirilerek Ana Menü sayfası açılır.
        """
        b = self.sifre_sorgula(self.sifre.text())
        if(b==1):
            pass
        else:
            self.hata.setText(b)  

        a = self.isim_sorgula(self.giris_ismi.text())
        if(a==1):
            pass
        else:
            self.hata.setText(a)  

        if(len(self.giris_ismi.text())==0 or len(self.sifre.text())==0):
                self.hata.setText("**Lütfen '*' ile gösterilen yerleri doldurunuz.**")

        if(a==1 and b==1):
            x = self.giris_karsilastir(self.giris_ismi.text(),self.sifre.text())
            if(x==0):
                self.hata.setText("**Henüz hiç bir kayıt yapılmamıştır.**")
            elif(x==1):
                self.hata.setText("**Başarılı.**")
                self.giris_basarili()
            elif(x==2):
                self.hata.setText("**Bu isimle şifre uyuşmamaktadır.**")
            else:
                self.hata.setText("**Bu isimli bir banka müşterisi bulunmamaktadır.**")

    def geri_cik(self):
        #Giriş yap Qui'sini kapatıp açılış sayfasına geri dönüp,o Qui'yi açar
        self.banka = Acilis_Sayfasi()
        self.close()
        self.banka.show()

    def kayita_git(self):
        #Eğerki yeni kayıt yapmak istenirse bu Qui'yi kapatıp Kayıt ol Qui'sini açar
        self.kayit = Kayit_Ol_Sayfasi()
        self.close()
        self.kayit.show()

    def init_giris(self):
        #Bilgisayarın tarih bilgilerinin alınması
        şuan = datetime.now()
        saat = şuan.hour
        dakika = şuan.minute
        gün = datetime.strftime(datetime.now(),"%D\n%A\n")
        if(len(str(dakika))==1):
            dakika = "0" + str(dakika)
        if(len(str(saat))==1):
            saat = "0"+str(saat)
        gün = gün +str(saat)+":"+str(dakika) 

        #Qui'nin elemanlarının yaratılması ve özelliklerinin atanması
        self.tarih = QtWidgets.QLabel()
        self.tarih.setText(gün)
        self.tarih.setFont(QtGui.QFont("arial",15))
        self.tarih.setStyleSheet("color:green")

        self.uyari = QtWidgets.QLabel()
        self.uyari.setText("Lütfen '*' ile gösterilen alanları doldurunuz.\n**Lütfen özel karakter kullanmayınız.")
        self.uyari.setStyleSheet("color:red;")

        self.hata= QtWidgets.QLabel()
        self.hata.setStyleSheet("color:red;")
        self.hata.setFont(QtGui.QFont("arial",10))

        self.giris_ismi = QtWidgets.QLineEdit()
        self.giris_ismi.setMinimumSize(300,30)
        self.giris_ismi_yazi = QtWidgets.QLabel()
        self.giris_ismi_yazi.setText("İsim Soyisim*")
        self.giris_ismi_yazi.setStyleSheet("color:green")
        self.giris_ismi_yazi.setFont(QtGui.QFont("arial",14))
        self.sifre = QtWidgets.QLineEdit()
        self.sifre.setMinimumSize(300,30)
        self.sifre.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sifre_yazi = QtWidgets.QLabel()
        self.sifre_yazi.setText("Şifre*")
        self.sifre_yazi.setStyleSheet("color:green")
        self.sifre_yazi.setFont(QtGui.QFont("arial",14))

        self.giris_buton = QtWidgets.QPushButton("Giriş")
        self.giris_buton.setStyleSheet("background-color:green;color:white;")
        self.giris_buton.setFont(QtGui.QFont("arial",10))
        self.giris_buton.setMinimumSize(80,35)
        
        self.geri_buton = QtWidgets.QPushButton("Geri")
        self.geri_buton.setStyleSheet("background-color:green;color:white;")
        self.geri_buton.setFont(QtGui.QFont("arial",10))
        self.geri_buton.setMinimumSize(80,35)

        self.kayit_buton = QtWidgets.QPushButton("Yeni Kayıt")
        self.kayit_buton.setStyleSheet("background-color:green;color:white;")
        self.kayit_buton.setFont(QtGui.QFont("arial",10))
        self.kayit_buton.setMinimumSize(80,35)

        layoutSpacer = QtWidgets.QSpacerItem(70,0)
        self.bosluk = QtWidgets.QLabel()
        self.bosluk.setText(" ")

        #Qui penceresindeki elemanların yerlerini ayarlamak için layoutlar kullanılır.
        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(self.giris_ismi_yazi)
        v_box.addWidget(self.giris_ismi)
        v_box.addWidget(self.sifre_yazi)
        v_box.addWidget(self.sifre)
        v_box.addStretch()

        hh_box = QtWidgets.QHBoxLayout()
        hh_box.addWidget(self.kayit_buton)
        hh_box.addWidget(self.geri_buton)

        v2_box = QtWidgets.QVBoxLayout()
        v2_box.addWidget(self.tarih)
        v2_box.addStretch()
        
        v3_box = QtWidgets.QVBoxLayout()
        v3_box.addWidget(self.uyari)
        v3_box.addStretch()

        vvv_box = QtWidgets.QVBoxLayout()
        vvv_box.addStretch()
        vvv_box.addLayout(v_box)
        vvv_box.addWidget(self.bosluk)
        vvv_box.addLayout(hh_box)
        vvv_box.addWidget(self.giris_buton)
        vvv_box.addWidget(self.hata)
        vvv_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v3_box)
        h_box.addItem(layoutSpacer)
        h_box.addLayout(vvv_box)
        h_box.addStretch()
        h_box.addLayout(v2_box)

        self.giris_buton.clicked.connect(self.giris_yap)
        self.geri_buton.clicked.connect(self.geri_cik)
        self.kayit_buton.clicked.connect(self.kayita_git)
        #Buton elemanlarına basıldığında hangi fonksiyonlara gidileceğini belirtir

        self.setFixedSize(900,500)
        self.setLayout(h_box)
        #Qui'nin ana layoutu ayarlanır

class Kayit_Ol_Sayfasi(QtWidgets.QWidget):
    #Kayıt etme işlemine girildiğinde bu sayfanın Qui özelliklerinin tutulduğu class
    def __init__(self):
        super().__init__()
        self.init_kayit()
        self.setWindowTitle("Alize Bankası")
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.baglanti_kur()

    def baglanti_kur(self):
        #Veritabanıyla bağlantı kurularak, bu veritabanı içerisinde bilgilerin tutulması için tablolar oluşturulur
        self.bağlantı = sqlite3.connect("database.db")
        self.cursor = self.bağlantı.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS BANKA_MUSTERILERI(Isim_Soyisim TEXT,Sifre TEXT,Telefon TEXT,Bakiye FLOAT,Borc FLOAT,Hesap_No INT)")
        self.bağlantı.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS DOVIZ(Hesap_No INT,Dolar FLOAT,Euro FLOAT,Sterlin FLOAT,Isvicre_Frangi FLOAT,Kanada_Dolari FLOAT,Rus_Rublesi FLOAT,Isvec_Kronu FLOAT,Japon_Yeni FLOAT,Kuveyt_Dinari FLOAT,Cin_Yuani FLOAT)")
        self.bağlantı.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS YATIRIM(Hesap_No INT,ACSEL FLOAT,ADEL FLOAT,ADESE FLOAT,AEFES FLOAT,AFYON FLOAT,AGHOL FLOAT,AGYO FLOAT,AKBNK FLOAT,AKCNS FLOAT,AKENR FLOAT)")
        self.bağlantı.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS FATURALAR(Fatura_No TEXT)")
        self.bağlantı.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS SIGORTALAR(Sigorta_No TEXT)")
        self.bağlantı.commit()

    def veritabani_kayit(self,isim,sifre,telefon):
        #Oluşturulan veritabanındaki tablolara, verilen bilgiler kayıt edilir.
        hesap_no = random.randint(10000,100000)
        self.cursor.execute("insert into BANKA_MUSTERILERI VALUES(?,?,?,?,?,?)",(isim,sifre,telefon,0.0,0.0,hesap_no))
        self.bağlantı.commit()
        self.cursor.execute("insert into DOVIZ VALUES(?,?,?,?,?,?,?,?,?,?,?)",(hesap_no,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0))
        self.bağlantı.commit()
        self.cursor.execute("insert into YATIRIM VALUES(?,?,?,?,?,?,?,?,?,?,?)",(hesap_no,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0))
        self.bağlantı.commit()

    def karsilastir(self,telefon):
        #Kayıt etme işlemi için kullanılan telefon numarasına daha önce kayıt işlemi yapılıp yapılmadığını kontrol eder. Eğer daha önce yapılmışsa yeni kayıt işlemini yapmaz.
        a=0
        self.cursor.execute("select Telefon from BANKA_MUSTERILERI")
        liste = self.cursor.fetchall()
        for i in liste:
            for y in i:
                if(y == telefon):
                    a+=1
        if(a==0):
            return 1
        else:
            return 0

    def isim_sorgula(self,isim):
        #Girilen ismin verilen kurallara uyup uymadığına bakılır.Örneğin;sadece harflerde oluşması gerekir,isim ve soyisim arasında boşluk olması gerekir vb.
        a=0
        b=0
        for i in list(self.kayit_ismi.text()):
            if ((i >="a" and i<="z") or (i >="A" and i<="Z") or (i == " ")):
                a+=1
            else:
                return "**İsim-Soyisim'de rakam veya özel karakter \nbulunamaz.**"
        for i in list(self.kayit_ismi.text()):
            if (i ==" "):
                b+=1
            else:
                pass
        if(b==0):
            return "**Lütfen isim ve soyisminizin arasında boşluk\n olmayacak şekilde yazınız.**"
        if(len(self.kayit_ismi.text())<6):
            return"**Lütfen isminizi doğru şekilde giriniz.**"
        return 1

    def sifre_sorgula(self,sifre,sifre_tekrar):
        #Girilen şifrelerin verilen kurallara uyup uymadığına bakılır.Örneğin;şifrelerin uyuşması,şifrelerin sadece rakam içermesi vb.
        a=0
        b=0
        if(sifre != sifre_tekrar):
            return "**Şifreler Uyuşmamaktadır.**"
        elif(len(sifre)<4 or len(sifre)>6 or len(sifre_tekrar)<4 or len(sifre_tekrar)>6):
            return "**Şifre 4-6 adet rakamdan oluşmalıdır.**"
        for i in list(sifre):
            if(i>="0" and i<="9"):
                a+=1
            else:
                a=0
        if(a != len(sifre)):
            return "**Şifre sadece rakamlardan oluşmalıdır.**"
        for i in list(sifre_tekrar):
            if(i>="0" and i<="9"):
                b+=1
            else:
                b=0
        if(b != len(sifre)):
            return "**Şifre sadece rakamlardan oluşmalıdır.**"
        return 1    
    
    def telefon_sorgula(self,telefon):
        #Girilen telefon numarasının verilen kurallara uyup uymadığına bakılır.Örneğin;10 rakamdan oluşması gerektiği, sadece rakam içermesi gerektiği vb.
        a=0
        b=0
        if(len(telefon)!=0):
            if(list(telefon)[0] == "0"):
                return "**Lütfen telefon numarasının başına '0' koymayınız.**"
            elif(len(telefon)!=10):
                return "**Telefon numarası 10 adet rakamdan oluşmalıdır.**"
        for i in list(telefon):
            if (i ==" "):
                b+=1
            else:
                pass
        if(b!=0):
            return "**Lütfen telefon numarasında boşluk olmayacak\nşekilde yazınız.**"
        for i in list(telefon):
            if(i>="0" and i<="9"):
                a+=1
            else:
                a=0
        if(a != len(telefon)):
            return "**Telefon numarası sadece rakamlardan\noluşmalıdır.**"  
        return 1
        
    def kayit_et(self):
        """
        Öncelikle verilen şifreler,isim ve telefon bilgisinin kurallara uyup uymadığını anlamak için sifre_sorgula,isim_sorgula ve telefon_sorgula fonksiyonunlarına gönderilir.
        Eğerki bilgilerin hepsi kurallara uyuyorsa, devam edilir.
        Bu fonksiyonların hepsi sorunsuz aşılırsa veritabani_kayit fonksiyonuna yönlendirilerek veritabanına bu kullanıcı eklenir.
        """
        c=self.telefon_sorgula(self.telefon.text())
        if(c==1):
            pass
        else:
            self.hata.setText(c)

        b=self.sifre_sorgula(self.sifre.text(),self.sifre_tekrar.text())
        if(b==1):
            pass
        else:
            self.hata.setText(b)

        a = self.isim_sorgula(self.kayit_ismi.text())
        if(a==1):
            pass
        else:
            self.hata.setText(a)

        if(len(self.kayit_ismi.text())==0 or len(self.sifre.text())==0 or len(self.sifre_tekrar.text())==0 or len(self.telefon.text())==0):
            self.hata.setText("**Lütfen '*' ile gösterilen yerleri doldurunuz.**")
             
        if(a==1 and b==1 and c==1):
            islem =self.karsilastir(self.telefon.text())
            if islem ==1:
                self.hata.setText("**Kayıt işleminiz başarıyla gerçekleşmiştir.**")
                self.veritabani_kayit(self.kayit_ismi.text().upper(),self.sifre.text(),self.telefon.text())
            else:
                self.hata.setText("**Bu telefon numarası daha önce kayıt edilmiştir.**\nLütfen tekrar deneyiniz.")   
       
    def geri_cik(self):
        #Kayıt ol Qui'sini kapatıp açılış sayfasına geri dönüp,o Qui'yi açar
        self.banka = Acilis_Sayfasi()
        self.close()
        self.banka.show()

    def init_kayit(self):
        #Bilgisayarın tarih bilgilerinin alınması
        şuan = datetime.now()
        saat = şuan.hour
        dakika = şuan.minute
        gün = datetime.strftime(datetime.now(),"%D\n%A\n")
        if(len(str(dakika))==1):
            dakika = "0" + str(dakika)
        if(len(str(saat))==1):
            saat = "0"+str(saat)
        gün = gün +str(saat)+":"+str(dakika) 

        #Qui'nin elemanlarının yaratılması ve özelliklerinin atanması
        self.tarih = QtWidgets.QLabel()
        self.tarih.setText(gün)
        self.tarih.setFont(QtGui.QFont("arial",15))
        self.tarih.setStyleSheet("color:green")

        self.uyari = QtWidgets.QLabel()
        self.uyari.setText("Lütfen '*' ile gösterilen alanları doldurunuz.\n**Lütfen özel karakter kullanmayınız.\n**Şifre 4-6 adet rakamdan oluşmalıdır.\n**Telefon numaranızı başında '0' olmadan giriniz.")
        self.uyari.setStyleSheet("color:red;")

        self.hata= QtWidgets.QLabel()
        self.hata.setStyleSheet("color:red;")
        self.hata.setFont(QtGui.QFont("arial",10))

        self.kayit_ismi = QtWidgets.QLineEdit()
        self.kayit_ismi.setMinimumSize(300,30)
        self.kayit_ismi_yazi = QtWidgets.QLabel()
        self.kayit_ismi_yazi.setText("İsim Soyisim*")
        self.kayit_ismi_yazi.setStyleSheet("color:green")
        self.kayit_ismi_yazi.setFont(QtGui.QFont("arial",14))
        self.sifre = QtWidgets.QLineEdit()
        self.sifre.setMinimumSize(300,30)
        self.sifre.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sifre_yazi = QtWidgets.QLabel()
        self.sifre_yazi.setText("Şifre*")
        self.sifre_yazi.setStyleSheet("color:green")
        self.sifre_yazi.setFont(QtGui.QFont("arial",14))
        self.sifre_tekrar = QtWidgets.QLineEdit()
        self.sifre_tekrar.setMinimumSize(300,30)
        self.sifre_tekrar.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sifre_tekrar_yazi = QtWidgets.QLabel()
        self.sifre_tekrar_yazi.setText("Şifre Onayla*")
        self.sifre_tekrar_yazi.setStyleSheet("color:green")
        self.sifre_tekrar_yazi.setFont(QtGui.QFont("arial",14))
        self.telefon = QtWidgets.QLineEdit()
        self.telefon.setMinimumSize(300,30)
        self.telefon_yazi = QtWidgets.QLabel()
        self.telefon_yazi.setText("Telefon Numarası*")
        self.telefon_yazi.setStyleSheet("color:green")
        self.telefon_yazi.setFont(QtGui.QFont("arial",14))

        self.kayit_buton = QtWidgets.QPushButton("Kayıt")
        self.kayit_buton.setStyleSheet("background-color:green;color:white;")
        self.kayit_buton.setFont(QtGui.QFont("arial",10))
        self.kayit_buton.setMinimumSize(80,35)
        
        self.geri_buton = QtWidgets.QPushButton("Geri")
        self.geri_buton.setStyleSheet("background-color:green;color:white;")
        self.geri_buton.setFont(QtGui.QFont("arial",10))
        self.geri_buton.setMinimumSize(80,35)

        layoutSpacer = QtWidgets.QSpacerItem(45,0)
        self.bosluk = QtWidgets.QLabel()
        self.bosluk.setText(" ")

        #Qui penceresindeki elemanların yerlerini ayarlamak için layoutlar kullanılır.
        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(self.kayit_ismi_yazi)
        v_box.addWidget(self.kayit_ismi)
        v_box.addWidget(self.sifre_yazi)
        v_box.addWidget(self.sifre)
        v_box.addWidget(self.sifre_tekrar_yazi)
        v_box.addWidget(self.sifre_tekrar)
        v_box.addWidget(self.telefon_yazi)
        v_box.addWidget(self.telefon)
        v_box.addStretch()

        hh_box = QtWidgets.QHBoxLayout()
        hh_box.addWidget(self.kayit_buton)
        hh_box.addWidget(self.geri_buton)

        v2_box = QtWidgets.QVBoxLayout()
        v2_box.addWidget(self.tarih)
        v2_box.addStretch()
        
        v3_box = QtWidgets.QVBoxLayout()
        v3_box.addWidget(self.uyari)
        v3_box.addStretch()

        vvv_box = QtWidgets.QVBoxLayout()
        vvv_box.addStretch()
        vvv_box.addLayout(v_box)
        vvv_box.addWidget(self.bosluk)
        vvv_box.addLayout(hh_box)
        vvv_box.addWidget(self.hata)
        vvv_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v3_box)
        h_box.addItem(layoutSpacer)
        h_box.addLayout(vvv_box)
        h_box.addStretch()
        h_box.addLayout(v2_box)

        self.kayit_buton.clicked.connect(self.kayit_et)
        self.geri_buton.clicked.connect(self.geri_cik)
        #Buton elemanlarına basıldığında hangi fonksiyonlara gidileceğini belirtir

        self.setFixedSize(900,500)
        self.setLayout(h_box)
        #Qui'nin ana layoutu ayarlanır

class Kayit_Sil_Sayfasi(QtWidgets.QWidget):
    #Kayıt silme işlemine girildiğinde bu sayfanın Qui özelliklerinin tutulduğu class
    def __init__(self):
        super().__init__()
        self.init_kayit_sil()
        self.setWindowTitle("Alize Bankası")
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
          
    def geri_cik(self):
        #Kayıt sil Qui'sini kapatıp açılış sayfasına geri dönüp,o Qui'yi açar
        self.banka = Acilis_Sayfasi()
        self.close()
        self.banka.show()

    def kayit_sil_basarili(self):
        self.cursor.execute("delete from BANKA_MUSTERILERI where Hesap_No = ?",(kayit_sil_hesapno[0],))
        self.bağlantı.commit()
        self.cursor.execute("delete from DOVIZ where Hesap_No = ?",(kayit_sil_hesapno[0],))
        self.bağlantı.commit()
        self.cursor.execute("delete from YATIRIM where Hesap_No = ?",(kayit_sil_hesapno[0],))
        self.bağlantı.commit()
        kayit_sil_hesapno.clear()
        return 1
        #kayıt silme işlemi esnasında tüm şartlar sağlanırsa bu fonksiyona gelir ve veritabanından o kullanıcı bilgilerini siler

    def bilgi_karsilastir(self,isim,sifre):
        """
        Bu fonksiyon öncelikle silinebilecek bir kullanıcı olup olmadığına bakar. Daha sonra silmek istenen isimle kayıt edilmiş biri olup olmadığına bakar.
        En sonunda ise silmek istenen kullanıcı ile verilen şifre uyuşuyormu diye kontrol eder. Eğer herhangi birinde sıkıntı yoksa kayıt silme işlemi onaylanabilinir.
        """
        try:
            self.bağlantı = sqlite3.connect("database.db")
            self.cursor = self.bağlantı.cursor()
            self.cursor.execute("select * from BANKA_MUSTERILERI")
            liste2 = self.cursor.fetchall()
            if(len(liste2)==0):
                return 0
        except:
            return 0
        try:
            self.bağlantı = sqlite3.connect("database.db")
            self.cursor = self.bağlantı.cursor()
            self.cursor.execute("select * from BANKA_MUSTERILERI where Isim_soyisim = ?",(str(isim).upper(),))
        except:
            return 0
        liste = self.cursor.fetchall()
        try:
            kayit_sil_hesapno.append(liste[0][5])
        except:
            pass
        if(len(liste)==0):
            return 3
        elif(liste[0][1]!=sifre):
            return 2
        else:
            return self.kayit_sil_basarili()
        
    def isim_sorgula(self,isim):
        #Girilen ismin verilen kurallara uyup uymadığına bakılır.Örneğin;sadece harflerde oluşması gerekir,isim ve soyisim arasında boşluk olması gerekir vb.
        a=0
        b=0
        for i in list(self.giris_ismi.text()):
            if ((i >="a" and i<="z") or (i >="A" and i<="Z") or (i == " ")):
                a+=1
            else:
                return "**İsim-Soyisim'de rakam veya özel karakter \nbulunamaz.**"
        for i in list(self.giris_ismi.text()):
            if (i ==" "):
                b+=1
            else:
                pass
        if(b==0):
            return "**Lütfen isim ve soyisminizin arasında boşluk\n olmayacak şekilde yazınız.**"
        if(len(self.giris_ismi.text())<6):
            return"**Lütfen isminizi doğru şekilde giriniz.**"
        return 1

    def sifre_sorgula(self,sifre,sifre_tekrar):
        #Girilen şifrelerin verilen kurallara uyup uymadığına bakılır.Örneğin;şifrelerin uyuşması,şifrelerin sadece rakam içermesi vb.
        a=0
        b=0
        if(sifre != sifre_tekrar):
            return "**Şifreler Uyuşmamaktadır.**"
        if(len(sifre)<4 or len(sifre)>6):
            return "**Şifre 4-6 adet rakamdan oluşmalıdır.**"
        for i in list(sifre):
            if(i>="0" and i<="9"):
                a+=1
            else:
                a=0
        if(a != len(sifre)):
            return "**Şifre sadece rakamlardan oluşmalıdır.**"
        for i in list(sifre_tekrar):
            if(i>="0" and i<="9"):
                b+=1
            else:
                b=0
        if(b != len(sifre)):
            return "**Şifre sadece rakamlardan oluşmalıdır.**"
        return 1    

    def kayit_sil(self):
        """
        Öncelikle verilen şifreler ve isim bilgisinin kurallara uyup uymadığını anlamak için sifre_sorgula ve isim_sorgula fonksiyonunlarına gönderilir.
        Eğerki bilgilerin hepsi kurallara uyuyorsa, böyle bir kullanıcının var olup olmadığını anlamak için bilgi_karsilastir fonksiyona gönderilir.
        Bu fonksiyonların hepsi sorunsuz aşılırsa kayit_sil_basarili fonksiyonuna yönlendirilerek veritabanından bu kullanıcı silinir.
        """
        b = self.sifre_sorgula(self.sifre.text(),self.sifre_tekrar.text())
        if(b==1):
            pass
        else:
            self.hata.setText(b)  

        a = self.isim_sorgula(self.giris_ismi.text())
        if(a==1):
            pass
        else:
            self.hata.setText(a)

        if(len(self.giris_ismi.text())==0 or len(self.sifre.text())==0 or len(self.sifre_tekrar.text())==0):
                self.hata.setText("**Lütfen '*' ile gösterilen yerleri doldurunuz.**")

        if(a==1 and b==1):
            x = self.bilgi_karsilastir(self.giris_ismi.text(),self.sifre.text())
            if(x==0):
                self.hata.setText("**Henüz hiç bir kayıt yapılmamıştır.**")
            elif(x==1):
                self.hata.setText("**Kayıt silme işlemi başarıyla gerçekleştirilmiştir.**")
            elif(x==2):
                self.hata.setText("**Bu isimle şifre uyuşmamaktadır.**")
            else:
                self.hata.setText("**Bu isimli bir banka müşterisi bulunmamaktadır.**")

    def init_kayit_sil(self):
        #Bilgisayarın tarih bilgilerinin alınması
        şuan = datetime.now()
        saat = şuan.hour
        dakika = şuan.minute
        gün = datetime.strftime(datetime.now(),"%D\n%A\n")
        if(len(str(dakika))==1):
            dakika = "0" + str(dakika)
        if(len(str(saat))==1):
            saat = "0"+str(saat)
        gün = gün +str(saat)+":"+str(dakika) 

        #Qui'nin elemanlarının yaratılması ve özelliklerinin atanması
        self.tarih = QtWidgets.QLabel()
        self.tarih.setText(gün)
        self.tarih.setFont(QtGui.QFont("arial",15))
        self.tarih.setStyleSheet("color:green")

        self.uyari = QtWidgets.QLabel()
        self.uyari.setText("Lütfen '*' ile gösterilen alanları doldurunuz.\n**Lütfen özel karakter kullanmayınız.")
        self.uyari.setStyleSheet("color:red;")

        self.hata= QtWidgets.QLabel()
        self.hata.setStyleSheet("color:red;")
        self.hata.setFont(QtGui.QFont("arial",10))

        self.giris_ismi = QtWidgets.QLineEdit()
        self.giris_ismi.setMinimumSize(300,30)
        self.giris_ismi_yazi = QtWidgets.QLabel()
        self.giris_ismi_yazi.setText("İsim Soyisim*")
        self.giris_ismi_yazi.setStyleSheet("color:green")
        self.giris_ismi_yazi.setFont(QtGui.QFont("arial",14))
        self.sifre = QtWidgets.QLineEdit()
        self.sifre.setMinimumSize(300,30)
        self.sifre.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sifre_yazi = QtWidgets.QLabel()
        self.sifre_yazi.setText("Şifre*")
        self.sifre_yazi.setStyleSheet("color:green")
        self.sifre_yazi.setFont(QtGui.QFont("arial",14))
        self.sifre_tekrar = QtWidgets.QLineEdit()
        self.sifre_tekrar.setMinimumSize(300,30)
        self.sifre_tekrar.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sifre_tekrar_yazi = QtWidgets.QLabel()
        self.sifre_tekrar_yazi.setText("Şifre Onayla*")
        self.sifre_tekrar_yazi.setStyleSheet("color:green")
        self.sifre_tekrar_yazi.setFont(QtGui.QFont("arial",14))
        
        self.geri_buton = QtWidgets.QPushButton("Geri")
        self.geri_buton.setStyleSheet("background-color:green;color:white;")
        self.geri_buton.setFont(QtGui.QFont("arial",10))
        self.geri_buton.setMinimumSize(80,35)

        self.kayit_sil_buton = QtWidgets.QPushButton("Kayıt Sil")
        self.kayit_sil_buton.setStyleSheet("background-color:green;color:white;")
        self.kayit_sil_buton.setFont(QtGui.QFont("arial",10))
        self.kayit_sil_buton.setMinimumSize(80,35)

        layoutSpacer = QtWidgets.QSpacerItem(80,0)
        self.bosluk = QtWidgets.QLabel()
        self.bosluk.setText(" ")

        #Qui penceresindeki elemanların yerlerini ayarlamak için layoutlar kullanılır.
        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(self.giris_ismi_yazi)
        v_box.addWidget(self.giris_ismi)
        v_box.addWidget(self.sifre_yazi)
        v_box.addWidget(self.sifre)
        v_box.addWidget(self.sifre_tekrar_yazi)
        v_box.addWidget(self.sifre_tekrar)
        v_box.addStretch()

        hh_box = QtWidgets.QHBoxLayout()
        hh_box.addWidget(self.kayit_sil_buton)
        hh_box.addWidget(self.geri_buton)

        v2_box = QtWidgets.QVBoxLayout()
        v2_box.addWidget(self.tarih)
        v2_box.addStretch()
        
        v3_box = QtWidgets.QVBoxLayout()
        v3_box.addWidget(self.uyari)
        v3_box.addStretch()

        vvv_box = QtWidgets.QVBoxLayout()
        vvv_box.addStretch()
        vvv_box.addLayout(v_box)
        vvv_box.addWidget(self.bosluk)
        vvv_box.addLayout(hh_box)
        vvv_box.addWidget(self.hata)
        vvv_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v3_box)
        h_box.addItem(layoutSpacer)
        h_box.addLayout(vvv_box)
        h_box.addStretch()
        h_box.addLayout(v2_box)

        self.setFixedSize(900,500)
        self.setLayout(h_box)
        #Qui'nin ana layoutu ayarlanır

        self.kayit_sil_buton.clicked.connect(self.kayit_sil)
        self.geri_buton.clicked.connect(self.geri_cik)
        #Buton elemanlarına basıldığında hangi fonksiyonlara gidileceğini belirtir

class Acilis_Sayfasi(QtWidgets.QWidget):
    #ilk açılan sayfanın Qui özelliklerinin tutulduğu class
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("Alize Bankası'na Hoşgeldiniz...")
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        
    def cikis_yap(self):
        #QUİ'yi kapatıp,programı sonlandırır
        self.close()

    def kayit_sayfasi(self):
        #Açılış Qui'sini kapatıp kayit etme sayfasının Qui'sini açar
        self.kayit_sayfasi1 = Kayit_Ol_Sayfasi()
        self.close()
        self.kayit_sayfasi1.show()

    def giris_sayfasi(self):
        #Açılış Qui'sini kapatıp giriş yapma sayfasının Qui'sini açar
        self.giris_sayfasi1 = Giris_Yap_Sayfasi()
        self.close()
        self.giris_sayfasi1.show()

    def kayit_sil_sayfasi(self):
        #Açılış Qui'sini kapatıp kayit silme sayfasının Qui'sini açar
        self.kayit_sil_sayfasi1 = Kayit_Sil_Sayfasi()
        self.close()
        self.kayit_sil_sayfasi1.show()

    def init_ui(self):
        #Qui elemanlarını yaratıp bu elemanların özelliklerinin atanması
        self.kayit_ol = QtWidgets.QPushButton("Kayıt Ol")
        self.kayit_ol.setStyleSheet("background-color:green;color:white;font:10pt;width:20px")
        self.kayit_ol.setMinimumSize(300,35)
        self.giris_yap = QtWidgets.QPushButton("Giriş Yap")
        self.giris_yap.setStyleSheet("background-color:green;color:white;font:10pt;width:20px")
        self.giris_yap.setMinimumSize(300,35)
        self.kayit_sil = QtWidgets.QPushButton("Kayıt Sil")
        self.kayit_sil.setStyleSheet("background-color:green;color:white;font:10pt;width:20px")
        self.kayit_sil.setMinimumSize(300,35)
        self.çıkış = QtWidgets.QPushButton("Çıkış")
        self.çıkış.setStyleSheet("background-color:green;color:white;font:10pt;width:20px")
        self.çıkış.setMinimumSize(300,35)

        self.bayrak = QtWidgets.QLabel()
        self.bayrak.setMinimumSize(120,69)
        self.bayrak.setStyleSheet("background-image:url(bayrak.png);")

        self.banka_ismi=QtWidgets.QLabel()
        self.banka_ismi.setText("Alize Bankası")
        self.banka_ismi.setStyleSheet("color:green;")
        self.banka_ismi.setFont(QtGui.QFont("arial",45))

        self.isim = QtWidgets.QLabel()
        self.isim.setText("            Ömer Şenol")
        self.isim.setStyleSheet("color:gray")
        self.isim.setFont(QtGui.QFont("arial",7))

        self.dolar_doviz = QtWidgets.QLabel()
        self.dolar_doviz.setText("Dolar: "+ana_sayfa_dolar_bilgi[:4])
        self.dolar_doviz.setFont(QtGui.QFont("arial",15))
        self.dolar_doviz.setStyleSheet("color:green")
        self.euro_doviz = QtWidgets.QLabel()
        self.euro_doviz.setText("Euro: "+ana_sayfa_euro_bilgi[:4])
        self.euro_doviz.setFont(QtGui.QFont("arial",15))
        self.euro_doviz.setStyleSheet("color:green")
        self.sterlin_doviz = QtWidgets.QLabel()
        self.sterlin_doviz.setText("Sterlin: "+ana_sayfa_sterlin_bilgi[:5])
        self.sterlin_doviz.setFont(QtGui.QFont("arial",15))
        self.sterlin_doviz.setStyleSheet("color:green")    
        
        #Bilgisayarın tarih bilgilerinin alınması
        şuan = datetime.now()
        saat = şuan.hour
        dakika = şuan.minute
        if(len(str(dakika))==1):
            dakika = "0" + str(dakika)
        if(len(str(saat))==1):
            saat = "0"+str(saat)
        gün = datetime.strftime(datetime.now(),"%D\n%A\n")
        gün = gün+str(saat)+":"+str(dakika)
               
        self.tarih = QtWidgets.QLabel()
        self.tarih.setText(gün)
        self.tarih.setFont(QtGui.QFont("arial",15))
        self.tarih.setStyleSheet("color:green")

        #Qui penceresindeki elemanların yerlerini ayarlamak için layoutlar kullanılır.
        vv_box = QtWidgets.QVBoxLayout()
        vv_box.addWidget(self.banka_ismi)

        vvv_box = QtWidgets.QVBoxLayout()
        vvv_box.addStretch()
        vvv_box.addWidget(self.giris_yap)
        vvv_box.addWidget(self.kayit_ol)
        vvv_box.addWidget(self.kayit_sil)
        vvv_box.addWidget(self.çıkış)
        vvv_box.addStretch()

        hhh_box =QtWidgets.QHBoxLayout()
        hhh_box.addStretch()
        #Layoutlarda addStretch() methodu, o layoutun üstten veya alttan boşluk bırakılarak hizalanmasını sağlar
        hhh_box.addLayout(vvv_box)
        hhh_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()
        v_box.addLayout(vv_box)
        v_box.addStretch()
        v_box.addLayout(hhh_box)
        v_box.addStretch()

        h_bayrak = QtWidgets.QHBoxLayout()
        h_bayrak.addWidget(self.bayrak)
        h_bayrak.addStretch()

        v_borsa = QtWidgets.QVBoxLayout()
        v_borsa.addWidget(self.dolar_doviz)
        v_borsa.addWidget(self.euro_doviz)
        v_borsa.addWidget(self.sterlin_doviz)

        v2_box = QtWidgets.QVBoxLayout()
        v2_box.addLayout(h_bayrak)
        v2_box.addStretch()
        v2_box.addLayout(v_borsa)
        
        v3_box = QtWidgets.QVBoxLayout()
        v3_box.addWidget(self.tarih)
        v3_box.addStretch()
        v3_box.addWidget(self.isim)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v2_box)
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        h_box.addLayout(v3_box)
        #addLayout() methodu, içine yazılan layoutu diğer bir layoutun içine atar

        self.kayit_ol.clicked.connect(self.kayit_sayfasi)
        self.çıkış.clicked.connect(self.cikis_yap)
        self.giris_yap.clicked.connect(self.giris_sayfasi)
        self.kayit_sil.clicked.connect(self.kayit_sil_sayfasi)
        #Buton elemanlarına basıldığında hangi fonksiyonlara gidileceğini belirtir
        
        self.setLayout(h_box)
        #Qui'nin ana layoutu ayarlanır
        self.setFixedSize(900,500)
        #Qui'nin ekran boyutu ayarlanır
        self.show()

app = QtWidgets.QApplication(sys.argv)
app.setStyle("fusion")
banka = Acilis_Sayfasi()
sys.exit(app.exec_())
#Qui verilen class ile yaratılır