from django.http import HttpResponse

def view(request):
    rendered = "<p>" + request.GET.get("q", "") + "</p>"
    # ruleid: openctem.python.django.httpresponse-unescaped
    return HttpResponse(rendered)

def ping(request):
    # ok: openctem.python.django.httpresponse-unescaped
    return HttpResponse("pong")
