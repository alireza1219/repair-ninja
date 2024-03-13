from rest_framework_nested import routers
from .views import CategoryViewSet, CustomerViewSet, ManufacturerViewSet, RepairManViewSet

router = routers.DefaultRouter()

# The /repairmen API endpoint
router.register('repairmen', RepairManViewSet)

# The /customer API endpoint
router.register('customers', CustomerViewSet)

# The /categories API endpoint
router.register('categories', CategoryViewSet)

# The /manufacturers API endpoint
router.register('manufacturers', ManufacturerViewSet)

urlpatterns = router.urls
