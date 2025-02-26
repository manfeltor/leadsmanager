from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import FormSubmission, CustomUser, ESTADO_CHOICES
from .forms import FormSubmissionEditForm, ManualFormSubmissionForm, UploadExcelForm
from django.utils.dateparse import parse_date
from django.utils.timezone import localtime
from django.db.models import Max
from django.utils import timezone
import pandas as pd
from django.contrib import messages
from leadsmanager.authvars import WPUSER, WPPASS, frmids, WPCUSTOMAPISUBM
import requests
from requests.auth import HTTPBasicAuth
from .management.commands.populate_formsubmission import normalize_submission
from django.http import HttpResponse
import logging

@login_required
def forms_list_view(request):
    forms = FormSubmission.objects.exclude(estado="negativo").order_by('-submission_id')

    # Filters
    assigned_user_id = request.GET.get('assigned_user')
    estado = request.GET.get('estado')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if assigned_user_id:
        forms = forms.filter(assigned_user_id=assigned_user_id)
    if estado:
        forms = forms.filter(estado=estado)
    if start_date:
        forms = forms.filter(fecha_creacion__gte=start_date)
    if end_date:
        forms = forms.filter(fecha_creacion__lte=end_date)

    # Sorting logic
    sort_field = request.GET.get('sort', 'fecha_creacion')  # Default sort by date
    sort_direction = request.GET.get('dir', 'desc')  # Default descending

    if sort_field in ['estado', 'fecha_creacion']:  
        sort_prefix = '' if sort_direction == 'asc' else '-'  # Ascending or Descending
        forms = forms.order_by(f"{sort_prefix}{sort_field}")

    # Toggle sorting direction for UI
    next_direction = 'asc' if sort_direction == 'desc' else 'desc'

    users = CustomUser.objects.all()
    estados = FormSubmission._meta.get_field('estado').choices

    return render(request, 'list_forms_submissions.html', {
        'forms': forms,
        'users': users,
        'estados': estados,
        'current_sort': sort_field,
        'current_direction': sort_direction,
        'next_direction': next_direction
    })

