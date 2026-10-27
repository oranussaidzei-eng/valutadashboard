from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/history", methods=["POST"])
def history():
    fran_valuta = request.form.get("fran_valuta")
    till_valuta = request.form.get("till_valuta")
    belopp = request.form.get("belopp")

    valutor = ["SEK", "USD", "EUR", "TND", "AFN", "CDF"]

    if fran_valuta not in valutor or till_valuta not in valutor:
        return render_template("error.html", fel="Välj giltiga valutor"), 400

    try:
        belopp = float(belopp)
    except (ValueError, TypeError):
        return render_template("error.html", fel="Ange belopp som ett tal."), 400

    if belopp <= 0:
        return render_template(
            "error.html", fel="Beloppet måste vara större än noll."
        ), 400

    return render_template(
        "history.html", fran_valuta=fran_valuta, till_valuta=till_valuta, belopp=belopp
    )


@app.errorhandler(404)
def saknas(e):
    return render_template("error.html", fel="Sidan finns inte"), 404
