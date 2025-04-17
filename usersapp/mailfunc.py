import requests
import pandas as pd
from django.contrib import messages
from leadsmanager.authvars import PRFTAPIKEY

def main_func(uploaded_file):
    message_list = []  # Initialize message list
    try:
        df_raw = pd.read_excel(uploaded_file)
        clean_df, message = clean_raw_df(df_raw)  # Unpack clean_raw_df result
        message_list.append((messages.SUCCESS, message['text']))  # Append success message
        
        if not validate_columns(clean_df):
            raise ValueError("La validacion de columnas fallo. Por favor checkea las columnas 'estadoLpn' y 'trackingTransporte'")
        
        mail_messages = automails(clean_df)
        message_list.extend([(messages.SUCCESS, msg['text']) if msg['level'] == 25 else (messages.ERROR, msg['text']) for msg in mail_messages])

    except Exception as e:
        print('02')
        message_list.append((messages.ERROR, f"Error procesando archivo: {str(e)}"))

    return message_list

def clean_raw_df(raw_df: pd.DataFrame):
    try:
        filtered_df = raw_df[['pedido', 'seller', 'nombre', 'estadoLpn', 'trackingTransporte']].drop_duplicates(subset=['pedido'])
        return filtered_df, {'level': messages.SUCCESS, 'text': "DataFrame limpiado con exito."}
    except Exception as e:
        return None, {'level': messages.ERROR, 'text': f"Error limpiando el dataframe: {str(e)}"}

def validate_columns(clean_df):
    valid_values = ['COLECTADO_CA', 'AUSENTE', 'EN_SUCURSAL', 'EN_TRONCAL']
    if clean_df['estadoLpn'].isnull().any() or not clean_df['estadoLpn'].isin(valid_values).all() or clean_df['trackingTransporte'].isnull().any():
        return False
    return True

def automails(clean_df: pd.DataFrame):
    url = "https://transactional.myperfit.com/v1/mail/send"
    headers = {
        "Authorization": PRFTAPIKEY,
        "Content-Type": "application/json"
    }
    mail_messages = []
    for _, reclamo in clean_df.iterrows():

        # Compose email content based on `estadoLpn`
        subject, content = compose_email_content(reclamo)
        data = {
            "from": {"email": "notificaciones@intralog.com.ar"},
            "subject": subject,
            "content": {"html": content},
            "recipients": [
            {
                "to": {"email": "atclientepaq.ar@correoargentino.com.ar"},
                "cc": [
                {"email": "cmontenegro@intralog.com.ar"},
                ]
            }
        ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 202:
            mail_messages.append({'level': messages.SUCCESS, 'text': f"Email envioado para trk tracking {reclamo['trackingTransporte']}."})
            print(response.status_code, 1)
        else:
            mail_messages.append({'level': messages.ERROR, 'text': f"Email fallido para trk {reclamo['trackingTransporte']}."})
            print(response.status_code, 0)
    return mail_messages

def compose_email_content(reclamo):
    # Logic for content based on estadoLpn
    if reclamo['estadoLpn'] == 'COLECTADO_CA':
        subject = f"{reclamo['estadoLpn']} {reclamo['trackingTransporte']}"
        content = f"""<p>Estimados,<br><br>

Solicitamos por favor la actualización del siguiente pedido que se encuentra demorado y no tenemos novedades del mismo.<br><br>

pedido: {reclamo['pedido']}<br>seller: {reclamo['seller']}<br>nombre: {reclamo['nombre']}<br>tracking num: {reclamo['trackingTransporte']}<br><br>


Aguardamos novedades

 ¡Saludos!</p>"""
        
    elif reclamo['estadoLpn'] == 'AUSENTE':
        subject = f"{reclamo['estadoLpn']} {reclamo['trackingTransporte']}"
        content = f"""<p>Estimados,<br><br>

Solicitamos por favor la actualización del siguiente pedido el cual fue visitado pero no tenemos novedades del mismo.<br><br>

pedido: {reclamo['pedido']}<br>seller: {reclamo['seller']}<br>nombre: {reclamo['nombre']}<br>tracking num: {reclamo['trackingTransporte']}<br><br>


Aguardamos novedades

 ¡Saludos!</p>"""
        
    elif reclamo['estadoLpn'] == 'EN_SUCURSAL':
        subject = f"{reclamo['estadoLpn']} {reclamo['trackingTransporte']}"
        content = f"""<p>Estimados,<br><br>

El siguiente pedido ya excedió el tiempo pactado en la sucursal, solicitamos que avance con el proceso de plazo vencido<br><br>

pedido: {reclamo['pedido']}<br>seller: {reclamo['seller']}<br>nombre: {reclamo['nombre']}<br>tracking num: {reclamo['trackingTransporte']}<br><br>

Aguardamos confirmación
 ¡Saludos!</p>"""
        
    elif reclamo['estadoLpn'] == 'EN_TRONCAL':
        subject = f"{reclamo['estadoLpn']} {reclamo['trackingTransporte']}"
        content = f"""<p>Estimados,<br><br>

Solicitamos por favor la actualización del siguiente pedido el cual fue visitado pero no actualizo su estado, quedo en poder del cartero.<br><br>

pedido: {reclamo['pedido']}<br>seller: {reclamo['seller']}<br>nombre: {reclamo['nombre']}<br>tracking num: {reclamo['trackingTransporte']}<br><br>

Aguardamos confirmación
 ¡Saludos!</p>"""

    return subject, content
