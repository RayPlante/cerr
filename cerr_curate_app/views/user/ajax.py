from django.http.response import HttpResponseBadRequest, HttpResponse

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from cerr_curate_app.views.user.forms.roles import roleForm
import json


def role_form(request):
    """Endpoint for role form value

    :param request:
    :return:
    """
    if request.method == "GET":
        return get_role_form(request)
    elif request.method == "POST":
        return save_role_form(request)


def get_role_form(request):
    """Gets the value of a data structure element

    Args:
        request:

    Returns:

    """
    if "role" not in request.GET:
        return HttpResponseBadRequest()

    try:
        # Create empty form instance
        newform = roleForm.createForm(request.GET["role"], data=None)
        # Create html and add it to the DOM
        # TODO
        role_html = (
            "<div id ='role_form'>Role: <b>" + request.GET["role"] + "   </b>"
        )  # add a remove button
        button_html = '<button type="button" onclick="removeRole()" class = "btn btn-outline-danger">Delete Role</button>'
        html_form = str(newform)
        html_form = role_html + button_html + html_form + "</div>"
        #     html_form = role_html+html_form
        json_data = json.dumps(html_form)
        # fancy tree = product class
        return HttpResponse(json_data, content_type="application/json")

    except (AccessControlError, DoesNotExist) as exc:
        return HttpResponseBadRequest(({"message": str(exc)}))


def save_role_form(request):

    """Post value"""
    pass
