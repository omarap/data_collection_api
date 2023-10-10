# filters.py

import django_filters
from .models import *

class ConstructionBuildingFilter(django_filters.FilterSet):
    pap = django_filters.CharFilter(lookup_expr='icontains')  # Allows searching by a partial match of the 'name' field

    class Meta:
        model = ConstructionBuilding
        fields = ['pap']  # Add more fields if needed
