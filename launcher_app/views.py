from django.http import HttpResponse, StreamingHttpResponse
from requests import request as proxy_request


def redirect(request):
    return HttpResponse("Hello, World!")


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
