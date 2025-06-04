import frappe
from frappe import _

@frappe.whitelist()
def get_issue():
    issue_id = frappe.local.request.args.get('id')
    
    if not issue_id or not frappe.db.exists("Issue", issue_id):
        frappe.throw("الصفحة غير موجودة!")

    issue = frappe.get_doc("Issue", issue_id)

    attachements = frappe.db.sql("""
        SELECT f.file_url, f.file_name, f.file_type
        FROM `tabFile` AS f
        WHERE f.attached_to_name = %s
    """, (issue.name,), as_dict=True)
    
    return {"details": issue, "attaches": attachements}


@frappe.whitelist()
def get_replies():
    issue_id = frappe.local.request.args.get('id')

    if not issue_id or not frappe.db.exists("Issue", issue_id):
        frappe.throw("الصفحة غير موجودة!")

    replies = frappe.db.sql("""
        SELECT i.name, i.subject, i.description, i.creation
        FROM `tabIssue` AS i
        WHERE i.is_reply = 1 AND i.reference_ticket = %s
        ORDER BY i.creation ASC
    """, (issue_id, ), as_dict=True)

    for rep in replies:
        attachements = frappe.db.sql("""
            SELECT f.file_url, f.file_name, f.file_type
            FROM `tabFile` AS f
            WHERE f.attached_to_name = %s
        """, (rep.name,), as_dict=True)

        rep.attaches = attachements

    return replies


@frappe.whitelist()
def sendReply():
    try:
        issue_id = frappe.local.request.args.get('id')

        user = frappe.get_doc("User", frappe.session.user)
        full_name = user.full_name
        phone_number = user.mobile_no
        email = user.email
        message = frappe.form_dict.get("message")
        institution = frappe.form_dict.get("institution")
        
        issue = frappe.new_doc("Issue")
        issue.full_name = full_name
        issue.phone_number = phone_number
        issue.subject = ""
        issue.raised_by = email
        issue.institution = institution
        issue.description = message
        issue.issue_type = "Ticket"

        if issue_id and frappe.db.exists("Issue", issue_id):
            issue.is_reply = 1
            issue.reference_ticket = issue_id

        issue.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"passed": True, "message": "Message Sent"}

    except Exception as e:
        return {"passed": False, "error": str(e)}

    



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