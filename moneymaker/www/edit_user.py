import frappe
# from ....education.education.subscriptions.subscription import SubscriptionModel
from .models.subscription import SubscriptionModel
from .models.client import ClientModel
from frappe import _

def get_context(context):
    context = {
        "content":getWebContent(),
        "logged_in": isLoggedIn(),
        "subs": subs(),
        "profile": profile_info(),
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
def subs():
    subs = SubscriptionModel().get_subscriptions(frappe.session.user)
    return subs


# @frappe.whitelist()
# def subs():
#     user = frappe.session.user
#     subs = SubscriptionModel().individual_subscriptions(user)
#     return subs