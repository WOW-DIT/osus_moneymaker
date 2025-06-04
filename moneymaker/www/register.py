import frappe
from frappe import _

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
    content["features"] = main_content.features
    content["solutions"] = main_content.solutions
    content["goals"] = main_content.goals
    content["partners"] = main_content.partners
    return content


@frappe.whitelist(allow_guest=True)
def isLoggedIn():
    return frappe.session.user != "Guest"


@frappe.whitelist(allow_guest=True)
def join_request(name, email, phone, subject, message):
    request = frappe.new_doc("Osus Contacts")

    request.name = name
    request.email = email
    request.phone = phone
    request.subjet = subject
    request.message = message

    request.insert(ignore_permissions=True)
