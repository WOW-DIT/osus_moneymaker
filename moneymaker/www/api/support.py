import frappe
import math
from frappe import _

@frappe.whitelist()
def get_issues(institution):
    status = frappe.local.request.args.get('status', 'Open').title()
    page_number = frappe.local.request.args.get('page', '1')
    page_number = int(page_number)
    page_size = 10
    page_offset = (page_number - 1) * page_size
    

    if status not in ["Open", "Closed"]:
        status = "Open"

    if status == "Open":
        status_list = ['Open', 'Replied', 'On Hold']
    else:
        status_list = ['Closed', 'Resolved']

    issues = frappe.db.sql("""
        SELECT i.name, i.subject, i.modified
        FROM `tabIssue` AS i
        WHERE i.status IN %s AND i.institution = %s AND i.issue_type = %s AND i.is_reply = 0
        ORDER BY i.modified DESC
    """, (tuple(status_list),institution, 'Ticket'), as_dict=True)


    page_issues = issues[page_offset:(page_offset + page_size)]
    number_of_pages = math.ceil(len(issues) / page_size)

    return {
        "issues": page_issues,
        "number_of_pages": number_of_pages,
        "status": status,
        "page_number": page_number,
    }