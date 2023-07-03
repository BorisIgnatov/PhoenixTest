import asyncio
import json
import base64

from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import  render, redirect
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from .services.api_call import call_api


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/users/qwe")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/registration.html",
                  context={"register_form": form})


@sync_to_async
def get_user_from_request(request: HttpRequest) -> CustomUser | AnonymousUser | None:
    return request.user if bool(request.user) else None


async def index(request):
    user = await get_user_from_request(request)
    if not user.is_authenticated:
        return HttpResponse('authentication error', status=401)
    res = await asyncio.gather(call_api(user))
    users = json.loads(res[0])
    return render(request, "integration.html", context={'users': users.get('users')})


def _check_user(hash_string: str):
    decoded = base64.b64decode(hash_string.split()[1])
    decoded = decoded.decode()
    username = decoded.split(':')[0]
    password = decoded.split(':')[1]
    try:
        user = CustomUser.objects.get(username=username)
        if password != user.password:
            return False
    except ObjectDoesNotExist:
        return False
    print(user.username)
    return True


@csrf_exempt
def get_users(request):
    if request.method == "POST":

        if request.POST.get('request_id') != 'e1477272-88d1-4acc-8e03-7008cdedc81e':
            return HttpResponse('error', status=400)

        if not request.META['HTTP_AUTHORIZATION']:
            return HttpResponse('error', status=401)

        if not _check_user(request.META['HTTP_AUTHORIZATION']):
            return HttpResponse('error', status=401)

        users = CustomUser.objects.all()
        response = {'users': []}
        for user in users:
            user_info = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                         'phone': user.phone, 'photo': request.build_absolute_uri(user.image.url), 'club_id': user.club_id}
            response['users'].append(user_info)
        return HttpResponse(json.dumps(response))
    else:
        return HttpResponse('error', status=400)
