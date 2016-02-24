from django.db import transaction
from django.shortcuts import get_object_or_404
from hashids import Hashids
from rest_framework import mixins, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from crowdsourcing.models import TaskWorker, TaskWorkerResult
from crowdsourcing.serializers.task import (TaskSerializer,)
from csp import settings


class MTurkAssignmentViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = TaskWorker.objects.all()
    serializer_class = TaskSerializer


class MTurkConfig(ViewSet):

    @staticmethod
    def get_mturk_url(request):
        host = settings.MTURK_WORKER_HOST
        return Response({'url': host}, status=status.HTTP_200_OK)
