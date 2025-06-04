import frappe
from frappe import _
from datetime import datetime

def get_context(context):
    content = getWebContent()
    categories = getCategories(content.institution)
    category = categories[0].category if len(categories) > 0 else None
    context.update({
        "selected_category": getSelectedCategory(),
        "content":content,
        "category":categories,
        "course":getCourses(institution=content.institution, category=category),
        "number_of_students": numberOfStudents(content.institution),
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
        "lang": getLang(),
        "year": datetime.today().year,
    })
    cats = []

    for c in context["category"]:
        cats.append(c.category)

    context["contains_category"] = context["selected_category"] in cats
    
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
def numberOfStudents(institution="Osus"):
    content = frappe.db.sql(f""" SELECT SUM(number_of_students) as students FROM `tabCourse` WHERE institution=%s """,(institution),as_dict=True)

    if len(content) > 0 and content[0]["students"] is not None:
        number_of_students = int(content[0]["students"])
    else:
        number_of_students = 0

    digits = str(number_of_students)
    first_digit = digits[0]

    full_str = ""
    full_str += first_digit

    for _ in range(len(digits)-1):
        full_str += "0"

    return full_str


@frappe.whitelist(allow_guest=True)
def getCategories(institution):
    categories = frappe.db.sql(f"""
        SELECT a.category, a.image
        FROM `tabCourse Category` AS a
        JOIN 
        `tabCourse` AS c ON a.category = c.category AND c.activee = 1
        where c.institution = %s
        GROUP BY c.category
        ORDER BY a.name """,
        (institution),as_dict=True,)

    return categories

@frappe.whitelist(allow_guest=True)
def getCourses(institution, category, page=1):
    page_size = 6

    page = int(page)
    
    page_number = int((page - 1) * page_size)
    
    courses = frappe.db.sql(f""" 
        SELECT  c.name, c.course_name, c.course_name_ar, c.hero_image, c.description, c.description_ar, c.created_by, c.price AS priceold, c.category,
        COALESCE(AVG(r.rating), 0) AS average_rating, COUNT(r.rating) AS rate_count,
        COALESCE(FLOOR(AVG(r.rating)), 0) AS full_stars, ROUND(c.price * (1 - c.discount / 100), 2) AS price,
        CASE WHEN AVG(r.rating) - FLOOR(AVG(r.rating)) >= 0.5 THEN 1 ELSE 0 END AS half_star, 5 AS total_stars
        FROM `tabCourse` AS c
        LEFT JOIN `tabCourse Ratings` AS r ON c.name = r.course
        WHERE c.institution = %s AND c.standalone = 1 AND c.category = %s  AND c.activee = 1
        GROUP BY c.name LIMIT %s, %s""",
        (institution, category, page_number, page_size),
        as_dict=True
    )
    return courses