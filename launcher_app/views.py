from django.http import HttpResponse


def redirect(request):
    return HttpResponse("Hello, World!")
