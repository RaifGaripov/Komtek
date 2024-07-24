import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

from .models import RefBook, RefBookVersion, RefBookElement
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiParameter, OpenApiExample
from rest_framework import serializers


class RefBookListView(APIView):
    @extend_schema(
        description="Получение списка справочников",
        parameters=[
            OpenApiParameter(name='date', description='Дата в формате YYYY-MM-DD', required=False, type=str),
        ],
        examples=[
            OpenApiExample(
                'Пример',
                value={
                    "refbooks": [
                        {"id": 1, "code": "001", "name": "Справочник 1"},
                        {"id": 2, "code": "002", "name": "Справочник 2"},
                    ]
                },
                response_only=True,
                status_codes=["200"]
            )
        ],
        responses={
            200: inline_serializer(
                name="RefBookListResponse",
                fields={
                    "refbooks": serializers.ListField(
                        child=serializers.DictField(
                            child=serializers.CharField()
                        )
                    )
                }
            )
        }
    )
    def get(self, request):
        date_str = request.GET.get('date')
        refbooks = RefBook.objects.prefetch_related('refbookversion_set')
        filtered_refbooks = []

        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError as e:
                return Response({"error": e.args}, status=400)
            for refbook in refbooks:
                versions = refbook.refbookversion_set.all()
                if versions:
                    latest_version = max(versions, key=lambda v: v.start_date)
                    if latest_version.start_date <= date:
                        filtered_refbooks.append(refbook)
            refbooks = filtered_refbooks
        else:
            refbooks = RefBook.objects.all()
        data = [
            {
                "id": refbook.id,
                "code": refbook.code,
                "name": refbook.name,
            }
            for refbook in refbooks
        ]
        return Response({"refbooks": data})


class RefBookElementsView(APIView):
    @extend_schema(
        description="Получение элементов заданного справочника",
        parameters=[
            OpenApiParameter(name='version', description='Версия справочника', required=False, type=str),
        ],
        examples=[
            OpenApiExample(
                'Пример',
                value={
                    "elements": [
                        {"code": "001", "value": "Элемент 1"},
                        {"code": "002", "value": "Элемент 2"},
                    ]
                },
                response_only=True,
                status_codes=["200"]
            ),
        ],
        responses={
            200: inline_serializer(
                name="RefBookElementsResponse",
                fields={
                    "elements": serializers.ListField(
                        child=serializers.DictField(
                            child=serializers.CharField()
                        )
                    )
                }
            )
        }
    )
    def get(self, request, id):
        version = request.GET.get('version')
        if version:
            refbook_version = RefBookVersion.objects.filter(refbook_id=id, version=version).first()
        else:
            refbook_version = RefBookVersion.objects.filter(refbook_id=id, start_date__lte=datetime.now().date()).order_by('-start_date').first()

        if not refbook_version:
            return Response({"elements": []})

        elements = RefBookElement.objects.filter(refbook_version=refbook_version)
        data = [
            {
                "code": element.code,
                "value": element.value,
            }
            for element in elements
        ]
        return Response({"elements": data})

class RefBookElementCheckView(APIView):
    @extend_schema(
        description="Проверка наличия элемента в заданном справочнике",
        parameters=[
            OpenApiParameter(name='code', description='Код элемента', required=True, type=str),
            OpenApiParameter(name='value', description='Значение элемента', required=True, type=str),
            OpenApiParameter(name='version', description='Версия справочника', required=False, type=str),
        ],
        examples=[
            OpenApiExample(
                'Пример 1: Элемент присутствует',
                value={
                    "exists": True
                },
                response_only=True,
                status_codes=["200"]
            ),
            OpenApiExample(
                'Пример 2: Элемент отсутствует',
                value={
                    "exists": False
                },
                response_only=True,
                status_codes=["200"]
            ),
        ],
        responses={
            200: inline_serializer(
                name="RefBookElementCheckResponse",
                fields={
                    "exists": serializers.BooleanField(),
                    "error": serializers.CharField(required=False),
                }
            )
        }
    )
    def get(self, request, id):
        code = request.GET.get('code')
        value = request.GET.get('value')
        version = request.GET.get('version')
        if code and value:
            if version:
                refbook_version = RefBookVersion.objects.filter(refbook_id=id, version=version).first()
            else:
                refbook_version = RefBookVersion.objects.filter(refbook_id=id, start_date__lte=datetime.now().date()).order_by('-start_date').first()
            exists = RefBookElement.objects.filter(refbook_version=refbook_version, code=code, value=value).exists()
            return Response({'exists': exists})
        else:
            return Response({'error': 'Add "code" and "value" parameters'})
