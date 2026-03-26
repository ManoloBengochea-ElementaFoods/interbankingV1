# Interbanking · Reportes (Streamlit)

App para generar extractos bancarios en Excel directamente desde la API de Interbanking.

---

## Correr local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Asegurate de tener el archivo `.streamlit/secrets.toml` con las credenciales reales.

---

## Publicar en Streamlit Cloud (paso a paso)

### 1. Subir a GitHub

```bash
git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

> ⚠️ Verificá que `.streamlit/secrets.toml` aparezca en `.gitignore` y NO se suba.

### 2. Crear app en Streamlit Cloud

1. Entrá a https://share.streamlit.io
2. Hacé click en **"New app"**
3. Conectá tu cuenta de GitHub
4. Seleccioná el repo y como archivo principal: `app.py`
5. Click en **"Deploy"**

### 3. Cargar las credenciales (Secrets)

1. En tu app desplegada, click en **"⋮" → Settings → Secrets**
2. Pegá el contenido de tu `secrets.toml` local:

```toml
[eliantus]
client_id     = "..."
client_secret = "..."
url_servicio  = "https://eliantus.com"
customer_id   = "..."

[elementa]
client_id     = "..."
...

[integra]
client_id     = "..."
...
```

3. Click **"Save"** — la app se reinicia automáticamente.

### 4. Compartir con el equipo

Streamlit te da una URL pública. Podés restringir el acceso desde
**Settings → Sharing** (requiere plan Teams o autenticación propia).

---

## Estructura

```
interbanking-streamlit/
├── app.py                        ← App principal Streamlit
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── secrets.toml              ← ⚠️ Local only, nunca a GitHub
├── reportes/
│   └── generador.py              ← Lógica Excel (genérica)
├── srcELIANTUS/
│   ├── authEliantus.py
│   ├── CodigoBancosEliantus.py
│   └── MovimientosEliantus.py
├── srcELEMENTA/                  ← Completar cuentas y credenciales
└── srcINTEGRA/                   ← Completar cuentas y credenciales
```
