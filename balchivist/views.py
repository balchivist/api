from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from balchivist.converter import Converter
from balchivist.models import Dataset
from balchivist.models import Family
from balchivist.models import Node
from balchivist.models import NodeConfig
from balchivist.models import Snapshot
from balchivist.models import Task
from balchivist.models import Watchlist
from balchivist.serializers import DatasetSerializer
from balchivist.serializers import FamilySerializer
from balchivist.serializers import NodeSerializer
from balchivist.serializers import NodeConfigSerializer
from balchivist.serializers import SnapshotSerializer
from balchivist.serializers import TaskSerializer
from balchivist.serializers import UserSerializer
from balchivist.serializers import WatchlistSerializer


class FamilyV1ViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing families.
    """
    queryset = Family.objects.all().order_by('identifier')
    lookup_field = "identifier"
    serializer_class = FamilySerializer
    permission_classes = []


class DatasetV1ViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing datasets within families.
    """
    serializer_class = DatasetSerializer
    lookup_field = "identifier"
    permission_classes = []

    def get_queryset(self):
        return Dataset.objects.filter(family__identifier=self.kwargs['family_identifier']).order_by('identifier')


class SnapshotV1ViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing snapshots within datasets within families.
    """
    serializer_class = SnapshotSerializer
    lookup_field = "identifier"
    permission_classes = []

    def get_queryset(self):
        return Snapshot.objects.filter(dataset__identifier=self.kwargs['dataset_identifier'],
                                       dataset__family__identifier=self.kwargs['family_identifier'])\
            .order_by('identifier')


class NodeV1ViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing runner nodes.
    """
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    lookup_field = "name"
    permission_classes = []


class NodeConfigV1ViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing runner node configuration settings.
    """
    serializer_class = NodeConfigSerializer
    lookup_field = "key"
    permission_classes = []

    def get_queryset(self):
        return NodeConfig.objects.filter(node__name=self.kwargs['node_name']).order_by('key')


class TaskV1ViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = []


class WatchlistV1ViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing user watchlists.
    """
    serializer_class = WatchlistSerializer
    permission_classes = []

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.kwargs['user_pk']).order_by('created_at')


class UserV1ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConverterV1View(views.APIView):
    """
    API endpoint that converts a Wikimedia-specific database name to the local name, given the language code
    """
    def get(self, request, format = None):
        if 'language' not in request.query_params.keys():
            raise ValidationError({
                'language': 'Please specify the language code to display the local name in.'
            })
        elif 'db' not in request.query_params.keys():
            raise ValidationError({
                'db': 'Please specify the database name to convert.'
            })

        converter = Converter()
        dbIds = request.query_params.getlist('db')
        result = {dbname: converter.getNameFromDB(dbname, request.query_params['language']) for dbname in dbIds}

        output = {
            'language': request.query_params['language'],
            'results': result
        }

        return Response(output)
