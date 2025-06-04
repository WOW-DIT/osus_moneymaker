import frappe
from frappe import _
from frappe.twofactor import confirm_otp_token
from frappe.auth import LoginManager


def get_context(context):
    if frappe.session.user != "Guest":
        frappe.local.flags.redirect_location = '/'
        raise frappe.Redirect

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
def confirm_otp(email, password, otp, tmp_id):
    try:
        login_manager = LoginManager()
        login_manager.user = email
        login_manager.authenticate(email, password)
  

        auth = confirm_otp_token(login_manager, otp, tmp_id)
        if auth:
            login_manager.post_login()
            return {"status": 200, "message": auth}
        
        return {"status": 500, "message": auth}
    except frappe.AuthenticationError as e:
        return {"status": 404, "error": "User not found"}
