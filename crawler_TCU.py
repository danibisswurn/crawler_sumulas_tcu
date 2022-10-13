import requests
import csv


def requester(id):
    response = requests.get(f"https://pesquisa.apps.tcu.gov.br/rest/publico/base/sumula/documento?termo=*&filtro=DATASESSAO%3A%5B19000101%20to%2020220927%5D&ordenacao=DTRELEVANCIA%20asc,%20NUMEROINT%20asc&quantidade=1&inicio={id}&sinonimos=true",
        headers={
            "content-type": "application/json",
        },
    )
    if response.status_code == 200:
        return response.json().get("documentos")

    return None

def run(initial_id, final_id):
    with open("tnu.csv", "w", encoding="utf-8", newline='') as cursor:
        fieldnames = [
            "NUMERO",
            "CABECALHO",
            "DATASESSAOFORMATADA",
            "VIGENTE",
            "EXCERTO",
            "REFERENCIALEGAL",
            "TEMA",
            "AUTORTESE",
        ]
        writer = csv.DictWriter(
            cursor,
            fieldnames=fieldnames,
            delimiter=";"
        )
        writer.writeheader()

        id = initial_id
        while id <= final_id:
            sumulas = requester(id)
            for sumula in sumulas:
                data = {field: sumula.get(field, "") for field in fieldnames}
                writer.writerow(data)
            id += 1

if __name__ == "__main__":
    run(
        initial_id=0, final_id=288
    )
