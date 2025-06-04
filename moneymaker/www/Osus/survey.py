import frappe
from frappe import _
from datetime import datetime
import json

def get_context(context):
    if finishedSurvey():
        course_id=frappe.local.request.args.get('id')
        frappe.local.flags.redirect_location = f'course_det?id={course_id}'
        raise frappe.Redirect

    content = getWebContent()
    context = {
        "content":content,
        "course":singleCourse(),
        "logged_in": isLoggedIn(),
        "user": frappe.session.user,
        "lang": getLang(),
        "year": datetime.today().year,
    }
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
    

@frappe.whitelist()
def finishedSurvey():
    course_id=frappe.local.request.args.get('id')

    if not frappe.db.exists(
        "Course Purchase",
        {"user": frappe.session.user, "course": course_id, "is_refunded": 0},
    ):
        frappe.throw("You need to purchase this course")
    
    user = frappe.session.user

    if frappe.db.exists("User Survey Answer", {"user": user, "course": course_id}):
        return True
    
    return False


@frappe.whitelist(allow_guest=True)
def getCategories(institution="Osus"):
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
        lang += l.language
        if i < len(langs)-1:
            lang += "/"

    return lang


@frappe.whitelist(allow_guest=True)
def singleCourse():
    id=frappe.local.request.args.get('id')
    course = frappe.db.sql(f"""
        SELECT c.name, c.description, c.category, c.survey_template
        FROM `tabCourse` AS c
        WHERE c.name= %s AND c.activee = 1
         """,
        (id,),as_dict=True,)
    
    questions = frappe.db.sql("""
        SELECT sq.name, sq.question, sq.type
        FROM `tabSurvey Questions Table` AS q
        LEFT JOIN `tabSurvey Question` AS sq ON sq.name = q.question
        WHERE q.parent = %s
        ORDER BY q.idx
        """, (course[0].survey_template), as_dict=True)

    for question in questions:
        if question.type != "Text":
            options = frappe.db.sql("""
                SELECT o.option
                FROM `tabSurvey Options Table` AS o
                WHERE o.parent = %s
                ORDER BY o.idx
            """, (question.name), as_dict=True)
        else:
            options = None

        question["options"] = options

    return {"course": course[0], "survey": questions}


@frappe.whitelist()
def submitSurvey():
    try:
        id=frappe.local.request.args.get('id')

        course = frappe.get_doc("Course", id)
        user = frappe.get_doc("User", frappe.session.user)

        raw_data = frappe.local.request.get_data(as_text=True)
        data = json.loads(raw_data)
        questions = data["questions"]
        survey_template = data["survey"]

        for q in questions:
            answers = questions[q]
            if len(answers) > 0:
                answer = frappe.new_doc("User Survey Answer")
                answer.user = user.name
                answer.survey = survey_template
                answer.question = q
                answer.answer = "\n,\n".join(answers)
                answer.course = course.name
                answer.insert(ignore_permissions=True)

        frappe.db.commit()
        certificate_url = newCertificate(course, user)

        return {"message": "Survey has been submitted successfully", "successful": True, "certificate_url": certificate_url}

    except Exception as e:
        return {"message": e, "successful": False}


@frappe.whitelist()
def newCertificate(course, user):
    try:
        cert = frappe.new_doc("Certificate")
        cert.user = user.name
        cert.date = datetime.now()
        cert.type = "Course"
        cert.course = course.name
        cert.instructor = course.created_by
        cert.institution = course.institution

        cert.insert(ignore_permissions=True)

        return f"/api/method/frappe.utils.print_format.download_pdf?doctype=Certificate&name={cert.name}&format=Certificate&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D"
    
    except:
        return None