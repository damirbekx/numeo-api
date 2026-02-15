from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, CountryViewSet, AnalyticsViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'countries', CountryViewSet, basename='countries')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = router.urls
