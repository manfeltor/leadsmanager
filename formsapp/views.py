from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import FormSubmission, CustomUser, ESTADO_CHOICES
from .forms import FormSubmissionEditForm, ManualFormSubmissionForm, UploadExcelForm
from django.utils.dateparse import parse_date
from django.db.models import Max
from django.utils import timezone
import pandas as pd
from django.contrib import messages

@login_required
def forms_list_view(request):
    # Start with all forms
    forms = FormSubmission.objects.all()

    # Get filter parameters from the request
    assigned_user_id = request.GET.get('assigned_user')
    estado = request.GET.get('estado')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter by assigned user if provided
    if assigned_user_id:
        forms = forms.filter(assigned_user_id=assigned_user_id)

    # Filter by estado if provided
    if estado:
        forms = forms.filter(estado=estado)

    # Filter by date range if provided
    if start_date:
        forms = forms.filter(fecha_creacion__gte=start_date)
    if end_date:
        forms = forms.filter(fecha_creacion__lte=end_date)

    # Get all users and estados for the dropdowns
    users = CustomUser.objects.all()
    estados = FormSubmission._meta.get_field('estado').choices

    return render(request, 'list_forms_submissions.html', {
        'forms': forms,
        'users': users,
        'estados': estados,
    })

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
            if 'mail' not in df.columns or 'estado' not in df.columns or 'cliente' not in df.columns:
                messages.error(request, "El archivo Excel debe contener las columnas 'mail', 'estado' y 'cliente'.")
                return redirect('forms_list')

            # Iterate over FormSubmission objects to update them
            updated_count = 0
            for submission in FormSubmission.objects.exclude(estado='negativo'):
                matched_row = df[df['mail'] == submission.mail]

                if matched_row.empty:
                    matched_row = df[df['cliente'] == submission.razon_social]

                if matched_row.empty:
                    submission.estado = 'noDefinido'
                else:
                    submission.estado = matched_row['estado'].values[0]

                submission.save()
                updated_count += 1

            messages.success(request, f"{updated_count} registros actualizados con éxito.")
            return redirect('forms_list')
    else:
        form = UploadExcelForm()

    return redirect('forms_list')