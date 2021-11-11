from datetime import datetime
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q

# Create your views here.
from rest_framework.response import Response

from SurveyApp.models import SurveyModel, ResultModel
from SurveyApp.serializers import SurveyDetailManageSerializer, SurveyListSerializer, SurveyCreateSerializer, \
    AskCreateSerializer, AskDetailManageSerializer, SurveyDetailSerializer, ResultSerializer, ResultCreateSerializer
from SurveyApp.service import Pagination


class AskCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = AskCreateSerializer

    def perform_create(self, serializer):
        survey = get_object_or_404(SurveyModel, createUser=self.request.user, pk=self.kwargs['surveyID'])
        ask = serializer.save()
        survey.askList.add(ask)
        return ask


class AskManageDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = AskDetailManageSerializer

    def get_queryset(self):
        survey = get_object_or_404(SurveyModel, createUser=self.request.user, pk=self.kwargs['surveyID'])
        return survey.askList.all()


class SurveyCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = SurveyCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(createUser=self.request.user)


class SurveyManageDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = SurveyDetailManageSerializer

    def get_queryset(self):
        return SurveyModel.objects.filter(createUser=self.request.user)


class SurveyListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = SurveyListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        date = datetime.now()
        return SurveyModel.objects.order_by('id').filter(startDate__lte=date, endDate__gte=date)


class SurveyGetAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = SurveyDetailSerializer

    def get_queryset(self):
        date = datetime.now()
        return SurveyModel.objects.filter(startDate__lte=date, endDate__gte=date)

class ResultGetAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = ResultSerializer
    pagination_class = Pagination
    lookup_field = 'user_id'

    def get_queryset(self):
        return ResultModel.objects.order_by('-id')



class ResultCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = ResultCreateSerializer
    queryset = ResultModel.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = ResultSerializer(instance=instance)
        return Response(instance_serializer.data)