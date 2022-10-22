from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:note_id>/', views.one_note, name='one_note')
]