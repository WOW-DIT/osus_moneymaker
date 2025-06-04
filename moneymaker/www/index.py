import frappe
from frappe import _

def get_context(context):
    context = {
        "content": getWebContent(),
        "services": get_services(),
        "feedback": get_feedback(),
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
def get_features(f_table):
    features = []
    for f in f_table:
        feature = frappe.get_doc("Osus Features", f.reference)

        points = frappe.db.sql("""
            SELECT p.title, p.description, p.image
            FROM `tabFeature Points` AS p
            WHERE p.parent = %s
        """,(feature.name), as_dict=True)

        features.append({
            "feature": {"title": feature.title, "icon": feature.icon},
            "points": points,
        })


    return features


@frappe.whitelist(allow_guest=True)
def get_solutions(s_table):
    solutions = []
    for s in s_table:
        solution = frappe.get_doc("Osus Solutions", s.reference)

        points = frappe.db.sql("""
            SELECT p.title, p.description
            FROM `tabFeature Points` AS p
            WHERE p.parent = %s
        """,(solution.name), as_dict=True)

        solution.append({
            "feature": {"title": solution.title, "icon": solution.icon},
            "points": points,
        })


    return solutions

@frappe.whitelist(allow_guest=True)
def join_request(name, email, phone, subject, message):
    request = frappe.new_doc("Osus Contacts")

    request.name = name
    request.email = email
    request.phone = phone
    request.subjet = subject
    request.message = message

    request.insert(ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def get_services():
    services = frappe.db.sql("""
        SELECT s.name, s.description, s.active, s.image
        FROM `tabOsus Service` AS s
        WHERE s.active = 1;
    """, as_dict=True)

    return services


@frappe.whitelist(allow_guest=True)
def get_feedback():
    feedback = frappe.db.sql("""
        SELECT f.feedback, f.rating, f.client_name, f.image
        FROM `tabWebsite Feedback` AS f;
    """, as_dict=True)

    return feedback