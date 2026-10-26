from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/history", methods=["POST"])
def history():
    from_currency = request.form.get("from_currency")
    to_currency = request.form.get("to_currency")
    amount = request.form.get("amount")

    return render_template(
        "history.html",
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
    )


@app.errorhandler(404)
def saknas(e):
    return render_template("error.html", fel="Sidan finns inte"), 404
