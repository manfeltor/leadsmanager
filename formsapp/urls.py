from django.urls import path
from .views import forms_list_view, form_detail_view, form_edit_view, user_leads_view, manual_form_submission_view
from .views import user_form_detail_view, user_form_edit_view, status_change_not_allowed_view, update_submissions_from_excel
from .views import fetch_new_submissions_view
from usersapp.views import unauthorized_view

urlpatterns = [
    path('list/', forms_list_view, name='forms_list'),
    path('update-submissions/', update_submissions_from_excel, name='update_submissions'),
    path('fetch-submissions/', fetch_new_submissions_view, name='fetch_submissions'),
    path('detail/<int:submission_id>/', form_detail_view, name='form_detail'),
    path('edit/<int:submission_id>/', form_edit_view, name='form_edit'),
    path('unauthorized/', unauthorized_view , name='unauthorized'),
    path('my_leads/', user_leads_view, name='user_leads'),
    path('user_form_detail/<int:submission_id>/', user_form_detail_view, name='user_form_detail'),
    path('user_form_edit/<int:submission_id>/', user_form_edit_view, name='user_form_edit'),
    path('status-change-not-allowed/', status_change_not_allowed_view, name='status_change_not_allowed'),
    path('manual-form-submission/', manual_form_submission_view, name='manual_form_submission'),
]