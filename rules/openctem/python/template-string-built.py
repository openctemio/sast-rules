from flask import render_template_string

def blog(request):
    body = request.POST["blog"]
    # ruleid: openctem.python.injection.template-from-request
    page = render_template_string(body)
    # ok: openctem.python.injection.template-from-request
    page2 = render_template_string("<p>{{ body }}</p>", body=body)
    return page, page2
