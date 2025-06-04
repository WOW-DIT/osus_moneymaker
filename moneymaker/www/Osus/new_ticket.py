import frappe
from frappe import _
from datetime import datetime

def get_context(context):
    content = getWebContent()
    context.update({
        "content":content,
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
        "lang": getLang(),
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
    

@frappe.whitelist()
def sendTicket():
    try:
        user = frappe.get_doc("User", frappe.session.user)
        full_name = user.full_name
        phone_number = user.mobile_no
        email = user.email
        subject = frappe.form_dict.get("subject")
        message = frappe.form_dict.get("message")
        is_reply = frappe.form_dict.get("is_reply", False)
        reference_ticket = frappe.form_dict.get("reference_ticket")
        
        institution = getInstitutionName()
        issue = frappe.new_doc("Issue")
        issue.full_name = full_name
        issue.phone_number = phone_number
        issue.subject = subject
        issue.raised_by = email
        issue.institution = institution
        issue.description = message
        issue.issue_type = "Ticket"

        if is_reply and reference_ticket:
            issue.is_reply = 1
            issue.reference_ticket = reference_ticket

        issue.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"passed": True, "message": "Message Sent", "url": f"support_det?id={issue.name}"}

    except Exception as e:
        return {"passed": False, "error": str(e)}