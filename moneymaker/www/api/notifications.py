import frappe
from frappe import _
from frappe.desk.doctype.notification_log.notification_log import get_notification_logs, mark_as_read

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