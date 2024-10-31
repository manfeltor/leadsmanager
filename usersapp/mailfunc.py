import requests
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from django.shortcuts import render

def main_func(req):

    path_raw_oms = select_file("Selecciona el archivo de OMS")
    df_raw = pd.read_excel(path_raw_oms)
    clean_df = clean_raw_df(df_raw)
    if not validate_columns(clean_df):
        raise ValueError("La validacion de columnas fallo. Por favor checkea las columnas 'estadoLpn' y 'trackingTransporte")
    automails(clean_df)

def clean_raw_df(raw_df: pd.DataFrame):

    try:
        filtered_df = raw_df[['pedido', 'seller', 'nombre', 'estadoLpn', 'trackingTransporte']].drop_duplicates(subset=['pedido'])
        return filtered_df
    
    except Exception as e:
        messagebox.showerror("Error", f"Error limpiando el dataframe: {str(e)}")
        return None

def select_file(title):

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title, filetypes=[("Excel files", "*.xlsx")])
    root.destroy()

    if not file_path:
        messagebox.showerror("Error", "no selecciono ningun archivo.")
        return None

    return file_path

def validate_columns(clean_df):
    # Check if 'estadoLpn' column has empty values
    if clean_df['estadoLpn'].isnull().any():
        return False
    
    # Check if 'estadoLpn' column has values other than the specified ones
    valid_values = ['COLECTADO_CA', 'AUSENTE', 'EN_SUCURSAL', 'EN_TRONCAL']
    if not clean_df['estadoLpn'].isin(valid_values).all():
        return False
    
    # Check if 'trackingTransporte' column has empty values
    if clean_df['trackingTransporte'].isnull().any():
        return False
    
    return True

def automails(request, clean_df: pd.DataFrame):

    url = "https://transactional.myperfit.com/v1/mail/send"
    headers = {
        "Authorization": "intralog-tr-UWRAflBbTPzEzhvAXSEveytWYaHqxOHl",
        "Content-Type": "application/json"
    }

    for index, reclamo in clean_df.iterrows():  # Iterate over rows using iterrows()

        if reclamo['estadoLpn'] == 'COLECTADO_CA':

            content = f"""<p>Estimados,<br><br>

Solicitamos por favor la actualización del siguiente pedido que se encuentra demorado y no tenemos novedades del mismo.<br><br>

pedido: {reclamo['pedido']}<br>seller: {reclamo['seller']}<br>nombre: {reclamo['nombre']}<br>tracking num: {reclamo['trackingTransporte']}<br><br>


Aguardamos novedades

 ¡Saludos!</p>"""
            
            subject = f"{reclamo['estadoLpn']} {reclamo['trackingTransporte']}"

        elif reclamo['estadoLpn'] == 'AUSENTE':

            content = f"""<p>Estimados,<br><br>

Solicitamos por favor la actualización del siguiente pedido el cual fue visitado pero no tenemos novedades del mismo.<br><br>

pedido: {reclamo['pedido']}<br>seller: {reclamo['seller']}<br>nombre: {reclamo['nombre']}<br>tracking num: {reclamo['trackingTransporte']}<br><br>


Aguardamos novedades

 ¡Saludos!</p>"""
            
            subject = f"{reclamo['estadoLpn']} {reclamo['trackingTransporte']}"

        elif reclamo["estadoLpn"] == 'EN_SUCURSAL':

            content = f"""<p>Estimados,<br><br>

El siguiente pedido ya excedió el tiempo pactado en la sucursal, solicitamos que avance con el proceso de plazo vencido<br><br>

pedido: {reclamo['pedido']}<br>seller: {reclamo['seller']}<br>nombre: {reclamo['nombre']}<br>tracking num: {reclamo['trackingTransporte']}<br><br>

Aguardamos confirmación
 ¡Saludos!</p>"""
            
            subject = f"{reclamo['estadoLpn']} {reclamo['trackingTransporte']}"

        elif reclamo["estadoLpn"] == 'EN_TRONCAL':

            content = f"""<p>Estimados,<br><br>

Solicitamos por favor la actualización del siguiente pedido el cual fue visitado pero no actualizo su estado, quedo en poder del cartero.<br><br>

pedido: {reclamo['pedido']}<br>seller: {reclamo['seller']}<br>nombre: {reclamo['nombre']}<br>tracking num: {reclamo['trackingTransporte']}<br><br>

Aguardamos confirmación
 ¡Saludos!</p>"""
            
            subject = f"VISITA {reclamo['trackingTransporte']}"

        data = {
            "from": { "email": "notificaciones@intralog.com.ar" },
            "subject": subject,
            "content": {"html": content},
            "recipients": [{"to": {"email": "atclientepaq.ar@correoargentino.com.ar"}}]
            # "recipients": [{"to": {"email": "cmontenegro@intralog.com.ar"}}]
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

    return render(request, 'functions.html')
