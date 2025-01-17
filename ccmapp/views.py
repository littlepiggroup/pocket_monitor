# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime as DT
from collections import OrderedDict

import django_filters.rest_framework
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import viewsets, filters, status
from rest_framework.decorators import detail_route
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.utils.translation import ugettext_lazy as _

from ccmapp import models, serializers

# Create your views here.
from ccmapp.models import EzvizAccount, Camera, Video, Project, Alert, SampleAlert, GlobalReport, VideoAlert, \
    TemperatureAlert, HumidityAlert
from ccmapp.serializers import EzvizAccountSerializer, CameraSerializer, VideoSerializer, GlobalReportSerializer, \
    SampleAlertSerializer, VideoAlertSerializer, TemperatureAlertSerializer, \
    HumidityAlertSerializer
from ccmapp.report import phase_report
from ccmauth.serializers import UserRegisterSerializer, UserPasswordResetSerializer


# ----------------------------- Start: auth related views -----------------------------

class LoginCodeAccessView(GenericAPIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        errors = None
        user_model = get_user_model()
        phone = self.request.data.get(user_model.USERNAME_FIELD)
        is_new_user = False
        if phone:
            data = {user_model.USERNAME_FIELD: phone}
            serializer = self.get_serializer(**data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if isinstance(serializer, UserRegisterSerializer):
                is_new_user = True
        else:
            errors = {'detail': _("Must include '%s'." % user_model.USERNAME_FIELD)}
        if errors:
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=(status.HTTP_201_CREATED if is_new_user else status.HTTP_200_OK))

    def get_serializer(self, **kwargs):
        user_model = get_user_model()

        try:
            user_model.objects.get(**kwargs)
            return UserPasswordResetSerializer(data=kwargs)
        except user_model.DoesNotExist:
            return UserRegisterSerializer(data=kwargs)

# ----------------------------- End: auth related views -----------------------------


def index_view(request):
    templateName = 'index.html'
    return render_to_response(templateName, RequestContext(request, locals()))

def normalize_resp(data_list):
    resp_json = [
        ("count", len(data_list)),
    ("next", None),
        ("previous", None),
        ("results", data_list)
    ]
    return OrderedDict(resp_json)


class BuildingCompanyViewSet(viewsets.ModelViewSet):
    queryset = models.BuildingCompany.objects.all()
    serializer_class = serializers.BuildingCompanySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('id', 'name', 'disabled', 'added_time')
    ordering_fields = ('id', 'name', 'disabled', 'added_time')


class BuildingCompanyUserViewSet(viewsets.ModelViewSet):
    queryset = models.BuildingCompanyUser.objects.all()
    serializer_class = serializers.BuildingCompanyUserSerializer
    filter_fields = ('id', 'login_name', 'disabled', 'building_company', 'added_time')
    ordering_fields = ('id', 'login_name', 'disabled', 'building_company', 'added_time')


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('id', 'status', 'nature', 'create_time', 'region', 'address',
                     'last_edit_time', 'building_company', 'instance_id', 'added_time', 'PrjName')
    search_fields = ('nature', 'region', 'address')
    ordering_fields = ('id', 'status', 'nature', 'create_time', 'region', 'address',
                       'last_edit_time', 'building_company', 'added_time', 'PrjName')

    @detail_route(methods=['post'], url_path='collect')
    def collect(self, request, pk=None):
        iterator = models.UserCollectProject.objects.filter(project_id=pk, user_id=request.user.id)

        if iterator:
            errors = {'detail': _("Project already collected.")}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = models.Project.objects.get(id=pk)
        except models.Project.DoesNotExist:
            errors = {'detail': _("Project not existed.")}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        data = {"user": request.user.id, "project": project.id}
        serializer = serializers.UserCollectProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['post'], url_path='uncollect')
    def uncollect(self, request, pk=None):
        iterator = models.UserCollectProject.objects.filter(project_id=pk, user_id=request.user.id)

        if iterator:
            iterator.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        errors = {'detail': _("Project not collected.")}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], url_path='follow')
    def follow(self, request, pk=None):
        iterator = models.UserFollowProject.objects.filter(project_id=pk, user_id=request.user.id)

        if iterator:
            errors = {'detail': _("Project already followed.")}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = models.Project.objects.get(id=pk)
        except models.Project.DoesNotExist:
            errors = {'detail': _("Project not existed.")}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        data = {"user": request.user.id, "project": project.id}
        serializer = serializers.UserFollowProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['post'], url_path='unfollow')
    def unfollow(self, request, pk=None):
        iterator = models.UserFollowProject.objects.filter(project_id=pk, user_id=request.user.id)

        if iterator:
            iterator.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        errors = {'detail': _("Project not followed.")}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectNameViewSet(viewsets.ModelViewSet):
    queryset = models.ProjectName.objects.all()
    serializer_class = serializers.ProjectNameSerializer
    filter_fields = ('id', 'project', 'name', 'added_time')
    ordering_fields = ('id', 'project', 'name', 'added_time')


