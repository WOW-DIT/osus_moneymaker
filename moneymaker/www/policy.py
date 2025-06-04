import frappe

from frappe import _

def get_context(context):
    context = {
        "content":getWebContent(),
        "user": frappe.session.user,
    }

    return context


@frappe.whitelist(allow_guest=True)
def getWebContent():
    content = {}
    main_content = frappe.get_doc("Website Manager", "Website Manager")
    content["main"] = main_content
    content["terms"] = get_terms(main_content.privacy_policy)
    return content

def get_terms(terms_docs):
    terms = []
    for index, t in enumerate(terms_docs):
        term = frappe.get_doc("Osus Terms and Conditions", t.reference)

        points = frappe.db.sql("""
            SELECT p.title, p.is_point
            FROM `tabFeature Points` AS p
            WHERE p.parent = %s
            ORDER BY p.idx
        """,(term.name), as_dict=True)

        terms.append({
            "term": {"title": term.condition, "index": index+1},
            "points": points,
        })

    return terms