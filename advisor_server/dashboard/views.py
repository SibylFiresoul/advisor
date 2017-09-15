# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django import forms
from django.contrib.admin.views.decorators import staff_member_required

from suggestion.models import Study
from suggestion.models import Trial


def index(request):
  try:
    studies = [study.to_json() for study in Study.objects.all()]
  except Study.DoesNotExist:
    studies = []

  try:
    trials = [trial.to_json() for trial in Trial.objects.all()]
  except Study.DoesNotExist:
    trials = []

  context = {"success": True, "studies": studies, "trials": trials}
  return render(request, "index.html", context)


@csrf_exempt
def v1_studies(request):
  if request.method == "POST":
    name = request.POST.get("name", "")
    study_configuration = request.POST.get("study_configuration", "")

    data = {"name": name, "study_configuration": study_configuration}

    url = "http://127.0.0.1:8000/suggestion/v1/studies"
    response = requests.post(url, json=data)
    messages.info(request, response.content)
    return redirect("index")
  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_study(request):
  context = {}
  return render(request, "index.html", context)


@csrf_exempt
def v1_trials(request):
  if request.method == "POST":
    study_id = request.POST.get("study_id", "")
    name = request.POST.get("name", "")

    data = {"name": name}

    url = "http://127.0.0.1:8000/suggestion/v1/studies/{}/trials".format(
        study_id)
    response = requests.post(url, json=data)
    messages.info(request, response.content)
    return redirect("index")
  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_trial(request, study_id, trial_id):
  context = {}
  return render(request, "index.html", context)
