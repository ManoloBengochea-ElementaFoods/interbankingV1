import http.client, json

def obtener_extractos_Integra(cuenta, token, desde, hasta, secrets, limit=10000):
    conn = http.client.HTTPSConnection("api-gw.interbanking.com.ar")
    headers = {"client_id": secrets["client_id"], "Authorization": f"Bearer {token}", "accept": "application/json"}
    path = (
        f"/api/prod/v1/accounts/{cuenta.numero}/statements"
        f"?account-type={cuenta.tipo}&bank-number={cuenta.banco}&currency={cuenta.peso}"
        f"&customer-id={secrets['customer_id']}&date-since={desde}&date-until={hasta}&limit={limit}"
    )
    conn.request("GET", path, headers=headers)
    data = json.loads(conn.getresponse().read().decode("utf-8"))
    return data.get("general_data", {}), data.get("statements", [])
