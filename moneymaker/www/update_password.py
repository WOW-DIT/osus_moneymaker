import frappe
from frappe.utils.password import update_password

from frappe import _

def get_context(context):
    context = {
        "content":getWebContent(),
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


@frappe.whitelist(allow_guest=True)
def update_pass(new_password):
    key = frappe.local.request.args.get('key')
    email = frappe.local.request.args.get('email')
    missingKey = key is None or key == ""
    missingEmail = email is None or email == ""

    if missingKey:
        return {"status": 500, "error": "Missing or Invalid key"}
    
    if missingEmail or frappe.get_value("User", {"email": str(email).lower().strip()}) is None:
        return {"status": 500, "error": "Missing or Invalid email"}
        
    email = str(email).lower().strip()
        
    update_password()
    
    
