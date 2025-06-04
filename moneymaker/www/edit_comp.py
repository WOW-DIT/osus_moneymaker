import frappe
from .models.subscription import SubscriptionModel
from .models.client import ClientModel
from frappe import _
import json

def get_context(context):
    context = {
        "content":getWebContent(),
        "profile": profile_info(),
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

@frappe.whitelist()
def profile_info():
    return ClientModel().profile_info()


@frappe.whitelist()
def edit_profile():
    data = json.loads(frappe.request.data)
    return ClientModel().edit_profile(data)

