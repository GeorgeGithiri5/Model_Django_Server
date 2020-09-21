from django.conf.urls import url,include
from rest_framework import DefaultRouter

from  app.endpoints.views import EndpointViewSet
from  app.endpoints.views import MLAlgorithmViewSet
from  app.endpoints.views import MLAlgorithmStatusViewSet
from  app.endpoints.views import MLRequest

router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints",EndpointViewSet,basename="endpoints")
router.register(r"mlalgorithms",MLAlgorithmViewSet,basename="mlAlgorithm")
router.register(r"mlalgorithmstatus",MLAlgorithmStatusViewSet,basename ="mlalgorithmstatus")
router.register(r"mlrequest",MLAlgorithmStatusViewSet,basename = "mlrequests")

urlpatterns = [
    url(r"^api/v1/",include(router.urls)),
]
