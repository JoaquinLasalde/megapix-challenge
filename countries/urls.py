from django.urls import path
from .views import CountryListView, CountryDetailView

urlpatterns = [
    # Ruta para listar todos los países y crear nuevos
    path('countries/', CountryListView.as_view(), name='country-list'),
    # Ruta para ver un país específico
    path('countries/<int:id>/', CountryDetailView.as_view(), name='country-detail'),
]