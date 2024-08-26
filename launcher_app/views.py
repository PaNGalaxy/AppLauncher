from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from requests import request as proxy_request

from launcher_app.auth import AuthManager


auth_manager = AuthManager()


def redirect(request):
    return HttpResponse("Hello, World!")


def get_auth_urls(request):
    return JsonResponse(
        {
            "ucams": auth_manager.get_ucams_auth_url(),
            "xcams": auth_manager.get_xcams_auth_url(),
        }
    )


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
