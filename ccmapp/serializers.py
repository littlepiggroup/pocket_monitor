# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from ccmapp import models
from ccmapp.models import EzvizAccount, Project, Video, Camera


class BuildingCompanySerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=models.BuildingCompanyUser.objects.all(),
                                               required=False)
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Project.objects.all(), required=False)

    class Meta:
        model = models.BuildingCompany
        exclude = ('instance_id',)
        depth = 1


class BuildingCompanyUserSerializer(serializers.ModelSerializer):
    building_company = serializers.PrimaryKeyRelatedField(many=False,
                                                          queryset=models.BuildingCompany.objects.all(), required=False)

    class Meta:
        model = models.BuildingCompanyUser
        exclude = ('instance_id',)
        depth = 1


class ProjectNameSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all(), required=False)

    class Meta:
        model = models.ProjectName
        fields = '__all__'
        depth = 1


class ProjectSerializer(serializers.ModelSerializer):
    building_company = serializers.PrimaryKeyRelatedField(many=False,
                                                          queryset=models.BuildingCompany.objects.all())
    names = ProjectNameSerializer(many=True, read_only=False)

    class Meta:
        model = models.Project
        exclude = ('instance_id',)
        depth = 1

    def create(self, validated_data):
        names_data = validated_data.pop('names')
        project = super(ProjectSerializer, self).create(validated_data)

        for name_data in names_data:
            models.ProjectName.objects.create(project=project, **name_data)
        return project


class UserCollectProjectSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all(), required=True)
    user = serializers.PrimaryKeyRelatedField(many=False, queryset=models.User.objects.all(), required=True)

    class Meta:
        model = models.UserCollectProject
        depth = 1


class UserFollowProjectSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all(), required=True)
    user = serializers.PrimaryKeyRelatedField(many=False, queryset=models.User.objects.all(), required=True)

    class Meta:
        model = models.UserFollowProject
        depth = 1


class SampleSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all())

    class Meta:
        model = models.Sample
        exclude = ('instance_id', 'contract')
        depth = 1

class SampleAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SampleAlert

# ----------------------------- Start: video related code -----------------------------
class EzvizAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EzvizAccount
        fields = '__all__'
        depth = 1


class CameraSerializer(serializers.ModelSerializer):
    ezviz_account = serializers.PrimaryKeyRelatedField(queryset=EzvizAccount.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = models.Camera
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        pass
        ezviz_account = validated_data['ezviz_account']
        from ccmapp.videomgr.videomgr import EzvizClient
        # ezviz_client = EzvizClient(ezviz_account)
        # rtmp_address = ezviz_client.get_rtmp_adr_smooth(validated_data['device_serial_number'])
        # validated_data['rtmp_address'] = rtmp_address
        temp = models.Camera.objects.create(**validated_data)
        return temp


class VideoSerializer(serializers.ModelSerializer):
    camera = serializers.PrimaryKeyRelatedField(queryset=Camera.objects.all())

    class Meta:
        model = models.Video
        fields = '__all__'
        depth = 1

class VideoAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoAlert

# ----------------------------- End: video related code -----------------------------


class TemperatureAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TemperatureAlert


class HumidityAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HumidityAlert

class GlobalReportSerializer(serializers.Serializer):
    project_count = serializers.IntegerField()
    open_alert_count = serializers.IntegerField()

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Alert
        fields = '__all__'
        depth = 1
