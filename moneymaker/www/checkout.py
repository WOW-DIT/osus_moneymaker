import frappe
from .models.subscription import SubscriptionModel
from frappe import _

def get_context(context):
    context = {
        "content":getWebContent(),
        "logged_in": isLoggedIn(),
        "payment_methods": payment_methods(),
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
def saved_order(package_name, session_id, recurring_type="1"):
    order = SubscriptionModel().saved_order(package_name, session_id, recurring_type)
    return order
    

@frappe.whitelist(allow_guest=True)
def payment_methods():
    methods = SubscriptionModel().payment_methods()
    return methods

@frappe.whitelist()
def apply_coupon(code):
    try:
        coupon = SubscriptionModel().apply_coupon(code)
        return coupon
    except Exception as e:
        return {"status": 500, "error": str(e)}