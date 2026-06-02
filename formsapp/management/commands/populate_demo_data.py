import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from formsapp.models import FormSubmission, LeadHistory, Campaign
from usersapp.models import CustomUser


EMPRESAS_ORIGEN = ["INTRALOG", "INTRAPAL"]

RAZONES_SOCIALES = [
    "Transportes del Sur S.A.", "Logística Andina SRL", "Distribuidora Patagónica S.A.",
    "Grupo Comercial Norte", "Almacenes Centrales SA", "Frigorífico del Litoral SRL",
    "Constructora Pampas SA", "Metalúrgica Bonaerense SRL", "Agroexport Argentina SA",
    "Servicios Industriales del Este", "Cargas Express SRL", "Depósitos Fiscales SA",
    "Farmacéutica del Centro SRL", "Electro Insumos SA", "Bebidas del Plata SRL",
    "Editorial Universitaria SA", "Textil Cuyana SRL", "Cerealera del Noroeste SA",
    "Automotores del Río SA", "Plásticos Industriales SRL", "Maderas del Norte SRL",
    "Química del Sur SA", "Importadora Atlántica SRL", "Ferretera Central SA",
    "Alimentos Frescos SRL", "Tecnología Industrial SA", "Obras Civiles del Plata SRL",
    "Pescados y Mariscos SA", "Envases Modernos SRL", "Agropecuaria Pampeana SA",
    "Repuestos Automotrices SRL", "Refrigeración Industrial SA", "Semillas del Oeste SRL",
    "Lubricantes del Sur SA", "Indumentaria Bonaerense SRL", "Muebles del Litoral SA",
    "Servicios Portuarios SRL", "Aceros del Plata SA", "Vinos y Espirituosas SRL",
    "Cerámica Argentina SA", "Pinturas del Norte SRL", "Lácteos del Centro SA",
    "Calzados del Sur SRL", "Electrónica del Plata SA", "Seguros y Finanzas SRL",
    "Consultoría Estratégica SA", "Diseño Industrial SRL", "Soluciones Logísticas SA",
    "Comercializadora del Oeste SRL", "Inversiones del Litoral SA",
]

NOMBRES = [
    "Carlos García", "María López", "Juan Martínez", "Ana Rodríguez", "Roberto Sánchez",
    "Laura Fernández", "Diego González", "Claudia Pérez", "Martín Díaz", "Valeria Torres",
    "Sebastián Ruiz", "Patricia Flores", "Hernán Molina", "Cecilia Castro", "Pablo Ortega",
    "Florencia Moreno", "Andrés Jiménez", "Natalia Romero", "Gustavo Vargas", "Verónica Reyes",
    "Francisco Herrera", "Alejandra Medina", "Ramón Suárez", "Silvana Aguilar", "Oscar Muñoz",
]

SERVICIOS = [
    "Depósito fiscal", "Logística inversa", "Cross docking", "Almacenamiento a temperatura controlada",
    "Distribución urbana", "Fulfillment e-commerce", "Gestión de inventario", "Transporte de carga",
    "Operación integral", "Importación y despacho aduanero",
]

ORIGENES = ["Web", "LinkedIn", "Referido", "Email", "Exposición", "Cold Call", "Google Ads"]
SUB_ORIGENES = ["Formulario web", "InMail", "Cliente referente", "Campaña outbound", "ExpoLogística", "Prospección directa", "Search"]

MENSAJES = [
    "Necesitamos ampliar nuestra capacidad de almacenamiento para el próximo trimestre.",
    "Estamos evaluando tercerizar nuestra logística de distribución.",
    "Buscamos un operador para manejo de productos refrigerados.",
    "Necesitamos cotización para servicio de fulfillment con envíos a todo el país.",
    "Tenemos un proyecto de importación y necesitamos depósito fiscal.",
    "Estamos revisando proveedores para reducir costos logísticos.",
    "Necesitamos urgente espacio de almacenamiento temporario.",
    "Queremos cotizar servicio completo de logística para lanzamiento de nueva línea.",
    "Tenemos picos estacionales y buscamos capacidad flexible.",
    "Nos interesa evaluar la propuesta para nuestra operación de e-commerce.",
    "Estamos migrando de operación propia a tercerizada.",
    "Necesitamos soporte logístico para expansión al interior del país.",
    "",
]

ESTADO_DISTRIBUTION = [
    ("esperandoDatos", 22),
    ("faltaCotizar", 18),
    ("cotizado", 15),
    ("avanzando", 10),
    ("noAvanzo", 13),
    ("noViable", 8),
    ("nuevoCliente", 7),
    ("negativo", 7),
]

