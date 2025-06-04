import frappe

from frappe import _
import json
from .models.client import ClientModel

def get_context(context):
    context = {
        "content":getWebContent(),
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
    }

    return context


@frappe.whitelist(allow_guest=True)
def getWebContent():
    content = {}
    main_content = frappe.get_doc("Website Manager", "Website Manager")
    content["main"] = main_content
    return content


@frappe.whitelist(allow_guest=True)
def isLoggedIn():
    return frappe.session.user != "Guest"


@frappe.whitelist(allow_guest=True)
def register():
    data = json.loads(frappe.request.data)

    return ClientModel().register_comp(data)

