import frappe
from frappe import _
from datetime import datetime

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

@frappe.whitelist()
def submitSurvey(data):
    try:
        id=frappe.local.request.args.get('id')

        course = frappe.get_doc("Course", id)
        user = frappe.get_doc("User", frappe.session.user)

        questions = data["questions"]
        # survey_template = data["survey"]
        # course = data["course"]

        for q in questions:
            answers = questions[q]
            if len(answers) > 0:
                answer = frappe.new_doc("User Survey Answer")
                answer.user = user
                # answer.survey = survey_template
                answer.question = q
                answer.answer = "\n,\n".join(answers)
                answer.course = course.name
                answer.insert(ignore_permissions=True)

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

        return cert.get_url()
    
    except:
        return None