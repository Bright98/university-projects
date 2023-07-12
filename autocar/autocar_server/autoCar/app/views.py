from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from .models import *


@csrf_exempt
def last_stopCommand(request):
    if request.method == "POST":

        if request.POST:
            new_command = request.POST
        else:
            new_command = json.loads(request.body.decode("utf-8"))

        new_status = new_command["status"]

        _stop = Stop(status=new_status)
        _stop.save()

    elif request.method == "GET":
        _stop = Stop.objects.latest("id")

    context = {
        "status": str(_stop.status),
    }
    return JsonResponse(context, safe=False)


@csrf_exempt
def last_trafficLightCommand(request):
    if request.method == "POST":

        if request.POST:
            new_command = request.POST
        else:
            new_command = json.loads(request.body.decode("utf-8"))

        new_comm = new_command["command"]
        new_status = new_command["status"]

        _light = TrafficLight(command=new_comm, status=new_status)
        _light.save()

    elif request.method == "GET":
        _light = TrafficLight.objects.latest("id")

    context = {
        "command": str(_light.command),
        "status": str(_light.status),
    }
    return JsonResponse(context, safe=False)
