import frappe

from frappe import _

def get_context(context):
    content = getWebContent()
    categories = getCategories(content.institution)
    category = categories[0].category if len(categories) > 0 else None
    context = {
        "selected_category": getSelectedCategory(),
        "content":content,
        "category":categories,
        "course":getCourses(institution=content.institution, category=category),
        "number_of_students": numberOfStudents(content.institution),
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
        # "blogger":getBlogger(),
        # "news":getNews(),
        # "plans":getplans()
    }
    cats = []

    for c in context["category"]:
        cats.append(c.category)

    context["contains_category"] = context["selected_category"] in cats
    
    return context

def getInstitutionName():
    brand_name = getBrandName()
    with open(f"/home/frappe/frappe-bench/apps/moneymaker/moneymaker/www/{brand_name}/name.txt", "r") as f:
        institution = f.read()
    return institution

def getSelectedCategory():
    return str(frappe.local.request.args.get('category'))

# def getBlogger():
#     content = frappe.db.sql(f""" select * from `tabBlogger` where disabled='false' """,as_dict=True)
#     return content

# @frappe.whitelist(allow_guest=True)
# def getNews():
#     content = frappe.db.sql(f""" select message from `tabNewsletter` Limit 3 """,as_dict=True)
#     return content

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



# @frappe.whitelist(allow_guest=True)
# def getCategories():
#         # SELECT name, hero_image, description, created_by, price
#         # FROM `tabCourse`
#     courses = frappe.db.sql(f"""
#         SELECT category, image
#         FROM `tabCourse Category`
#         ORDER BY name """,as_dict=True,)
    
#     return courses

@frappe.whitelist(allow_guest=True)
def getCategories(institution):
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
def getCourses(institution, category, page=1):
    page_size = 6

    page = int(page)
    
    page_number = int((page - 1) * page_size)
    
    courses = frappe.db.sql(f""" 
        SELECT c.name, c.hero_image, c.description, c.created_by, c.price AS priceold, c.category,
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

# @frappe.whitelist(allow_guest=True)
# def singleCourse(course_name):
#     course = frappe.db.sql(f"""
#         SELECT c.name, c.hero_image, c.description, c.created_by, c.price, AVG(r.rating) AS average_rating
#         FROM `tabCourse` AS c
#         LEFT JOIN `tabCourse Ratings` AS r ON c.name = r.course
#         WHERE c.name=%s
#         GROUP BY c.name """,(course_name),as_dict=True,)
    
#     points = frappe.db.sql(f"""
#         SELECT p.title
#         FROM `tabWhat Will Be Learnt` AS p
#         WHERE p.parent=%s
#         ORDER BY p.idx """,(course_name),as_dict=True,)

#     return {"course": course, "points": points}