"""
app.py - Flask application for Interbanking Reportes
"""

import os
import base64
import importlib
from datetime import date, timedelta
from functools import wraps

from flask import Flask, jsonify, render_template, request, session, redirect, url_for

import json
from reportes.generador import generar_excel

USUARIOS = json.loads(os.environ.get("AUTH_USUARIOS", "{}"))

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-cambiar")

# Verificación de variables de entorno al arrancar
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EMPRESAS_MODULOS = {
    "eliantus": "srcELIANTUS.CodigoBancosEliantus",
    "elementa": "srcELEMENTA.CodigoBancosElementa",
    "integra": "srcINTEGRA.CodigoBancosINTEGRA",
}


# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("usuario"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        if USUARIOS.get(usuario) == password:
            session["usuario"] = usuario
            return redirect(url_for("index"))
        error = "Usuario o contraseña incorrectos"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ─────────────────────────────────────────────
# RUTAS PRINCIPALES
# ─────────────────────────────────────────────

@app.route("/")
@login_required
def index():
    hoy = date.today()
    return render_template(
        "index.html",
        desde=(hoy - timedelta(days=7)).isoformat(),
        hasta=hoy.isoformat(),
        usuario=session.get("usuario"),
    )


@app.route("/api/cuentas")
@login_required
def api_cuentas():
    empresa = request.args.get("empresa", "eliantus").lower()
    if empresa not in EMPRESAS_MODULOS:
        return jsonify({"error": "Empresa inválida"}), 400

    mod = importlib.import_module(EMPRESAS_MODULOS[empresa])
    cuentas = [
        {
            "id": i,
            "numero": c.numero,
            "tipo": c.tipo,
            "peso": c.peso,
            "banco": c.banco,
            "nombre": c.nombre,
            "abreviatura": c.abreviatura,
            "label": f"{c.abreviatura} - {c.numero} ({c.banco}) [{c.peso}]",
        }
        for i, c in enumerate(mod.CUENTAS)
    ]
    return jsonify(cuentas)


@app.route("/api/generar", methods=["POST"])
@login_required
def api_generar():
    data = request.get_json(force=True)
    empresa = data.get("empresa", "").lower()
    desde = data.get("desde", "")
    hasta = data.get("hasta", "")
    indices = data.get("indices", [])

    if empresa not in EMPRESAS_MODULOS:
        return jsonify({"error": "Empresa inválida"}), 400
    if not desde or not hasta:
        return jsonify({"error": "Fechas requeridas"}), 400
    if desde > hasta:
        return jsonify({"error": "La fecha 'Desde' no puede ser mayor que 'Hasta'"}), 400
    if not indices:
        return jsonify({"error": "Seleccioná al menos una cuenta"}), 400

    mod = importlib.import_module(EMPRESAS_MODULOS[empresa])
    todas = mod.CUENTAS
    cuentas_sel = [todas[i] for i in indices if 0 <= i < len(todas)]

    try:
        excel_bytes, resultados = generar_excel(
            empresa=empresa,
            desde=desde,
            hasta=hasta,
            cuentas_seleccionadas=cuentas_sel,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(
        {
            "excel": base64.b64encode(excel_bytes).decode(),
            "filename": f"reporte_{empresa}_{desde}_{hasta}.xlsx",
            "resultados": [
                {"nombre": c.abreviatura, "ok": ok} for c, ok in resultados
            ],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)