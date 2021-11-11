#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 01:47:52 2021

@author: bcyrnli
"""
import pyotp
from flask import *
from flask_bootstrap import Bootstrap
import qrcode
import base64

app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
Bootstrap(app)
@app.route("/")
def index():
    return "<h1>Herkese Merhaba! Sayfaya giriş için url sonuna /login ekleyin.</h1>"
@app.route("/login/")
def login():
    return render_template("login.html")
@app.route("/login/", methods=["POST"])
def login_form():
    creds = {"username": "test", "password": "admin"}

    username = request.form.get("username")
    password = request.form.get("password")

    if username == creds["username"] and password == creds["password"]:
        return redirect(url_for("login_2fa"))
    else:
        flash("You have supplied invalid login credentials!", "danger")
        return redirect(url_for("login"))

@app.route("/login/2fa/")
def login_2fa():
    """secret = pyotp.random_base32()"""  #rastgele anahtar üretici kod
    
    
    secret = "WYKTISVOGGRIDHTJHQKR4FE34ETR4HZE"
    
    #burası da kodun qr kodunu ve oluşturulan qr kodu png yapmasına yarıyor.
    """
    img = qrcode.make('WYKTISVOGGRIDHTJHQKR4FE34ETR4HZE')
    img.save('qr_code.png')
    im = Image.open("qr_code.png")
    data = io.BytesIO()
    im.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue())
    """
    
    return render_template("login_2fa.html", secret=secret)

@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():
    secret = request.form.get("secret")
    otp = int(request.form.get("otp"))

    if pyotp.TOTP(secret).verify(otp):
        flash("Girilen OTP doğru.", "success")
        return redirect(url_for("login_2fa"))
    else:
        flash("Girilen OTP yanlış.", "danger")
        return redirect(url_for("login_2fa"))
if __name__ == "__main__":
    app.run(debug=True)
