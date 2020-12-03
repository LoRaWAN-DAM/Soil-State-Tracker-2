from rest_framework import permissions, status
from rest_framework.response import Response 
from rest_framework.decorators import action
from django.db.models import Count

from .serializers import ClusterSerializer, ClusterDetectorSerializer
from .service import PSListCreateViewSet
from group.models import Cluster

class ClusterViewSet(PSListCreateViewSet):
    '''
    Список кластеров
    '''
    serializer_class = ClusterDetectorSerializer
    serializer_class_by_action = {
        'list': ClusterSerializer,
        'create': ClusterSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        'create': [permissions.AllowAny]
    }

    def get_queryset(self):
        return Cluster.objects.filter(user=self.request.user) \
            .annotate(num_detectors=Count('cluster_detectors'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_detector(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cluster = self.get_object()
        detectors = request.user.detectors.filter(id__in=serializer.data['detectors'])
        detectors.update(cluster=cluster)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def remove_detector(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        detectors = request.user.detectors.filter(id__in=serializer.data['detectors'])
        detectors.update(cluster=None)
        return Response(status=status.HTTP_200_OK)