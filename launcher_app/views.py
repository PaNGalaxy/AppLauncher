import json

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from jwt import decode
from requests import request as proxy_request

from launcher_app.auth import AuthManager
from launcher_app.galaxy import GalaxyManager


auth_manager = AuthManager()
galaxy_manager = GalaxyManager()


def _redirect_handler(request, session):
    match session:
        case "ucams":
            given_name_key = "given_name"
            session = auth_manager.ucams_session
        case "xcams":
            given_name_key = "givenName"
            session = auth_manager.xcams_session

    tokens = session.fetch_token(
        settings.UCAMS_TOKEN_URL,
        authorization_response=request.build_absolute_uri(),
        client_secret=settings.UCAMS_CLIENT_SECRET,
    )

    # TODO: verify signature seems important???
    user_info = decode(tokens["id_token"], options={"verify_signature": False})
    email = user_info["email"]
    given_name = user_info[given_name_key]

    try:
        user = get_user_model().objects.get(username=email)
    except get_user_model().DoesNotExist:
        user = get_user_model().objects.create_user(
            username=email, email=email, first_name=given_name
        )
    login(request, user)

    return redirect("/")


@require_GET
def ucams_redirect(request):
    return _redirect_handler(request, "ucams")


@require_GET
def xcams_redirect(request):
    return _redirect_handler(request, "xcams")


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


@login_required
@require_POST
def galaxy_launch(request):
    data = json.loads(request.body)
    galaxy_manager.launch_job(data.get("tool_id", None))

    return HttpResponse()


@login_required
@require_GET
def galaxy_monitor(_):
    galaxy_manager.monitor_jobs()
    return JsonResponse({})


@login_required
@require_POST
def galaxy_stop(request):
    data = json.loads(request.body)
    galaxy_manager.stop_job(data.get("job_id", None))

    return HttpResponse()


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
