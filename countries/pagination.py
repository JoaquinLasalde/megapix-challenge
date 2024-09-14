from rest_framework.pagination import CursorPagination
from rest_framework.response import Response

class CountryCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'id'
    
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

    # Definición del esquema de la respuesta paginada para la documentación de la API
    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'next': {
                    'type': 'string',
                    'nullable': True,
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                },
                'results': schema,
            },
        }