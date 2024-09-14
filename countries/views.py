from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework.response import Response
from django.db.models import Q
from .models import Country
from .serializers import CountrySerializer
from rest_framework.pagination import CursorPagination

class CountryFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_name')
    population = filters.NumberFilter()
    population_gt = filters.NumberFilter(field_name='population', lookup_expr='gt')
    population_lt = filters.NumberFilter(field_name='population', lookup_expr='lt')
    continent = filters.CharFilter(method='filter_continent')
    area_gt = filters.NumberFilter(field_name='area', lookup_expr='gt')
    area_lt = filters.NumberFilter(field_name='area', lookup_expr='lt')

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(official_name__icontains=value))

    def filter_continent(self, queryset, name, value):
        return queryset.filter(continents__icontains=value)

    class Meta:
        model = Country
        fields = ['name', 'population', 'continent', 'area']

class OptimizedCountryPagination(CursorPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
    ordering = 'id'

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        return super().paginate_queryset(queryset, request, view)

    def get_count(self, queryset):
        return queryset.count()

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = OptimizedCountryPagination
    filterset_class = CountryFilter

    def get_queryset(self):
        return super().get_queryset().order_by('id')

class CountryDetailView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = 'id'