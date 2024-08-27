import json

from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from requests import request as proxy_request

from launcher_app.auth import AuthManager
from launcher_app.galaxy import GalaxyManager


auth_manager = AuthManager()
galaxy_manager = GalaxyManager(auth_manager)


@require_GET
def ucams_redirect(request):
    user_info = auth_manager.redirect_handler(request, "ucams")

    email = user_info["email"]
    given_name = user_info["given_name"]

    auth_manager.login(request, email, given_name)

    return redirect("/")


@require_GET
def xcams_redirect(request):
    user_info = auth_manager.redirect_handler(request, "xcams")

    email = user_info["email"]
    given_name = user_info["givenName"]

    auth_manager.login(request, email, given_name)

    return redirect("/")


@ensure_csrf_cookie
@require_GET
def get_user(request):
    given_name = None
    if request.user.is_authenticated:
        given_name = request.user.first_name

    return JsonResponse(
        {
            "given_name": given_name,
            "is_logged_in": given_name is not None,
            "ucams": auth_manager.get_ucams_auth_url(),
            "xcams": auth_manager.get_xcams_auth_url(),
        }
    )


def _create_galaxy_error(exception):
    return JsonResponse({"error": str(exception)}, status=500)


@login_required
@require_POST
def galaxy_launch(request):
    try:
        data = json.loads(request.body)
        galaxy_manager.launch_job(data.get("tool_id", None))

        return HttpResponse()
    except Exception as e:
        return _create_galaxy_error(e)


@login_required
@require_GET
def galaxy_monitor(_):
    try:
        return JsonResponse({"jobs": galaxy_manager.monitor_jobs()})
    except Exception as e:
        return _create_galaxy_error(e)


@login_required
@require_POST
def galaxy_stop(request):
    try:
        data = json.loads(request.body)
        galaxy_manager.stop_job(data.get("job_id", None))

        return HttpResponse()
    except Exception as e:
        return _create_galaxy_error(e)


@require_GET
def client_proxy(request):
    proxy_response = proxy_request(
        "GET",
        f"http://localhost:5173{request.path}",
        headers=request.headers,
        stream=True,
    )

    response = StreamingHttpResponse(proxy_response.raw)
    response["Content-Type"] = proxy_response.headers["Content-Type"]

    return response
