from rest_framework import permissions, status
from rest_framework.response import Response 
from rest_framework.decorators import action
from django.db.models import Count, Prefetch, Avg

from cacheops import cached_as
from cacheops import invalidate_model

from .serializers import ClusterSerializer, ClusterDetectorSerializer
from .service import (
    PSListCreateViewSet, 
    PaginationData, 
    slice_data_by_timestamp,
    queryset_mean,
)
from detector.api.serializers import DetectorSerializer, DetectorDataSerializer
from group.models import Cluster
from detector.models import DetectorData

class ClusterViewSet(PSListCreateViewSet):
    '''
    Список кластеров
    '''
    serializer_class = ClusterSerializer
    serializer_class_by_action = {
        'add_detector': ClusterDetectorSerializer,
        'remove_detector': ClusterDetectorSerializer,
        'cluster_detectors': DetectorSerializer,
        'get_mean_data': DetectorDataSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationData

    def get_queryset(self):
        return Cluster.objects.filter(user=self.request.user) \
            .annotate(num_detectors=Count('cluster_detectors')) \
            .order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def get_mean_data(self, request, *args, **kwargs):
        cluster = self.get_object()
        detectors = cluster.cluster_detectors.all() \
            .prefetch_related(
                Prefetch(
                    'data',
                    queryset=DetectorData.objects.all() \
                        .defer('detector')
                )
            )
        sliced_data = slice_data_by_timestamp(detectors)
        resulting_queryset = queryset_mean(sliced_data, detectors)
        serializer = self.get_serializer(resulting_queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        

    @action(detail=False, methods=['post'])
    def add_detector(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cluster = self.get_object()
        detectors = request.user.detectors.filter(id__in=serializer.data['detectors'])
        detectors.update(cluster=cluster)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def cluster_detectors(self, request, *args, **kwargs):
        cluster = self.get_object()
        queryset = cluster.cluster_detectors.all() \
            .select_related('cluster').nocache() \
            .order_by('id')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(data=detectors)
        return Response(serialzier.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def remove_detector(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        detectors = request.user.detectors.filter(id__in=serializer.data['detectors'])
        detectors.update(cluster=None)
        return Response(status=status.HTTP_200_OK)