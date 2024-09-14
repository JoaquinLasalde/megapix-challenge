from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework.response import Response
from django.db.models import Q
from .models import Country
from .serializers import CountrySerializer
from rest_framework.pagination import CursorPagination

# Definición de filtros para la API de países
class CountryFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name')
    population = filters.NumberFilter()
    population_gt = filters.NumberFilter(field_name='population', lookup_expr='gt')
    population_lt = filters.NumberFilter(field_name='population', lookup_expr='lt')
    continent = filters.CharFilter(method='filter_continent')
    area_gt = filters.NumberFilter(field_name='area', lookup_expr='gt')
    area_lt = filters.NumberFilter(field_name='area', lookup_expr='lt')

    # Método personalizado para filtrar por nombre o nombre oficial
    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(official_name__icontains=value))

    # Método personalizado para filtrar por continente
    def filter_continent(self, queryset, name, value):
        return queryset.filter(continents__icontains=value)

    class Meta:
        model = Country
        fields = ['name', 'population', 'continent', 'area']

# Paginación optimizada para la lista de países
class OptimizedCountryPagination(CursorPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
    ordering = 'id'

    # Sobrescribe el método para incluir el conteo total
    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        return super().paginate_queryset(queryset, request, view)

    # Método para obtener el conteo total de países
    def get_count(self, queryset):
        return queryset.count()

    # Personaliza la respuesta paginada para incluir el conteo total
    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

# Vista para listar todos los países
class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = OptimizedCountryPagination
    filterset_class = CountryFilter

    # Asegura que los resultados estén ordenados por id
    def get_queryset(self):
        return super().get_queryset().order_by('id')

# Vista para obtener detalles de un país específico
class CountryDetailView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = 'id'  # Usa 'id' como campo de búsqueda en lugar de 'pk'