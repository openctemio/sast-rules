from django.views.decorators.csrf import csrf_exempt, csrf_protect

# ruleid: openctem.python.django.csrf-exempt
@csrf_exempt
def transfer(request):
    return None

# ok: openctem.python.django.csrf-exempt
@csrf_protect
def update(request):
    return None
