from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_about_page, name='about'),
    path('about/', views.show_about_page, name='about'),
    path('playground/', views.show_playground_page, name='playground'),
    path('concepts/', views.show_concepts_page, name='concepts'),
    path('show_entries/<int:business_id>', views.show_entries, name='entries'),
    path('analyze/<int:business_id>', views.generate_financial_statement, name='analyze')
]
