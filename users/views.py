from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Avg
from users.models import User
from users.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response

class UserPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'age', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    ordering_fields = ['id', 'first_name', 'last_name', 'age', 'country', 'city', 'birth_date', 'is_active']

class CountryViewSet(viewsets.ViewSet):
    """
    Returns a searchable list of unique countries from the users database.
    """
    def list(self, request):
        search_query = request.query_params.get('search', '').strip()

        # Get unique countries, exclude nulls/blanks, and order them
        query = User.objects.exclude(country__isnull=True).exclude(country='').values_list('country', flat=True).distinct().order_by('country')

        if search_query:
            query = query.filter(country__icontains=search_query)

        return Response(list(query))

class AnalyticsViewSet(viewsets.ViewSet):
    """
    Returns analytics data for the dashboard.
    """
    def list(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()

        # Top 5 countries
        users_by_country = User.objects.exclude(country__isnull=True).exclude(country='').values('country').annotate(count=Count('id')).order_by('-count')[:5]

        # Top 5 occupations
        users_by_occupation = User.objects.exclude(occupation__isnull=True).exclude(occupation='').values('occupation').annotate(count=Count('id')).order_by('-count')[:5]

        # Average age
        average_age = User.objects.aggregate(avg_age=Avg('age'))['avg_age']

        data = {
            "total_users": total_users,
            "active_users": active_users,
            "top_countries": list(users_by_country),
            "top_occupations": list(users_by_occupation),
            "average_age": round(average_age, 1) if average_age else 0
        }

        return Response(data)
