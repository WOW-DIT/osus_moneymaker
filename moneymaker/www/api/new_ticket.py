import frappe
from frappe import _

@frappe.whitelist()
def sendTicket():
    try:
        user = frappe.get_doc("User", frappe.session.user)
        full_name = user.full_name
        phone_number = user.mobile_no
        email = user.email
        subject = frappe.form_dict.get("subject")
        message = frappe.form_dict.get("message")
        is_reply = frappe.form_dict.get("is_reply", False)
        reference_ticket = frappe.form_dict.get("reference_ticket")
        institution = frappe.form_dict.get("institution")
        
        issue = frappe.new_doc("Issue")
        issue.full_name = full_name
        issue.phone_number = phone_number
        issue.subject = subject
        issue.raised_by = email
        issue.institution = institution
        issue.description = message
        issue.issue_type = "Ticket"

        if is_reply and reference_ticket:
            issue.is_reply = 1
            issue.reference_ticket = reference_ticket

        issue.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"passed": True, "message": "Message Sent", "url": f"support_det?id={issue.name}"}

    except Exception as e:
        return {"passed": False, "error": str(e)}