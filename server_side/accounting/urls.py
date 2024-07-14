from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_welcome_page, name='home'),
    path('testhtml/', views.send_html),
    path('playground/', views.latest_entries, name='playground'),
    path('about/', views.latest_entries, name='about')
]
