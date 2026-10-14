def view(request, response, token):
    # ruleid: openctem.python.web.cookie-not-secure
    response.set_cookie('userid', token, max_age=31449600, secure=False)
    # ruleid: openctem.python.web.cookie-not-secure
    response.set_cookie("email", token)
    # ok: openctem.python.web.cookie-not-secure
    response.set_cookie("sid", token, secure=True, httponly=True, samesite="Lax")
    return response
