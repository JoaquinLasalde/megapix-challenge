from django.urls import path
from .views import CountryListView, CountryDetailView

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('countries/<int:id>/', CountryDetailView.as_view(), name='country-detail'),
]