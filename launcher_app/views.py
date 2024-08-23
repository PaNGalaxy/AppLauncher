from django.http import HttpResponse, StreamingHttpResponse
from requests import request as proxy_request


def redirect(request):
    return HttpResponse("Hello, World!")


def client_proxy(request):
    response = proxy_request(
        "GET",  # TODO: Support other HTTP methods
        f"http://localhost:5173{request.path}",
        headers=request.headers,
        stream=True,
        # TODO: Support params & data in requests
    )

    return StreamingHttpResponse(response.raw)
