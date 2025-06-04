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
        "contact_channels": getContactChannels(content.name),
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
    

@frappe.whitelist(allow_guest=True)
def getContactChannels(content_id):
    channels = frappe.db.sql(f"""
        SELECT c.title, c.image, c.type, c.content
        FROM `tabContact Channels` AS c
        WHERE c.parent=%s 
        ORDER BY c.idx""",(content_id),as_dict=True,)
    
    return channels


@frappe.whitelist(allow_guest=True)
def sendIssue():
    try:
        full_name = frappe.form_dict.get("full_name")
        phone_number = frappe.form_dict.get("phone_number")
        email = frappe.form_dict.get("email")
        subject = frappe.form_dict.get("subject")
        message = frappe.form_dict.get("message")
                
        institution = getInstitutionName()
        issue = frappe.new_doc("Issue")
        issue.full_name = full_name
        issue.phone_number = phone_number
        issue.subject = subject
        issue.raised_by = email
        issue.institution = institution
        issue.description = message
        issue.issue_type = "Contact Us"
        issue.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"passed": True, "message": "Message Sent"}

    except Exception as e:
        return {"passed": False, "error": str(e)}
