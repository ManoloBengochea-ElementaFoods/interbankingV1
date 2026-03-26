import http.client
import json


def obtener_extractos_Eliantus(cuenta, token, desde, hasta, secrets, limit=10000):
    conn = http.client.HTTPSConnection("api-gw.interbanking.com.ar")
    headers = {
        "client_id":     secrets["client_id"],
        "Authorization": f"Bearer {token}",
        "accept":        "application/json",
    }
    path = (
        f"/api/prod/v1/accounts/{cuenta.numero}/statements"
        f"?account-type={cuenta.tipo}"
        f"&bank-number={cuenta.banco}"
        f"&currency={cuenta.peso}"
        f"&customer-id={secrets['customer_id']}"
        f"&date-since={desde}"
        f"&date-until={hasta}"
        f"&limit={limit}"
    )
    conn.request("GET", path, headers=headers)
    data = json.loads(conn.getresponse().read().decode("utf-8"))
    return data.get("general_data", {}), data.get("statements", [])
