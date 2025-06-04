import frappe
from frappe import _
from datetime import datetime

def get_context(context):
    content = getWebContent()
    
    context.update({
        "content":content,
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
        "profile": get_profile(),
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
        content = frappe.get_doc('Educational Institution Website Content', content_id)
        return content
    

@frappe.whitelist()
def get_profile():
    user  = frappe.get_doc("User", frappe.session.user)
    return user
    

@frappe.whitelist()
def edit_profile():
    try:
        # institution = data.get("institution")
        first_name = frappe.form_dict.get("first_name")
        last_name = frappe.form_dict.get("last_name")
        password = frappe.form_dict.get("password", None)
        email = frappe.form_dict.get("email", "")
        phone = frappe.form_dict.get("phone", "")

        user = frappe.get_doc("User", frappe.session.user)

        if password:
            user.new_password = password
            
        user.mobile_no = phone
        user.phone = phone
        user.save()

        frappe.db.commit()
        return {"passed": True, "status": 200}

    except Exception as e:
        return {"passed": False, "status": 404, "error": str(e)}