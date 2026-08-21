import secrets
from db import baglanti_al

masalar = [
    ("M1", "Merkür Terası"),
    ("M2", "Merkür Terası"),
    ("M3", "Merkür Terası"),
    ("S1", "Satürn Salonu"),
    ("S2", "Satürn Salonu"),
    ("S3", "Satürn Salonu"),
    ("V1", "Venüs Köşesi"),
    ("V2", "Venüs Köşesi"),
]

b = baglanti_al()
c = b.cursor()

for kod, bolge in masalar:
    token = secrets.token_hex(16)
    c.execute(
        "INSERT INTO masalar (masa_kodu, bolge, qr_token) VALUES (%s, %s, %s)",
        (kod, bolge, token)
    )
    print(f"{kod} -> http://127.0.0.1:5000/masa/{token}")
    
b.commit()
c.close()
b.close()