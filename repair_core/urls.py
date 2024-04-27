from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

# The /repairmen API endpoint
router.register('repairmen', views.RepairManViewSet)

# The /customer API endpoint
router.register('customers', views.CustomerViewSet)

# The /categories API endpoint
router.register('categories', views.CategoryViewSet)

# The /manufacturers API endpoint
router.register('manufacturers', views.ManufacturerViewSet)

# The /services API endpoint
router.register('services', views.ServiceViewSet, basename='services')

# The /services/{service_pk}/items nested API endpoint
services_router = routers.NestedDefaultRouter(router, 'services', lookup='service')
services_router.register('items', views.ServiceItemViewSet, basename='service-items')

# It is not possible to directly register a normal view (such as classes inherited from APIView)
# on a router. This is based on the information found in the following StackOverflow answer:
# https://stackoverflow.com/questions/30389248/how-can-i-register-a-single-view-not-a-viewset-on-my-router/
# For now, instead of inheriting ServiceStatisticsViewSet from the APIView class,
# I have decided to use the ViewSet class as the base class.

# The /service-statistics API endpoint
router.register('service-statistics', views.ServiceStatisticsViewSet, basename='service-statistics')

urlpatterns = router.urls + services_router.urls
