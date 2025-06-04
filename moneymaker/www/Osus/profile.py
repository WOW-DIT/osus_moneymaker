import frappe
from datetime import datetime
from frappe import _

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = 'login'
        raise frappe.Redirect
    
    content = getWebContent()
    
    context.update({
        "selected_category": getSelectedCategory(),
        "content":content,
        "courses":getCourses(),
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
        "profile": get_profile(),
        "lang": getLang(),
        "year": datetime.today().year,
    })
    
    return context


def getLang():
    if frappe.session.user != "Guest":
        user = frappe.get_doc("User", frappe.session.user)
        return user.language
    
    return "en"

def getInstitutionName():
    brand_name = getBrandName()
    with open(f"/home/frappe/frappe-bench/apps/moneymaker/moneymaker/www/{brand_name}/name.txt", "r") as f:
        institution = f.read()
    return institution

def getSelectedCategory():
    return str(frappe.local.request.args.get('category'))

@frappe.whitelist(allow_guest=True)
def isLoggedIn():
    return frappe.session.user != "Guest"

@frappe.whitelist()
def getBrandName():
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    brand_name = dir_path.split("/")[len(dir_path.split("/")) - 1]
    return brand_name

@frappe.whitelist(allow_guest=True)
def getWebContent():
    brand_name = getBrandName()
    content_id = frappe.get_value("Educational Institution Website Content", {"brand_name": brand_name})
    if content_id is not None:
        content = frappe.get_doc('Educational Institution Website Content',content_id)
        return content


@frappe.whitelist(allow_guest=True)
def getCourses():
    completed = []
    in_progress = []


    institution = getInstitutionName()
    user = frappe.session.user
    courses = frappe.db.sql(f""" 
        SELECT
            c.name,
            c.course_name,
            c.course_name_ar,
            c.category,
            c.hero_image,
            cp.purchase_date AS date,
            COUNT(ci.name) AS total_items,
            CAST(SUM(CASE WHEN cis.state = 'Finished' THEN 1 ELSE 0 END) AS INT) AS completed_items,
            ROUND((SUM(CASE WHEN cis.state = 'Finished' THEN 1 ELSE 0 END) / COUNT(ci.name)) * 100, 2) AS completion_percentage,
            ROUND(c.price * (1 - c.discount / 100), 2) AS price
        FROM `tabCourse` AS c
        LEFT JOIN `tabCourse Purchase` AS cp ON c.name = cp.course
        LEFT JOIN `tabCourse Item` AS ci ON ci.course = c.name
        LEFT JOIN `tabCourse Item State` AS cis ON cis.item = ci.name AND cis.user = %s
        WHERE
            cp.name IS NOT NULL
            AND cp.user = %s
            AND cp.institution = %s
            AND cp.is_refunded = 0
        GROUP BY c.name""",
        (user, user, institution),
        as_dict=True
    )

    for c in courses:
        if c.completion_percentage < 100:
            in_progress.append(c)
        else:
            finished_survey = finishedSurvey(c.name)
            c.cert_url = certificate_link(finished_survey, c.name)

            completed.append(c)
            
    return {"in_progress": in_progress, "completed": completed}


def finishedSurvey(course_id):
    user = frappe.session.user

    if frappe.db.exists("User Survey Answer", {"user": user, "course": course_id}):
        return True
    
    return False


def certificate_link(finished, course_id):
    if finished:
        user = frappe.session.user
        
        cert_id = frappe.get_value("Certificate", {"user": user, "course": course_id})
        if cert_id is not None:
            # cert = frappe.get_doc("Certificate", cert_id)
            # return cert.get_url()
            return f"https://osus.wowdigital.sa/api/method/frappe.utils.print_format.download_pdf?doctype=Certificate&name={cert_id}&format=Certificate"
        
    return None


@frappe.whitelist()
def get_profile():
    user  = frappe.get_doc("User", frappe.session.user)
    return user