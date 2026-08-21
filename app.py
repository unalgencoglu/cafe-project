from flask import Flask, render_template
from db import sorgula

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

if __name__ == "__main__":
    app.run(debug=True)