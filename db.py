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