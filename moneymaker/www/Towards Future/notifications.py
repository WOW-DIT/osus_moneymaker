import frappe
from datetime import datetime
from frappe import _
from frappe.desk.doctype.notification_log.notification_log import get_notification_logs, mark_as_read

def get_context(context):
    content = getWebContent()

    context.update({
        "content":content,
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
        "lang": getLang(),
        "notifs": get_notifs(),
        "year": datetime.today().year,
    })
    
    return context

def getLang():
    if frappe.session.user != "Guest":
        user = frappe.get_doc("User", frappe.session.user)
        return user.language
    
    return "en"


def getInstitutionName():
    brand_name = getBrandName()
    with open(f"/home/frappe/frappe-bench/apps/moneymaker/moneymaker/www/{brand_name}/name.txt", "r") as f:
        institution = f.read()
    return institution


@frappe.whitelist(allow_guest=True)
def isLoggedIn():
    return frappe.session.user != "Guest"

@frappe.whitelist()
def getBrandName():
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    brand_name = dir_path.split("/")[len(dir_path.split("/")) - 1]
    return brand_name

@frappe.whitelist(allow_guest=True)
def getWebContent():
    brand_name = getBrandName()
    content_id = frappe.get_value("Educational Institution Website Content", {"brand_name": brand_name})
    if content_id is not None:
        content = frappe.get_doc('Educational Institution Website Content',content_id)
        return content

def get_notifs():
    notifs = get_notification_logs(limit=10)
    return notifs["notification_logs"]

@frappe.whitelist()
def get_all_notifs():
    notifs = get_notification_logs(limit=100)
    return notifs["notification_logs"]


@frappe.whitelist()
def mark_as_read():
    docname = frappe.form_dict.get("docname")
    try:
        mark_as_read(docname)
        return {"status": 200}

    except:
        return {"status": 500}