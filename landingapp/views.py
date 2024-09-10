from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from formsapp.models import FormSubmission
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from .graph_views import interactive_bar_plot, interactive_line_plot
import pandas as pd
from django.db.models.functions import TruncDate
import json
from django.contrib.auth.decorators import login_required

def base(req):

    days_period = 60
    date_threshold = timezone.now() - timedelta(days=days_period)

    # Get the filtered leads
    leads = FormSubmission.objects.filter(fecha_creacion__gte=date_threshold)

    group1_mapping = {
        'pendiente': 'Contacto inicial',
        'asignado': 'Contacto inicial',
        'contactado': 'Inicializados',
        'faltaCotizar': 'Inicializados',
        'cotizado': 'Inicializados',
        'interezadoAvanzar': 'Leads activos',
        'gestionExitosa': 'Leads activos',
        'pospuesto': 'Hold',
        'noAvanzo': 'Inactivos',
        'noViable': 'Inactivos',
        'nuevoCliente': 'Conversion',
        'negativo': 'Inactivos',
    }

    # Initialize counts for each group1 category
    group1_counts = {category: 0 for category in set(group1_mapping.values())}

    # Group the leads by 'estado' and count them
    leads_count = leads.values('estado').annotate(count=Count('id'))

    total_leads = leads.count()

    for lead in leads_count:
        estado = lead['estado']
        group1 = group1_mapping.get(estado)
        if group1:
            group1_counts[group1] += lead['count']

    # Calculate percentages for group1
    group1_percentages = {
        category: round((count / total_leads) * 100 if total_leads > 0 else 0, 2)
        for category, count in group1_counts.items()
    }

    # Initialize counts for each group2 category
    cold_count = active_count = closed_count = 0

    for lead in leads_count:
        state = lead['estado']
        if state in ['pendiente', 'asignado', 'contactado', 'pospuesto']:
            cold_count += lead['count']
        elif state in ['faltaCotizar', 'cotizado', 'interezadoAvanzar', 'gestionExitosa']:
            active_count += lead['count']
        elif state in ['noAvanzo', 'noViable', 'nuevoCliente', 'negativo']:
            closed_count += lead['count']

    # Calculate percentages for group2 categories
    cold_percentage = round((cold_count / total_leads) * 100 if total_leads > 0 else 0, 2)
    active_percentage = round((active_count / total_leads) * 100 if total_leads > 0 else 0, 2)
    closed_percentage = round((closed_count / total_leads) * 100 if total_leads > 0 else 0, 2)

    total_submissions = FormSubmission.objects.count()
    pending_submissions = FormSubmission.objects.filter(estado='pendiente').count()
    contacted_submissions = FormSubmission.objects.filter(estado__in=['faltaCotizar', 'cotizado']).count()
    active_submissions = FormSubmission.objects.filter(estado__in=['gestionExitosa', 'pospuesto', 'interezadoAvanzar']).count()
    recent_submissions = FormSubmission.objects.exclude(estado='negativo').order_by('-fecha_creacion')[:5]
    
    context = {
        'total_submissions': total_submissions,
        'pending_submissions': pending_submissions,
        'contacted_submissions': contacted_submissions,
        'active_submissions': active_submissions,
        'recent_submissions': recent_submissions,
        'cold_percentage': cold_percentage,
        'active_percentage': active_percentage,
        'closed_percentage': closed_percentage,
        'days_period': days_period,
        'group1_percentages': group1_percentages,
    }
    
    return render(req, "landing.html", context=context)

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Change 'home' to your desired redirect URL after login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'custom_login.html')

@login_required
def category_breakdown_view(request):
    # Get the selected days_period from the GET request or default to 60
    days_period = request.GET.get('days_period', 60)
    
    try:
        days_period = int(days_period)  # Ensure it's an integer
    except ValueError:
        days_period = 60  # Fallback to 60 if something invalid is passed

    date_threshold = timezone.now() - timedelta(days=days_period)
    leads = FormSubmission.objects.filter(fecha_creacion__gte=date_threshold)

    group1_mapping = {
        'pendiente': 'Contacto inicial',
        'asignado': 'Contacto inicial',
        'contactado': 'Inicializados',
        'faltaCotizar': 'Inicializados',
        'cotizado': 'Inicializados',
        'interezadoAvanzar': 'Leads activos',
        'gestionExitosa': 'Leads activos',
        'pospuesto': 'Hold',
        'noAvanzo': 'Inactivos',
        'noViable': 'Inactivos',
        'negativo': 'Inactivos',
        'noDefinido': 'Inactivos',
    }

    breakdown_data = {category: {} for category in set(group1_mapping.values())}
    leads_count = leads.values('estado').annotate(count=Count('id'))

    for lead in leads_count:
        estado = lead['estado']
        group1 = group1_mapping.get(estado)
        if group1:
            if estado not in breakdown_data[group1]:
                breakdown_data[group1][estado] = 0
            breakdown_data[group1][estado] += lead['count']

    group1_percentages = {}
    total_leads_in_group = {}
    trend_data = {}

    for group1, subcategories in breakdown_data.items():
        total_in_group = sum(subcategories.values())
        total_leads_in_group[group1] = total_in_group
        group1_percentages[group1] = {
            subcategory: round((count / total_in_group) * 100, 2)
            for subcategory, count in subcategories.items()
        }

        # Trend over time for this group (group by day and count)
        trend_for_group = leads.filter(estado__in=subcategories.keys()).annotate(
            date=TruncDate('fecha_creacion')
        ).values('date').annotate(daily_count=Count('id')).order_by('date')
        
        trend_df = pd.DataFrame(list(trend_for_group))

        if not trend_df.empty:
            # interactive_line_plot now returns two values, the graph and regression info
            graph_json, regression_info = interactive_line_plot(trend_df, 'date', 'daily_count', f'Trend for {group1}', add_regression=True)
            trend_data[group1] = {
                'data': json.loads(graph_json),  # Convert JSON string to Python object
                'regression_info': regression_info  # Pass regression info to the context
            }

    # Generate bar plots for each group1 category
    plot_data = {}
    for group1, data in group1_percentages.items():
        print(str(len(data)) + f"{group1}")
        df = pd.DataFrame(list(data.items()), columns=['subcategoria', 'percentage'])
        plot_data[group1] = interactive_bar_plot(df, 'subcategoria', 'percentage', f'Desglose {group1}', yaxis_title='porcentaje')

    total_leads_in_group_json = json.dumps(total_leads_in_group)
    trend_data_json = json.dumps(trend_data)  # Encode trend_data to JSON

    context = {
        'plot_data': plot_data,
        'trend_data_json': trend_data_json,
        'total_leads_in_group': total_leads_in_group,
        'total_leads_in_group_json': total_leads_in_group_json,
        'days_period': days_period,
    }

    return render(request, "category_breakdown.html", context)