@login_required
def download_forms_excel(request):
    # Fetch data
    forms = FormSubmission.objects.all()

    # Define the required column structure
    data = []
    for form in forms:
        data.append({
            "Cod Periodo": form.fecha_creacion.strftime("%m/%Y"),
            "Fecha": form.fecha_creacion.strftime("%d/%m/%Y"),
            "Cliente": form.razon_social,
            "Servicio": form.servicio,
            "Mail": form.mail,
            "Telefono": form.telefono,
            "Origen": form.origen,
            "Sub-Origen": form.sub_origen,
            "Datos importantes informados por cliente": form.mensaje,
            "Responsable": form.assigned_user,
            "Avance": "-",
            "Estado": form.get_estado_display(),
            "Comentarios / Avances /  Notas": "-",
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Create Excel file in-memory
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="leads_export.xlsx"'
    
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Leads")

    return response

@login_required
def user_leads_view(request):
    user_leads = FormSubmission.objects.filter(assigned_user=request.user)

    # Get filter values from the request
    status_filter = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # Apply status filter if provided
    if status_filter:
        user_leads = user_leads.filter(estado=status_filter)

    # Apply date filters if provided
    if date_from:
        user_leads = user_leads.filter(fecha_creacion__date__gte=parse_date(date_from))
    if date_to:
        user_leads = user_leads.filter(fecha_creacion__date__lte=parse_date(date_to))

    context = {
        'user_leads': user_leads,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
        'estado_choices': ESTADO_CHOICES,  # Pass status choices to the template
    }

    return render(request, 'user_leads_list.html', context)

@login_required
def form_detail_view(request, submission_id):
    form = get_object_or_404(FormSubmission, submission_id=submission_id)
    return render(request, 'form_detail.html', {'form': form})

@login_required
def user_form_detail_view(request, submission_id):
    form = get_object_or_404(FormSubmission, submission_id=submission_id)
    return render(request, 'user_form_detail.html', {'form': form})

@login_required
def form_edit_view(request, submission_id):
    form_instance = get_object_or_404(FormSubmission, submission_id=submission_id)

    if not request.user.is_management:
        return redirect('unauthorized')

    if request.method == 'POST':
        form = FormSubmissionEditForm(request.POST, instance=form_instance)
        if form.is_valid():
            form.save(commit=False)
            form_instance.save(user=request.user)  # Pass the logged-in user
            return redirect('form_detail', submission_id=submission_id)
    else:
        form = FormSubmissionEditForm(instance=form_instance)

    return render(request, 'form_edit.html', {'form': form, 'form_instance': form_instance})

@login_required
def user_form_edit_view(request, submission_id):
    form_instance = get_object_or_404(FormSubmission, submission_id=submission_id)

    if request.method == 'POST':
        form = FormSubmissionEditForm(request.POST, instance=form_instance)
        if form.is_valid():
            new_status = form.cleaned_data['estado']

            # # Check if the status change is allowed for non-management users
            # if not form_instance.is_status_change_allowed(new_status, request.user):
            #     return redirect('status_change_not_allowed')  # Redirect to an error page if not allowed

            # Save the changes with the current user
            form_instance.save(user=request.user)
            return redirect('form_detail', submission_id=submission_id)
    else:
        form = FormSubmissionEditForm(instance=form_instance)

    return render(request, 'user_form_edit.html', {'form': form, 'form_instance': form_instance})

def status_change_not_allowed_view(request):
    return render(request, 'status_change_not_allowed.html')


@login_required
def manual_form_submission_view(request):
    if request.method == 'POST':
        print("Form submission detected!")
        form = ManualFormSubmissionForm(request.POST)
        if form.is_valid():
            print("Form is valid!")
            submission = form.save(commit=False)  # Don't save yet

            # Generate unique "MU" form_id
            last_form = FormSubmission.objects.filter(form_id__startswith='MU').order_by('-form_id').first()
            if last_form:
                last_form_id = int(last_form.form_id[2:])  # Strip 'MU' prefix and convert to integer
                new_form_id = f"MU{last_form_id + 1:04d}"  # Increment and format as MU0001, MU0002, etc.
            else:
                new_form_id = "MU0001"  # First manual submission

            submission.form_id = new_form_id

            # Set the creation date to now
            submission.fecha_creacion = timezone.now()

            # Manually set the submission_id (auto increment can be handled by DB)
            last_submission = FormSubmission.objects.aggregate(Max('submission_id'))
            submission.submission_id = (last_submission['submission_id__max'] or 0) + 1

            # Save the submission and log the status change
            submission.save(user=request.user)  # Save the submission
            print("Form successfully saved, redirecting...")
            return redirect('success_view')  # Redirect after success
        else:
            print("Form is invalid!")
    else:
        print("GET request detected!")

    form = ManualFormSubmissionForm()
    print("Rendering manual form submission page...")
    return render(request, 'manual_form_submission.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_management)
def update_submissions_from_excel(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']

            # Process the Excel file using Pandas
            df = pd.read_excel(excel_file)

            # Ensure the required columns exist in the Excel file
            if 'Mail' not in df.columns or 'Estado' not in df.columns or 'Cliente' not in df.columns:
                messages.error(request, "El archivo Excel debe contener las columnas 'Mail', 'Estado' y 'Cliente'.")
                return redirect('forms_list')
            
            estado_dict = {label: value for value, label in ESTADO_CHOICES}
            if df["Estado"].isin(estado_dict.keys()).all():
                # Convert human-readable values to machine values
                df["Estado"] = df["Estado"].map(estado_dict)

            # Iterate over FormSubmission objects to update them
            updated_count = 0
            for submission in FormSubmission.objects.exclude(estado='negativo'):
                matched_row = df[df['Mail'] == submission.mail]

                if matched_row.empty:
                    matched_row = df[df['Cliente'] == submission.razon_social]

                if matched_row.empty:
                    pass
                else:
                    submission.estado = matched_row['Estado'].values[0]

                submission.save()
                updated_count += 1
            
            not_updated_count = len(df.index) - updated_count

            messages.success(request, f"{updated_count} registros actualizados con éxito.")
            if not_updated_count != 0:
                messages.warning(request, f"{not_updated_count} registros no se pudieron actualizar.")
            return redirect('forms_list')
    else:
        form = UploadExcelForm()

    return redirect('forms_list')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_form_submissions(api_url, username, password):
    try:
        response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            logger.info(f"Successfully retrieved data from {api_url}")
            return response.json()
        else:
            logger.error(f"Failed to retrieve data from {api_url}: {response.status_code}")
            logger.error(f"Error message: {response.text}")
            return None
    except requests.RequestException as e:
        logger.error(f"Request failed for {api_url}: {e}")
        return None

# View to fetch new submissions and update the database
@login_required
def fetch_new_submissions_view(request):
    all_data = []
    for form_id in frmids:
        full_api_url = f'{WPCUSTOMAPISUBM}{form_id}'
        data = get_form_submissions(full_api_url, WPUSER, WPPASS)
        if data:
            form_submissions = data.get('form_submissions', [])
            for submission in form_submissions:
                submission_id = submission.get('id')
                if not FormSubmission.objects.filter(submission_id=submission_id).exists():
                    processed_submission = normalize_submission(submission, form_id)
                    all_data.append(processed_submission)

    # Bulk create new FormSubmission entries
    form_submissions = [FormSubmission(**data) for data in all_data]
    FormSubmission.objects.bulk_create(form_submissions, ignore_conflicts=True)

    return HttpResponse("Base de formularios actualizada, por favor refresca la pagina para ver los cambios.")