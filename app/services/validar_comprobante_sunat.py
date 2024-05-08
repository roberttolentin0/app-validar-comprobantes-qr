import os
import requests
import json
import jwt

from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from dotenv import load_dotenv
from ..utils.utils import measure_time

load_dotenv()

RUC = os.getenv('RUC')
CLIENT_ID = os.getenv('CLIENT_ID_SOL')
CLIENT_SECRET = os.getenv('CLIENT_SECRET_SOL')


def get_token():
    url = f"https://api-seguridad.sunat.gob.pe/v1/clientesextranet/{CLIENT_ID}/oauth2/token/"
    payload = f'grant_type=client_credentials&scope=https%3A%2F%2Fapi.sunat.gob.pe%2Fv1%2Fcontribuyente%2Fcontribuyentes&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response_token = requests.post(url, headers=headers, data=payload)

    if response_token.status_code == 200:
        return response_token.json().get('access_token')
    else:
        print(f"Error al obtener el token. Código de estado: {response_token.status_code}")
        print(response_token.text)
        return None


def decode_token(token):
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except ExpiredSignatureError:
        print("El token ha expirado.")
        return None
    except InvalidTokenError:
        print("El token es inválido.")
        return None


def expired_token(payload):
    if payload:
        expiracion = payload.get("exp", 0)
        if expiracion > 0:
            exp_timestamp = datetime.utcfromtimestamp(expiracion)
            curr_date = datetime.utcnow()
            expired_token = exp_timestamp < curr_date
            # print('entro expired_token', expired_token, exp_timestamp, curr_date)
            if expired_token:
                print("El token ha expirado.")
            else:
                print("El token es válido hasta:", exp_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            return expired_token
        else:
            print("El token no incluye información de expiración.")
    else:
        print('Sin payload', payload)


def is_active_token(token):
    payload = decode_token(token)
    if payload is None:
        return False
    return not expired_token(payload)


def update_token_in_json():
    print('-- update_token_in_json')
    token = get_token()
    # Guardar el token en un archivo JSON
    data = {"token": token}
    with open('app\services\data_token.json', 'w') as json_file:
        json.dump(data, json_file)


def get_token_from_json():
    # Cargar el token desde el archivo JSON
    try:
        with open('app\services\data_token.json', 'r') as json_file:
            data = json.load(json_file)
            return data["token"]
    except FileNotFoundError as e:
        print(e)
        return None


@measure_time
def validar_comprobante(data_comprobante):
    """Validar estado de comprobante en SUNAT
    Keyword arguments:
    data_comprobante -- Dict con datos del comprobante:
        ex:
        {
            "numRuc": "20522199495",
            "codComp": "01",
            "numeroSerie": "F001",
            "numero": "55285",
            "fechaEmision": "30/11/2023",
            "monto": "22725.00"
        }
    Return: Respuesta de la API Sunat
    """
    print(data_comprobante)
    token = get_token_from_json()
    # print('token', token, is_active_token(token))
    if token == '' or not is_active_token(token):
        update_token_in_json()
        token = get_token_from_json()

    auth_token = f'Bearer {token}'
    url = f'https://api.sunat.gob.pe/v1/contribuyente/contribuyentes/{RUC}/validarcomprobante'
    payload = json.dumps(data_comprobante)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        response_data = response.json()['data']
        print('response_data', response_data)
        status_comprobante = data_comprobante | response_data
        return status_comprobante
    elif response.status_code == 401:
        pass
    else:
        print(f"Error al obtener Código de estado: {response.status_code}")
        print(response.text)
        return None

