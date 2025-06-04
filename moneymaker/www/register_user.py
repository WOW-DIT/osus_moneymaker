import frappe
from frappe import _
import json
from .models.client import ClientModel

def get_context(context):
    context = {
        "content": getWebContent(),
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
    }

    return context

@frappe.whitelist(allow_guest=True)
def getBlogger():
    content = frappe.db.sql(f""" select * from `tabBlogger` where disabled='false' """,as_dict=True)
    return content

@frappe.whitelist(allow_guest=True)
def getNews():
    content = frappe.db.sql(f""" select message from `tabNewsletter` Limit 3 """,as_dict=True)
    return content

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

    return ClientModel().register_user(data)

