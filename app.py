from flask import Flask, render_template, send_file
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Love QR is live ❤️"

@app.route("/love")
def love_page():
    return render_template("love.html")

@app.route("/qr")
def generate_qr():
    qr_url = "http://127.0.0.1:5000/love"

    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_H,
        box_size=12,
        border=4
    )

    qr.add_data(qr_url)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color="red",
        back_color="white"
    ).convert("RGBA")

    logo_path = os.path.join(app.root_path, "static", "heart.png")

    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        qr_w, qr_h = qr_img.size
        logo_size = qr_w // 5
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        pos = ((qr_w - logo_size) // 2, (qr_h - logo_size) // 2)
        qr_img.paste(logo, pos, logo)

    qr_img.save("love_qr.png")
    return send_file("love_qr.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
