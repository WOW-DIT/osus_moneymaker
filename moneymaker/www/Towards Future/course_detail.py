import frappe
from frappe import _
from datetime import datetime

def get_context(context):
    content = getWebContent()
    context.update({
        "content":content,
        "has_purchased": hasPurchased(),
        "category":getCategories(content.institution),
        "course":singleCourse(content.institution),
        "course_items": courseItems(),
        "course_langs": courseLangs(),
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
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
    with open("/Osus/name.txt", "r") as f:
        institution = f.read()
    return institution

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

# @frappe.whitelist(allow_guest=True)
# def getplans():
#     plans = frappe.db.sql(f"""  select name from `tabSystem plans` """,as_dict=True) 
#     content = []
#     for plan in plans:
#         p = frappe.get_doc("System plans" , plan)
#         content.append(p)
#     return content


# @frappe.whitelist(allow_guest=True)
# def numberOfStudents():
    
#     content = frappe.db.sql(f""" SELECT SUM(number_of_students) as students FROM `tabCourse` WHERE institution=%s """,(institution),as_dict=True)
#     if len(content) > 0:
#         number_of_students = int(content[0]["students"])
#     else:
#         number_of_students = 0

#     digits = str(number_of_students)
#     first_digit = digits[0]

#     full_str = ""
#     full_str += first_digit

#     for _ in range(len(digits)-1):
#         full_str += "0"
#     return full_str

@frappe.whitelist(allow_guest=True)
def getCategories(institution="Osus"):
        # SELECT name, hero_image, description, created_by, price
        # FROM `tabCourse`
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
def courseLangs():
    lang = ""
    course_id=frappe.local.request.args.get('id')
    langs = frappe.db.sql(f"""
        SELECT cl.language
        FROM `tabCourse Languages` AS cl
        WHERE cl.parent=%s
        ORDER BY cl.idx """,(course_id),as_dict=True,)
    
    for i, l in enumerate(langs):
        lang += _(l.language)
        if i < len(langs)-1:
            lang += "/"

    return lang
    
@frappe.whitelist(allow_guest=True)
def courseItems():
    course_id=frappe.local.request.args.get('id')

    items = frappe.db.sql(f"""
        SELECT ci.title, ci.description, (ci.time/60) AS time, ci.order,
        CAST((ci.time/60) AS INT) AS minutes,
        CAST(((ci.time/60) - CAST((ci.time/60) AS INT)) * 60 AS INT) AS seconds
        FROM `tabCourse Item` AS ci
        WHERE ci.course=%s
        ORDER BY ci.order """,(course_id),as_dict=True,)
    
    # items = frappe.db.sql(f"""
    #     SELECT title, description, time, order
    #     FROM `tabCourse Item`
    #     WHERE course=%s 
    #     GROUP BY order """,(course_id),as_dict=True)
    
    return items

@frappe.whitelist(allow_guest=True)
def hasPurchased():
    course_id=frappe.local.request.args.get('id')
    hp = frappe.db.exists(
        "Course Purchase",
        {"user": frappe.session.user, "course": course_id, "is_refunded": 0},
    )

    return hp


@frappe.whitelist(allow_guest=True)
def singleCourse(institution="Osus"):
    id=frappe.local.request.args.get('id')
    course = frappe.db.sql(f"""
        SELECT c.name, c.course_name, c.course_name_ar, c.course_name_ar, c.hero_image, c.description, c.description_ar, c.created_by, c.price AS priceold, c.category,
        COALESCE(AVG(r.rating), 0) AS average_rating, COUNT(r.rating) AS rate_count,
        COALESCE(FLOOR(AVG(r.rating)), 0) AS full_stars, ROUND(c.price * (1 - c.discount / 100), 2) AS price,
        CASE WHEN AVG(r.rating) - FLOOR(AVG(r.rating)) >= 0.5 THEN 1 ELSE 0 END AS half_star, 5 AS total_stars
        FROM `tabCourse` AS c
        LEFT JOIN `tabCourse Ratings` AS r ON c.name = r.course
        WHERE c.standalone = 1 AND c.name= %s AND c.activee = 1
         """,
        (id,),as_dict=True,)

    if not course[0]["name"]:
        frappe.local.flags.redirect_location = f'courses'
        raise frappe.Redirect
    
    points = frappe.db.sql(f"""
        SELECT p.title
        FROM `tabWhat Will Be Learnt` AS p
        WHERE p.parent=%s
        ORDER BY p.idx """,(course[0].name),as_dict=True,)
    # points = frappe.get_doc('course',id)
    coursesList = frappe.db.sql(f"""
        SELECT c.name, c.course_name, c.course_name_ar, c.hero_image, c.description, c.description_ar, c.created_by, c.price AS priceold, c.category,
        COALESCE(AVG(r.rating), 0) AS average_rating, COUNT(r.rating) AS rate_count,
        COALESCE(FLOOR(AVG(r.rating)), 0) AS full_stars, ROUND(c.price * (1 - c.discount / 100), 2) AS price,
        CASE WHEN AVG(r.rating) - FLOOR(AVG(r.rating)) >= 0.5 THEN 1 ELSE 0 END AS half_star, 5 AS total_stars
        FROM `tabCourse` AS c
        LEFT JOIN `tabCourse Ratings` AS r ON c.name = r.course
        WHERE c.institution = %s AND c.standalone = 1 AND c.name<> %s AND c.activee = 1
        LIMIT 4
         """,
        (institution ,id,),as_dict=True,)
    # frappe.throw(str(coursesList))

    if len(coursesList) < 0 or (len(coursesList) == 1 and coursesList[0].name is None):
        return {"course": course[0], "points": points,"coursesList": []}
    
    return {"course": course[0], "points": points,"coursesList": coursesList}