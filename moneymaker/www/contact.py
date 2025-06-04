import frappe

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
def sendIssue(full_name, phone_number, email, subject, message):
    # institution = getInstitutionName()
    issue = frappe.new_doc("Issue")
    issue.full_name = full_name
    issue.phone_number = phone_number
    issue.subject = subject
    issue.raised_by = email
    issue.institution = "Osus"
    issue.description = message
    issue.issue_type = "Contact Us"
    issue.insert(ignore_permissions=True)