class SampleViewSet(viewsets.ModelViewSet):
    queryset = models.Sample.objects.all()
    serializer_class = serializers.SampleSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('id', 'name', 'project', 'item_name', 'kind_name',
                     'core_code_id', 'core_code_id_end', 'status')
    search_fields = ('name',)
    ordering_fields = ('id', 'name', 'project', 'item_name', 'kind_name',
                       'core_code_id', 'core_code_id_end', 'status')


class SampleAlertViewSet(viewsets.ModelViewSet):
    queryset = SampleAlert.objects.all()
    serializer_class = SampleAlertSerializer

# -------------------- Start: video related views --------------------


class EzvizAccountViewSet(viewsets.ModelViewSet):
    queryset = EzvizAccount.objects.all()
    serializer_class = EzvizAccountSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('device_serial_number',)


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('camera',)

class VideoAlertViewSet(viewsets.ModelViewSet):
    queryset = VideoAlert.objects.all()
    serializer_class = VideoAlertSerializer

class TemperatureAlertViewSet(viewsets.ModelViewSet):
    queryset = TemperatureAlert.objects.all()
    serializer_class = TemperatureAlertSerializer

class HumidityAlertViewSet(viewsets.ModelViewSet):
    queryset = HumidityAlert.objects.all()
    serializer_class = HumidityAlertSerializer


class AlertViewSet(viewsets.ModelViewSet):
    queryset = models.Alert.objects.all()
    serializer_class = serializers.AlertSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('status', 'alert_type','project__id', 'is_open')
    search_fields = ('alert_type',)
    ordering_fields = ('alert_type',)


class GlobalReportView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    # http://www.django-rest-framework.org/tutorial/3-class-based-views/
    def get(self, request, format=None):
        project_count = Project.objects.all().count()
        total_open_alerts = Alert.objects.exclude(status=SampleAlert.CLOSED).count()
        global_report = GlobalReport(project_count, total_open_alerts)
        serializer = GlobalReportSerializer(global_report)
        return Response(serializer.data)


class CompanyPhaseReportView(APIView):

    # http://www.django-rest-framework.org/tutorial/3-class-based-views/
    def get(self, request, format=None):
        company_id = request.GET.get('company_id')
        time_range = request.GET.get('time_range', 'last_week')
        days = phase_report.time_para_to_days(time_range)

        # all_projects = Project.objects.filter(company__id=company_id)
        return Response(normalize_resp(phase_report.company_phase_report(company_id, days)))


class ProjectPhaseReportView(APIView):
    def get(self, request, format=None):
        time_range = request.GET.get('time_range', 'last_week')
        company_id = request.GET.get('company_id')
        project_id = request.GET.get('project_id')
        days = phase_report.time_para_to_days(time_range)

        # end_time = DT.datetime.now()
        # start_time = end_time - DT.timedelta(days=7)
        # if time_range == 'last_month':
        #     start_time = end_time - DT.timedelta(days=30)
        #
        # groupby_project = Alert.objects.filter(create_time__lt=end_time, create_time__gt=start_time).values(
        #     'project_id').annotate(alert_count=Count('id'))
        projects_report = phase_report.company_projects_phase_report(company_id, project_id, days)
        return Response(normalize_resp(projects_report))