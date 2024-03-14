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
router.register('services', views.ServiceRequestViewSet, basename='services')

# The /services/{service_pk}/items nested API endpoint
services_router = routers.NestedDefaultRouter(router, 'services', lookup='service')
services_router.register('items', views.ServiceRequestItemViewSet, basename='service-items')

urlpatterns = router.urls + services_router.urls
