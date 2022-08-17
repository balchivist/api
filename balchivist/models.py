from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint


class Family(models.Model):
    identifier = models.CharField(max_length=30, unique=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Dataset(models.Model):
    identifier = models.CharField(max_length=30)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['identifier', 'family'], name='pk_name_family')
        ]


class Snapshot(models.Model):
    STATUS_CHOICES = [
        ('in-progress', 'In progress'),
        ('error', 'Error'),
        ('done', 'Done'),
        ('unknown', 'Unknown')
    ]
    ARCHIVE_STATUS_CHOICES = [
        ('unarchived', 'Unarchived'),
        ('in-progress', 'In progress'),
        ('pending-check', 'Pending checks'),
        ('done', 'Done'),
        ('error', 'Error'),
        ('to-verify', 'To verify'),
        ('unknown', 'Unknown'),
        ('other', 'Other')
    ]
    identifier = models.CharField(max_length=100)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    archive_status = models.CharField(max_length=15, choices=ARCHIVE_STATUS_CHOICES, default='unarchived')
    url = models.URLField()
    total_size = models.PositiveBigIntegerField(default=0)
    files = models.JSONField(default=dict)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['identifier', 'dataset'], name='pk_identifier_dataset')
        ]


class Node(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('shutdown', 'Shutdown'),
        ('deleted', 'Deleted')
    ]
    name = models.CharField(max_length=30, unique=True)
    version = models.CharField(max_length=30)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    heartbeat = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class NodeConfig(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['node', 'key'], name='pk_node_key')
        ]


class Task(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('error', 'Error'),
        ('unknown', 'Unknown')
    ]
    command = models.CharField(max_length=100)
    snapshot = models.ForeignKey(Snapshot, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True)
    priority = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    logurl = models.URLField(blank=True)
    arguments = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Watchlist(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('disabled', 'Disabled'),
        ('deleted', 'Deleted')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    frequency = models.CharField(max_length=30)
    mode = models.CharField(max_length=100)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('error', 'Error'),
        ('unknown', 'Unknown')
    ]
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    runner = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.TextField(blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'key'], name='pk_user_key')
        ]