CAMPAIGN_DATA = [
    ("ExpoLogística 2024", "2024-03-01", "2024-05-31", "Contactos generados en la exposición anual."),
    ("Campaña Web Q2 2024", "2024-04-01", "2024-06-30", "Leads inbound desde formulario web."),
    ("Prospección Outbound Q3 2024", "2024-07-01", "2024-09-30", "Campaña de cold calling y email."),
    ("Cierre de Año 2024", "2024-10-01", "2024-12-31", "Leads de cierre del ejercicio fiscal."),
    ("Arranque 2025", "2025-01-01", "2025-06-30", "Primer semestre 2025."),
]


def weighted_estado():
    pool = []
    for estado, weight in ESTADO_DISTRIBUTION:
        pool.extend([estado] * weight)
    return random.choice(pool)


def random_date(start_days_ago=400, end_days_ago=0):
    delta = random.randint(end_days_ago, start_days_ago)
    return timezone.now() - timedelta(days=delta, hours=random.randint(0, 23), minutes=random.randint(0, 59))


class Command(BaseCommand):
    help = 'Wipes FormSubmission/LeadHistory/Campaign data and loads synthetic demo data. Users are preserved.'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=200, help='Number of fake leads to generate (default: 200)')

    def handle(self, *args, **kwargs):
        count = kwargs['count']

        self.stdout.write('Limpiando datos existentes...')
        LeadHistory.objects.all().delete()
        FormSubmission.objects.all().delete()
        Campaign.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('  Tablas vaciadas.'))

        self.stdout.write('Creando campañas...')
        campaigns = []
        for name, start, end, desc in CAMPAIGN_DATA:
            c = Campaign.objects.create(
                name=name,
                start_date=start,
                end_date=end,
                description=desc,
            )
            campaigns.append(c)
        self.stdout.write(self.style.SUCCESS(f'  {len(campaigns)} campañas creadas.'))

        users = list(CustomUser.objects.all())
        if not users:
            self.stdout.write(self.style.WARNING('  No hay usuarios en la base — assigned_user quedará vacío.'))

        self.stdout.write(f'Generando {count} leads sintéticos...')
        submissions = []
        histories = []
        used_ids = set()

        for i in range(count):
            sub_id = random.randint(10001, 99999)
            while sub_id in used_ids:
                sub_id = random.randint(10001, 99999)
            used_ids.add(sub_id)

            origen_idx = random.randint(0, len(ORIGENES) - 1)
            razon = random.choice(RAZONES_SOCIALES)
            nombre = random.choice(NOMBRES)
            estado = weighted_estado()
            empresa = random.choice(EMPRESAS_ORIGEN)
            form_id = random.choice([3, 4, 5, 7])
            campaign = random.choice(campaigns + [None, None])
            assigned = random.choice(users + [None]) if users else None
            fecha = random_date()

            avance = "▓" if estado == "negativo" else "⊕"

            raw_data = {
                "id": sub_id,
                "created_at": fecha.isoformat(),
                "Razón Social": razon,
                "Nombre y Apellido": nombre,
                "Me interesa el servicio": random.choice(SERVICIOS),
                "Mensaje": random.choice(MENSAJES),
            }

            fs = FormSubmission(
                empresa=empresa,
                fecha_creacion=fecha,
                razon_social=razon,
                nombre_y_apellido=nombre,
                servicio=random.choice(SERVICIOS),
                mail=f"{nombre.lower().replace(' ', '.')}{random.randint(1,99)}@example.com",
                telefono=f"11{random.randint(10000000, 99999999)}",
                origen=ORIGENES[origen_idx],
                sub_origen=SUB_ORIGENES[origen_idx],
                mensaje=random.choice(MENSAJES),
                avance=avance,
                estado=estado,
                form_id=form_id,
                submission_id=sub_id,
                data=raw_data,
                assigned_user=assigned,
                campaign=campaign,
            )
            submissions.append(fs)

        FormSubmission.objects.bulk_create(submissions)
        self.stdout.write(self.style.SUCCESS(f'  {len(submissions)} leads creados.'))

        self.stdout.write('Generando historial de estados...')
        saved_submissions = list(FormSubmission.objects.all())
        for fs in saved_submissions:
            histories.append(LeadHistory(
                form_submission=fs,
                previous_status=None,
                new_status=fs.estado,
                updated_by=None,
                timestamp=fs.fecha_creacion,
            ))
            if fs.estado not in ("esperandoDatos", "negativo") and random.random() > 0.4:
                histories.append(LeadHistory(
                    form_submission=fs,
                    previous_status="esperandoDatos",
                    new_status=fs.estado,
                    updated_by=random.choice(users) if users else None,
                    timestamp=fs.fecha_creacion + timedelta(days=random.randint(1, 15)),
                ))

        LeadHistory.objects.bulk_create(histories)
        self.stdout.write(self.style.SUCCESS(f'  {len(histories)} entradas de historial creadas.'))

        self.stdout.write(self.style.SUCCESS('\nDatos demo cargados exitosamente.'))
