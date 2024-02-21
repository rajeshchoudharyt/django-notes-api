from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='index'),
    path('share/', views.share_note, name='share'),
    path('<int:note_id>/', views.retrieve_note, name='retrieve_edit'),
    path('version-history/<int:note_id>/', views.note_version, name='version')
]