from flask import Flask, render_template, abort, make_response, request, redirect, url_for
from db import sorgula, calistir
import uuid

app = Flask(__name__)

@app.route("/")
def anasayfa():
    kategoriler = sorgula("""
                          SELECT id, ad, gorsel
                          FROM kategoriler
                          WHERE aktif = 1
                          ORDER BY sira
                          """)
    
    for kategori in kategoriler:
        kategori["urunler"] = sorgula("""
                                      SELECT u.id, u.ad, u.aciklama, ub.boy_ad, ub.fiyat
                                      FROM urunler u
                                      JOIN urun_boylari ub ON ub.urun_id = u.id
                                      WHERE u.kategori_id = %s AND u.aktif = 1 AND ub.aktif = 1
                                      ORDER BY u.ad, ub.fiyat
                                      """, (kategori["id"],))
    
    return render_template("tanitim/index.html", kategoriler=kategoriler)

@app.route("/masa/<token>")
def masa_giris(token):
    masa = sorgula(
        "SELECT id, masa_kodu, bolge FROM masalar WHERE qr_token = %s AND aktif = 1",
        (token,), tek=True
    )
    
    if not masa:
        abort(404)
        
    adisyon = sorgula(
        "SELECT id FROM adisyonlar WHERE masa_id = %s AND durum = 'acik'",
        (masa["id"],), tek=True
    )
    
    if not adisyon:
        adisyon_id = calistir(
            "INSERT INTO adisyonlar (masa_id) VALUES (%s)", (masa["id"],)
        )
    else:
        adisyon_id = adisyon["id"]
        
    cihaz_token = request.cookies.get("cihaz_token")
    musteri = None
    if cihaz_token:
        musteri = sorgula(
            "SELECT id, musteri_kodu FROM musteriler WHERE cihaz_token = %s",
            (cihaz_token,), tek=True
        )
        
    return f"Masa: {masa['masa_kodu']} ({masa['bolge']})"

if __name__ == "__main__":
    app.run(debug=True)