import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def sendIssue():
    try:
        full_name = frappe.form_dict.get("full_name")
        phone_number = frappe.form_dict.get("phone_number")
        email = frappe.form_dict.get("email")
        subject = frappe.form_dict.get("subject")
        message = frappe.form_dict.get("message")
        institution = frappe.form_dict.get("institution")
                
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
