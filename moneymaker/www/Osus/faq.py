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
        "faqs": get_faqs(content.institution),
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

def getSelectedCategory():
    return str(frappe.local.request.args.get('category'))


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
    

def get_faqs(institution="Osus"):
    faqs = frappe.db.sql("""
        SELECT f.order, f.question, f.answer
        FROM `tabFrequently Asked Questions` as f
        WHERE f.institution = %s
        ORDER BY f.order;
    """, (institution,), as_dict=True)
    return faqs