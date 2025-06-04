import frappe
import math
from frappe import _
from datetime import datetime

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = 'login'
        raise frappe.Redirect
    
    content = getWebContent()
    
    context.update({
        "content":content,
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
        "lang": getLang(),
        "support_details": get_issues(content.institution),
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
def get_issues(institution):
    status = frappe.local.request.args.get('status', 'Open').title()
    page_number = frappe.local.request.args.get('page', '1')
    page_number = int(page_number)
    page_size = 10
    page_offset = (page_number - 1) * page_size
    

    if status not in ["Open", "Closed"]:
        status = "Open"

    if status == "Open":
        status_list = ['Open', 'Replied', 'On Hold']
    else:
        status_list = ['Closed', 'Resolved']

    issues = frappe.db.sql("""
        SELECT i.name, i.subject, i.modified
        FROM `tabIssue` AS i
        WHERE i.status IN %s AND i.institution = %s AND i.issue_type = %s AND i.is_reply = 0
        ORDER BY i.modified DESC
    """, (tuple(status_list),institution, 'Ticket'), as_dict=True)


    page_issues = issues[page_offset:(page_offset + page_size)]
    number_of_pages = math.ceil(len(issues) / page_size)

    return {
        "issues": page_issues,
        "number_of_pages": number_of_pages,
        "status": status,
        "page_number": page_number,
    }