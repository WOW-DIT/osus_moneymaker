import frappe
from frappe.utils import get_url, random_string, now_datetime
from frappe.utils.password import update_password

from frappe import _
# from frappe.core.doctype.user.user import update_password

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
def reset_password(email: str, default_url="update-password"):
    try:
        email = email.lower().strip()
        user_id = frappe.get_value("User", {"email": email})

        if user_id is None:
            raise frappe.exceptions.NotFound("User Not Found!")
        
        else:
            key = random_string(32)
            user = frappe.get_doc("User", email)
            user.db_set("reset_password_key", key)
            user.db_set("last_reset_password_key_generated_on", now_datetime())
            link = user.reset_password(send_email=True, default_url=default_url)

            return {
                "status": 200,
                "link": link,
                "key": key,
                # "email": email,
            }
    except Exception as e:
        return {
            "status": 500,
            "error": e,
        }