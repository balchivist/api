from django.contrib.auth.models import User
from rest_framework.fields import SerializerMethodField

from rest_framework.serializers import ModelSerializer

from balchivist.models import Dataset
from balchivist.models import Family
from balchivist.models import Node
from balchivist.models import NodeConfig
from balchivist.models import Snapshot
from balchivist.models import Task
from balchivist.models import Watchlist


class FamilySerializer(ModelSerializer):
    class Meta:
        model = Family
        fields = ["identifier", "url"]


class DatasetSerializer(ModelSerializer):
    family = FamilySerializer(read_only=True)
    latest_snapshot_date = SerializerMethodField()

    def get_latest_snapshot_date(self, obj):
        result = Snapshot.objects.filter(dataset=obj).order_by('-date')

        if result.count():
            return result.first().date

        return None

    class Meta:
        model = Dataset
        fields = ["identifier", "url", "family", "latest_snapshot_date"]


class SnapshotSerializer(ModelSerializer):
    dataset = DatasetSerializer(read_only=True)
    total_size = SerializerMethodField()

    def get_total_size(self, obj):
        if not hasattr(obj, 'total_size') or obj.total_size == 0:
            all_files = obj['files'].values()
            return sum(map(lambda x: x['size'], all_files))
        else:
            return obj.total_size

    def save(self, **kwargs):
        kwargs['total_size'] = self.get_total_size(self.validated_data)
        self.instance = super().save(**kwargs)
        return self.instance

    class Meta:
        model = Snapshot
        fields = "__all__"


class NodeSerializer(ModelSerializer):
    class Meta:
        model = Node
        fields = "__all__"


class NodeConfigSerializer(ModelSerializer):
    node = NodeSerializer(read_only=True)

    class Meta:
        model = NodeConfig
        fields = "__all__"

    def create(self, validated_data):
        node = Node.objects.get(
            name=self.context.get("view").kwargs["node_name"])
        nodeconfig = NodeConfig.objects.create(node=node, **validated_data)
        return nodeconfig


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class WatchlistSerializer(ModelSerializer):
    class Meta:
        model = Watchlist
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.get(id=self.context.get("view").kwargs["user_pk"])
        watchlist = Watchlist.objects.create(user=user, **validated_data)
        return watchlist


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
