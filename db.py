import mysql.connector
from config import DB_CONFIG

def baglanti_al():
    return mysql.connector.connect(**DB_CONFIG)

def sorgula(sql, params=None, tek=False):
    b = baglanti_al()
    c = b.cursor(dictionary=True)
    c.execute(sql, params or ())
    sonuc = c.fetchone() if tek else c.fetchall()
    c.close()
    b.close()
    return sonuc

def calistir(sql, params=None):
    b = baglanti_al()
    c = b.cursor()
    c.execute(sql, params or ())
    b.commit()
    son_id = c.lastrowid
    c.close()
    b.close()
    return son_id

def sonraki_kod():
    son = sorgula(
        "SELECT musteri_kodu FROM musteriler ORDER BY id DESC LIMIT 1",
        tek=True
    )
    
    if not son:
        return "A1"
    
    harf = son["musteri_kodu"][0]
    sayi = int(son["musteri_kodu"][1:])
    
    if sayi < 99:
        return f"{harf}{sayi + 1}"
    return f"{chr(ord(harf) + 1)}1"