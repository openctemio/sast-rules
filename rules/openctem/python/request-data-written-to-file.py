def save(request):
    code = request.POST.get('code')
    f = open("playground/main.py", "w")
    # ruleid: openctem.python.injection.request-data-written-to-file
    f.write(code)
    # ok: openctem.python.injection.request-data-written-to-file
    f.write("# generated\n")
