import traceback
import pytz
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import viewsets, serializers, status, views
from rest_framework.decorators import action as detail_route, renderer_classes
from rest_framework.decorators import action as list_route
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from ledger_api_client.settings_base import TIME_ZONE
from boranga import settings
from django.core.cache import cache
from django.urls import reverse
from django.shortcuts import redirect
from boranga.helpers import is_customer, is_internal
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer
from copy import deepcopy
from django.shortcuts import render, redirect, get_object_or_404
from boranga.components.species_and_communities.models import (
    GroupType,
    Species,
    ConservationList,
    ConservationStatus,
    ConservationCategory,
    ConservationCriteria,
    Taxonomy,
)
from boranga.components.species_and_communities.serializers import (
    ListSpeciesSerializer,
)

import logging

logger = logging.getLogger(__name__)

class GetGroupTypeDict(views.APIView):
    renderer_classes = [JSONRenderer, ]

    def get(self, request, format=None):
        group_type_list = []
        group_types = GroupType.objects.all().order_by('name')
        if group_types:
            for g in group_types:
                group_type_list.append({'key': g.id,'value': g.name})
        return Response(group_type_list)

class GetScientificNameDict(views.APIView):
    renderer_classes = [JSONRenderer, ]

    def get(self, request, format=None):
        group_type = request.GET.get('group_type_name','')
        name_list = []
        if group_type:
            species = Species.objects.filter(group_type__name=group_type)
            if species:
                for s in species:
                    name_list.append({'species_id': s.id,'scientific_name': s.scientific_name,'common_name':s.common_name})
        return Response(name_list)

class SpeciesFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        print(request.GET)
        total_count = queryset.count()
        # filter_group_type
        filter_group_type = request.GET.get('filter_group_type')
        if filter_group_type:
            queryset = queryset.filter(group_type__name=filter_group_type)
        # filter_scientific_name
        filter_scientific_name = request.GET.get('filter_scientific_name')
        if filter_scientific_name and not filter_scientific_name.lower() == 'all':
            queryset = queryset.filter(scientific_name=filter_scientific_name)

        filter_common_name = request.GET.get('filter_common_name')
        if filter_common_name and not filter_common_name.lower() == 'all':
            queryset = queryset.filter(common_name=filter_common_name)

        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        try:
            queryset = super(SpeciesFilterBackend, self).filter_queryset(request, queryset, view)
        except Exception as e:
            print(e)
        setattr(view, '_datatables_total_count', total_count)
        return queryset

class SpeciesRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        return super(SpeciesRenderer, self).render(data, accepted_media_type, renderer_context)

class SpeciesPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (SpeciesFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (SpeciesRenderer,)
    queryset = Species.objects.none()
    serializer_class = ListSpeciesSerializer
    page_size = 10

    def get_queryset(self):
        #request_user = self.request.user
        qs = Species.objects.none()

        if is_internal(self.request):
            qs = Species.objects.all()

        return qs

    @list_route(methods=['GET',], detail=False)
    def species_internal(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListSpeciesSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)