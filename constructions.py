from json import JSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from api.models import *

## Получение данных стройки для модального окна "Уведомления"
@require_http_methods(["GET"])
def getConstructions(request):
    if request.method == "GET":
        # Получаем все объекты
        constructions_objects = Contractor.objects.all()

        # Используем множество для хранения уникальных названий
        unique_names = set(obj.NominativeName for obj in constructions_objects)

        # Преобразуем множество обратно в список для сериализации
        constructions_data = [{"Name": name} for name in unique_names]

        return JsonResponse({"message": "Данные успешно получены", "data": constructions_data}, status=200)

    return JsonResponse({"message": "Этот endpoint поддерживает только GET запросы."}, status=405)


def getRegion(request):
    if request.method == "GET":
        region_objects = Object.objects.all()

        unique_names = set(obj.Name for obj in region_objects)

        region_data = [{"Name": name} for name in unique_names]

        return JsonResponse({"message": "Данные успешно получены", "data": region_data}, status=200)

    return JsonResponse({"message": "Этот endpoint поддерживает только GET запросы."}, status=405)

def getInspector(request):
    if request.method == "GET":
        inspector_objects = Inspector.objects.all()

        unique_names = set(obj.NominativeName for obj in inspector_objects)

        inspector_data = [{"Name": name} for name in unique_names]

        return JsonResponse({"message": "Данные успешно получены", "data": inspector_data}, status=200)

    return JsonResponse({"message": "Этот endpoint поддерживает только GET запросы."}, status=405)

def getContractorMan(request):
    if request.method == "GET":
        contractorman_objects = ContractorMan.objects.all()

        unique_names = set(obj.NominativeName for obj in contractorman_objects)

        contractorman_data = [{"Name": name} for name in unique_names]
        
        return JsonResponse({"message": "Данные успешно получены", "data": contractorman_data}, status=200)

    return JsonResponse({"message": "Этот endpoint поддерживает только GET запросы."}, status=405)

def getWork(request):
    if request.method == "GET":
        work_objects = Work.objects.all()

        unique_names = set(obj.Name for obj in work_objects)

        work_data = [{"Name": name} for name in unique_names]
        
        return JsonResponse({"message": "Данные успешно получены", "data": work_data}, status=200)

    return JsonResponse({"message": "Этот endpoint поддерживает только GET запросы."}, status=405)
