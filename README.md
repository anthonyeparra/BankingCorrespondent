# WEB SCRAPING TEST - PLATAFORM

## Requisitos de la Aplicación

La aplicación requiere tener:

1. Python en su versión 3.11
2. Serverless Framework
3. Plugin de requirements
4. Plugin offline
5. Crear entorno virtual
6. Instalar dependencia
7. Ejecutar el serverless offline
8. Base de datos

## APLICACIÓN DESPLEGADA EN AWS LAMBDA + SERVICIO DE COGNITO COMO AUTHENTICADOR
### Instrucciones

1. **Instalar Python 3.10**

   Asegúrate de tener Python 3.11 instalado. Puedes descargarlo desde [python.org](https://www.python.org/downloads/release/python-3100/).

2. **Instalar Serverless Framework**

   Para instalar Serverless Framework, ejecuta el siguiente comando:

   ```sh
   npm install -g serverless

3. **Instalar Plugin Requirements**

   Instala el plugin de requirements con el siguiente comando:

   ```sh
   serverless plugin install -n serverless-python-requirements

4. **Instalar Plugin offline**

   Instala el plugin offline con el siguiente comando:

   ```sh
   serverless plugin install -n serverless-offline

5. **Crear entorno virtual**

    Crea un entorno virtual para la aplicación con los siguientes comandos:

    ```sh
    python -m venv venv
    # Para Linux o Macos
    source venv/bin/activate
    # Para Windows
    venv\Scripts\activate

6. **Instalar dependencias**

   Asegúrate de que el archivo requirements.txt esté en el directorio del proyecto. Luego, ejecuta el siguiente comando para instalar las dependencias:

    ```sh
    pip install -r requirements.txt

7. **Ejecutar serverless offline**

   Para ejecutar el proyecto:

    ```sh
    serverless offline
    # En su defecto
    sls offline

    Esto genera en el ambiente offline

8. **Base de datos**

   Necesito un servidor de sql, podriamos Mostrar Xaamps, Una Maquina virtual como servidor ...:

    ```sh
    Ejecutar el script de la carpeta Db en archivo llamado banking_correspondent.sql

    Adjunte Modelo de base de datos.

**`URL APIS: https://4jve2k1hc2.execute-api.us-east-1.amazonaws.com/dev/`**

## CREAR USUARIO INFORMACION POR CUFES

**`POST /users`**

Crear cliente base de datos, como Cognito Auth
Argumento:

```json
{
    "first_name":"Anthony",
    "last_name":"Parra",
    "email":"anthonyeparra@hotmail.com",
    "password":"A980119p@"
}
```

Atributos:

**`first_name`**: (obligatorio) : Primer Nombre.
**`last_name`**: (obligatorio) : Apellidos.
**`email`**: (obligatorio) : Email.
**`password`**: (obligatorio) : Contraseña.

Respuesta Exitosa:

```json
{
    "status": 201,
    "description": "Resource created successfully.",
    "data": {
        "user_id": 4,
        "first_name": "Anthony",
        "last_name": "Parra",
        "email": "anthonyeparra@hotmail.com",
        "password": "$5$rounds=535000$ROi/v7iflBWhG3Hq$6iulcglNnuTSdJQUeX42ihMH34hj2vS6OmpmeKDl/u7"
    }
}
```

Respuesta de errores:

Data invalida

```json
{
    "first_name":"Anthony",
    "last_name":"Parra",
    "email":"anthonyeparra@hotmail.com",
    "password":"A980119p"
}
```
Respuesta Invalida

```json
{
    "status": 400,
    "description": "A validation error ocurred.",
    "data": "The provided email already exists."
}
```
**`POST /get-token`**

Inicio de session de la plataforma
Argumento:

```json
{
    "email":"anthonyeparra@hotmail.com",
    "password":"A980119p@"
}
```

Atributos:
**`email`**: (obligatorio) : Email.
**`password`**: (obligatorio) : Contraseña.

Respuesta Exitosa:

```json
{
    "status": 200,
    "description": "The request was successfull.",
    "data": {
        "AccessToken": "eyJraWQiOiIrSUpxXC9NQ0M0ODZlUUxwaXJuXC9icEtYU2ZObk9jU0c2enVSNkw0ZzkrZG89IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI2NDI4YzRiOC0zMDIxLTcwMWMtMDgyNy04MmQ3M2ZlODRmN2YiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9BMGo4Y1lSc1EiLCJjbGllbnRfaWQiOiI1MDc3MGx1djFyOGpkNXNnc3JuOGwzNTg0ZSIsIm9yaWdpbl9qdGkiOiJkNmJkOTY2YS0yNTI5LTRhZjctOTZlZS02MWEyNzBmNDUwNjMiLCJldmVudF9pZCI6IjQ4M2E0N2YwLWI4NzQtNDc4Yi1hY2UzLTRmZDM2Nzk5MTVhYSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NDM5NDk4NzcsImV4cCI6MTc0Mzk1MzQ3NywiaWF0IjoxNzQzOTQ5ODc3LCJqdGkiOiI1MDJiODEzNS00MTc2LTQ5OWMtYjI0MC1mZjkxNTEwOTA2YzEiLCJ1c2VybmFtZSI6IjY0MjhjNGI4LTMwMjEtNzAxYy0wODI3LTgyZDczZmU4NGY3ZiJ9.qy37e8LlZytU9vcjjW39UtwNkucc8OMXLdZrZ6doIY6955l0kn3bthUigIGaSNLPmMUml4Zw9GSQpbHMscsWLfD3kJbasDykZNFmaZBwBEdHsw-IIO02qh4_QFqTmHW248IMrtltSFFzxjXL1OMZzgeZNzW-F4OP8-59oM0j1O285g3p8A605B5Yc1plc4kqHBa1Ap1HkXmhIlpAkXDKPEiFZs-I22A6v_2z_RyKjL0_Mfv3-va83zegegMZX96D3wKtpvv-S_qHh6iAA0HyRK_xjHnxjoeMUaSL1W5b9zJB48DgBZ6dbZ_uQdCMFNqg7aCO7HEv1lL5acJ_O1oBIA",
        "Idtoken": "eyJraWQiOiJmMW1SQlRUOTVvZEFCRGxQeFgxTG1ta3ZaSGFITm1tcEpOT3BhalNmY01NPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI2NDI4YzRiOC0zMDIxLTcwMWMtMDgyNy04MmQ3M2ZlODRmN2YiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfQTBqOGNZUnNRIiwiY29nbml0bzp1c2VybmFtZSI6IjY0MjhjNGI4LTMwMjEtNzAxYy0wODI3LTgyZDczZmU4NGY3ZiIsIm9yaWdpbl9qdGkiOiJkNmJkOTY2YS0yNTI5LTRhZjctOTZlZS02MWEyNzBmNDUwNjMiLCJhdWQiOiI1MDc3MGx1djFyOGpkNXNnc3JuOGwzNTg0ZSIsImV2ZW50X2lkIjoiNDgzYTQ3ZjAtYjg3NC00NzhiLWFjZTMtNGZkMzY3OTkxNWFhIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NDM5NDk4NzcsImV4cCI6MTc0Mzk1MzQ3NywiaWF0IjoxNzQzOTQ5ODc3LCJqdGkiOiI3ODg5ZjQ4Mi00MzJmLTQ3YTgtOTY2ZC1iODBjNjA1ZWE5NjQiLCJlbWFpbCI6ImFpYXZpbGFAZ21haWwuY29tIn0.P-i2Y-SPodOTHQOUViA7xZFYiu8lQ92xvYW2M3KeDq5fgY8HyHyQwEvalenVGbhqv8AHQ7TnrerInYa7A706KBCdCU-w1eT7Jr01dt47q7Sqk_qeSTsCtC9lV_xWpQO5HpXWhE_lqGBd4JIMecAthLmOBu9__FUu7e7Nm1MknnHVDm6pj1JEHcEoNKx1XL0y9NVsu2AYrbcdaFhbOFC5m4_Wgvhcv8N4co9PPeY84YnWlLy6Z6_eF8NsSFMh6jET5Yc8IMn_iEPnQnmLG4G39MlrOdk294UHHsVJQom1qCOLTx9bKOKtW37fayZZXrzS-wm-TNTFlBAA9D975yxCHg",
        "RefreshToken": "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.A_5jD7ek_tU3TfzVKzegDMhVju4ap-3UeQBBGOKTx05w3HmeKYtLECxn9aYtrnP37OPXbdNNpvzChrWMCfe7Y5iUvJ6pgU2zNUWaFQDI6Ki6dz3NFHyF8-J-Xz5WtOEDW5k7M9WJRJtcKWB2ybh_vqRImwPb3TQINEmknTUrGmtF17WITxQIHMhNE3W4Z6jWg4KRYjh8Puc_nqW1qwYpcr-sC7TicxeUdqhXeg5BR6fmNjWbSF_YMEs5Kd5UuGjlwZtAY6tm5nJzBj9ylOoapqdEEssNB_JtSV6Xe5se0Nqdh4D3l8n8KeHF3bC4cblBBcCRf4mfByNtZfT0jzQBcA.NdQc5IEb8PzychGT.XxgbNmBLhHn3pY8x3n-sDROV-4Nsh-TsZA0ePwosLcoxjMfGrGLmNwroeDcz3mvxRYjvG3owu4nIEDLznqdjSibwamDkQr9NTp--QvB4C-ghsNkWP5vKaFgPwCU9xi9ic84__f4RyJ_DPTHcHB4XvbGDfYT_gOtuIstOLlbYfiE8IWVOXBwIDMJ9mv8RBnONBTtTVGJ0fwkxRc2muE_bK_orrvHoFbT4OLvF6Nw_5q_HXvgJNS7SX0qj9HcEn1iiWtbPplvaHL-4HkzO6YVGQBnweI9ms0MnF_fFz1JPtQp0J05d0RF34cs75jCQ3byQe-jbOqepPj2Q_Dlp_paxyzJDY6OKSJVbTAXX7NKqYSO16C_2lXNo2_V2RevzmXNnzfuYzd1ZAwvgV6qIMnqLxaHmmVnOnijXTrpi0DbENA1kzt7TH-5d_vuDS062FK24BNsHJbzBfLrB8Z5Qzo8tu857h-DXUZiRM4kfZI6lh0cW8eflnJY27MXOHZ0iDWIuAxRUHhJ6jB8CCEvpfr8pvxN8BBxgCfPUX_Qix4UtU82tErcuoNFCy-DIJAgtpvEaSF5btLBit2i3NVRJfi89XzQiHXPi4njT6tVfTyGOK3R-OwfylFFqC0vppgWUOiHJfIclHSIc4M1FlCSjB2sbe4hCrCTcypmQbBkiw3Zj86NBN7QQyNc3g3mZvI5Y4P8QzVg40iy7kRA7oax17DGtKw866S6M5CCyFlB-2QCzKmDzsx4PBIvHXiQOe6Q5yQw6itaS9NlmaVFssFYJocdG9PyWdkMKVp87tJwkYB6nXdpTus5p4hGahh87IW0b7eh03htHdhcPPojzWJpMQcb3msNjRF9Ggl38p8OrsfCq-liFRqD5XKCQnIirhXJWVImEoIckSOcz_CbdI19gX0eZiHQ21_gW1jUS4m-NwtICoSmgZI4QPL_16saI7WiSa9wmQdPG7m-B8S1FJzFVb_s8QmCoSn4sY1M_CilLiUcM7BT1XTjwHlIimKpODOS6FggO4LitcpMVfyrpib8UJ7g3GRebKE3qR8oQex0SaR1qc9zOvOW6J-5jdwa_oYm4DNCxCwqnHnGVwB5xLzzWmN7bU5QRtGMhXWAWR7-8HOHoOQ1FMF3ZzhS8PTcP4u7qA_Vg33ZvWxJB0QmNfAGuWkeDz8Rzp8knU_QHBvLLs5kuWi6r_qN4XO5IOsF4qQyJEPljQQE_KQa4lBU6EoTqxH1ZqpwvYEPnSDycOijUUbAkWEFeN3-gAO6ngT3UhbYW2p-G6nJjY2ka5DTF-1rc4XGxam2Qt2TcdGgBv_hMZCP58sxn636JOa0Wnun9N8M.PvV3DEhupj6-MoqEvMIqfg"
    }
}
```
**`GET /resources/correspondent`**

Lista los corresponsales o por id

Respuesta Exitosa:

```json
{
    "status": 200,
    "description": "The request was successfull.",
    "data": [
        {
            "correspondent_id": 1,
            "name": "Rebaja",
            "address": "Calle 23 # 4A - 34",
            "maximum_capacity": 10000000.0,
            "available_space": 57482762.0,
            "quota_date": "2025-04-05"
        },
        {
            "correspondent_id": 2,
            "name": "Olimpica",
            "address": "Av 33 Sur",
            "maximum_capacity": 20000000.0,
            "available_space": 90000000.0,
            "quota_date": "2025-04-05"
        }...
    ]
}
```
**`GET /resources/transation_type`**

Lista los tipos de transaciones o por id
Deposito o Retiro
Respuesta Exitosa:

```json
{
    "status": 200,
    "description": "The request was successfull.",
    "data": [
        {
            "transaction_type_id": 1,
            "name": "Desposito",
            "icon_code": "ArrowUpFromLine"
        },
        {
            "transaction_type_id": 2,
            "name": "Retiro",
            "icon_code": "ArrowDownToLine"
        }
    ]
}
```

**`POST /transaction`**

Crear la transacion a ejecutar Retiro o Deposito
Argumento:

```json
{
    "transaction_type_id": 1, 
    "correspondent_id": 1,
    "amount": 10000000
}
```

Atributos:

**`transaction_type_id`**: (obligatorio) : Tipo de transación.
**`correspondent_id`**: (obligatorio) : Sucursal.
**`amount`**: (obligatorio) : Monto a Despositar o Retirar.

Respuesta Exitosa:

```json
{
    "status": 200,
    "description": "Operación realizada correctamente",
    "data": {
        "available_space": 67482762.0,
        "operation_name": "Desposito",
        "ammount": 10000000.0
    }
}
```

Respuesta de errores:

Data invalida

```json
{
    "transaction_type_id": 3,
    "correspondent_id": 1,
    "amount": 10000000
}
```
Respuesta Invalida

```json
{
    "status": 400,
    "description": "A validation error ocurred.",
    "data": "The provided transaction_type_id does not exist."
}
```
Adjunto Url de Posmtan y Respositorio github

**URL POSTMAN [https://drive.google.com/drive/folders/1KehDE4oMtxcnvux8KUU0rLoS8_Rnv06G?usp=sharing]**

**URL GITHUB [https://github.com/anthonyeparra/BankingCorrespondent]**
