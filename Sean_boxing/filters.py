from django.contrib.auth.models import User
import django_filters

from Sean_boxing.models import Box


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]

class BoxFilter(django_filters.FilterSet):
    # first_name = django_filters.CharFilter(lookup_expr='icontains')
    month_created = django_filters.NumberFilter(field_name='created_at', lookup_expr='month')
    day_created = django_filters.NumberFilter(field_name='created_at', lookup_expr='day')
    day_created__gt = django_filters.NumberFilter(field_name='created_at', lookup_expr='day__gt')
    day_created__lt = django_filters.NumberFilter(field_name='created_at', lookup_expr='day__lt')
    class Meta:
        model = Box
        fields = ['work_user', 'created_at', 'updated_at', ]