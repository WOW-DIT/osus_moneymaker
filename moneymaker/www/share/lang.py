import frappe

@frappe.whitelist()
def changeLanguage(lang):
    user = frappe.get_doc("User", frappe.session.user)

    user.language = lang
    user.save()