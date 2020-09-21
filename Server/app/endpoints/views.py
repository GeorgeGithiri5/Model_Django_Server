from rest_framework import viewsets
from rest_framework import mixins

from app.endpoints.models import Endpoint
from app.endpoints.serializers import EndpointSerializer

from app.endpoints.models import MLAlgorithm
from app.endpoints.serializers import MLAlgorithmSerializer

from app.endpoints.models import MLAlgorithmStatus
from app.endpoints.serializers import MLAlgorithmStatusSerializer

from app.endpoints.models import MLRequest
from app.endpoints.serializers import MLRequestSerializer

class EndpointViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()

class MLAlgorithmViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = MLAlgorithmSerializer
    queryset = MLAlgorithm.objects.all()

def deactivate_other_statuses(instance):
    old_statuses = MLAlgorithmStatus.objects.filter(parent_mlalgorithm=instance.parent_mlalgorithm,created_at__lt=instance.created_at,active=True)
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    MLAlgorithmStatus.objects.bulk_update(old_statuses,["active"])

class MLAlgorithmStatusViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet,mixins.CreateModelMixin):
    serializer_class = MLAlgorithmStatusSerializer
    queryset = MLAlgorithmStatus.objects.all()
    def perform_create(self,serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                deactivate_other_statuses(instance)
        except Exception as e:
            raise APIException(str(e))

class MLRequestViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet,mixins.UpdateModelMixin):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()

