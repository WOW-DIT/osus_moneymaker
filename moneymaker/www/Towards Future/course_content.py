import frappe
from frappe import _
from datetime import datetime

def get_context(context):
    content = getWebContent()
    is_survey_finished = finishedSurvey()
    context.update({
        "content":content,
        "category":getCategories(content.institution),
        "course": singleCourse(),
        "course_items": courseItems(),
        "modules": courseModules(),
        "active_item": getActiveItem(),
        "finished_items": finishedItems(),
        "QAs": QA(),
        "user_completion": userCompletion(),
        "logged_in": isLoggedIn(),
        "finishedSurvey": is_survey_finished,
        "certificate_link": certificate_link(is_survey_finished),
        "user": frappe.session.user,
        "lang": getLang(),
        "online_link": online_link(),
        "year": datetime.today().year
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


@frappe.whitelist()
def isLoggedIn():
    return frappe.session.user != "Guest"

@frappe.whitelist()
def finishedSurvey(course_id=None):
    if not course_id:
        course_id=frappe.local.request.args.get('id')

    user = frappe.session.user

    if frappe.db.exists("User Survey Answer", {"user": user, "course": course_id}):
        return True
    
    return False

@frappe.whitelist()
def certificate_link(finished):
    if finished:
        course_id=frappe.local.request.args.get('id')
        user = frappe.session.user
        
        cert_id = frappe.get_value("Certificate", {"user": user, "course": course_id})
        if cert_id is not None:
            # cert = frappe.get_doc("Certificate", cert_id)
            # return cert.get_url()
            return f"https://osus.wowdigital.sa/api/method/frappe.utils.print_format.download_pdf?doctype=Certificate&name={cert_id}&format=Certificate"
        
    return None

@frappe.whitelist()
def getBrandName():
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    brand_name = dir_path.split("/")[len(dir_path.split("/")) - 1]
    return brand_name

@frappe.whitelist()
def getWebContent():
    brand_name = getBrandName()
    content_id = frappe.get_value("Educational Institution Website Content", {"brand_name": brand_name})
    if content_id is not None:
        content = frappe.get_doc('Educational Institution Website Content',content_id)
        return content


# @frappe.whitelist()
# def courseLangs():
#     lang = ""
#     course_id=frappe.local.request.args.get('id')
#     langs = frappe.db.sql(f"""
#         SELECT cl.language
#         FROM `tabCourse Languages` AS cl
#         WHERE cl.parent=%s
#         ORDER BY cl.idx """,(course_id),as_dict=True,)
    
#     for i, l in enumerate(langs):
#         lang += l.language
#         if i < len(langs)-1:
#             lang += "/"

#     return lang


def courseModules():
    course_id=frappe.local.request.args.get('id')
    user = frappe.session.user

    modules = frappe.db.sql("""
        SELECT m.name, m.title, m.order
        FROM `tabCourse Module` AS m
        WHERE m.course = %s
        ORDER BY m.order
    """, (course_id,), as_dict=True)

    for mod in modules:
        items = frappe.db.sql(f"""
        SELECT ci.name, ci.title, ci.description, (ci.time/60) AS time, ci.order, ci.type,
        s.state AS state,
        CAST((ci.time/60) AS INT) AS minutes,
        CAST(((ci.time/60) - CAST((ci.time/60) AS INT)) * 60 AS INT) AS seconds
        FROM `tabCourse Item` AS ci
        LEFT JOIN `tabCourse Item State` AS s ON ci.name = s.item AND s.user=%s
        WHERE ci.course=%s AND ci.module=%s
        ORDER BY ci.order """,(user, course_id, mod.name),as_dict=True,)

        mod.course_items = items

    # frappe.throw(str(modules))
    return modules

    
    
@frappe.whitelist()
def courseItems():
    course_id=frappe.local.request.args.get('id')
    user = frappe.session.user

    items = frappe.db.sql(f"""
        SELECT ci.name, ci.title, ci.description, (ci.time/60) AS time, ci.order, ci.type,
        s.state AS state,
        CAST((ci.time/60) AS INT) AS minutes,
        CAST(((ci.time/60) - CAST((ci.time/60) AS INT)) * 60 AS INT) AS seconds
        FROM `tabCourse Item` AS ci
        LEFT JOIN `tabCourse Item State` AS s ON ci.name = s.item AND s.user=%s
        WHERE ci.course=%s
        ORDER BY ci.order """,(user, course_id),as_dict=True,)
    
    return items


@frappe.whitelist()
def finishedItems():
    course_id=frappe.local.request.args.get('id')
    user = frappe.session.user
    
    items = frappe.db.sql(f"""
        SELECT COUNT(s.name)
        FROM `tabCourse Item State` AS s
        WHERE s.course=%s AND s.state='Finished' AND s.user=%s""",(course_id, user))
    
    return items[0][0]


@frappe.whitelist()
def itemVideo():
    course_item=frappe.local.request.args.get('item')

    recording = frappe.db.sql(f"""
        SELECT ci.attachment
        FROM `tabCourse Item` AS ci
        WHERE ci.item=%s """,(course_item),as_dict=True,)
    
    return recording

@frappe.whitelist()
def itemContent(course_item):
    try:
        course_name = frappe.local.request.args.get('id')
        user = frappe.session.user
        
        items = frappe.db.sql(f"""
            SELECT 
                ci.type, ci.article, ci.records, ci.quiz, r.attachment AS attachment, COALESCE(s.state, 'None') AS state,
                ci.course, ci.order, s.number_of_attempts AS current_attempts, iq.number_of_attempts AS max_attempts,
                s.quiz_mark AS quiz_mark, s.passed AS passed
            FROM `tabCourse Item` AS ci
            LEFT JOIN `tabCourse Item State` AS s on ci.name = s.item AND s.user=%s
            LEFT JOIN `tabRecordings` AS r ON ci.records = r.name
            LEFT JOIN `tabItem Quiz` AS iq ON ci.quiz = iq.name
            WHERE ci.name=%s """,(user, course_item),as_dict=True,)
        
        if items[0]["records"] is not None and items[0]["records"] != "" and items[0]["type"] == "Video":
            subtitles = frappe.db.sql(f"""
                SELECT sub.file, sub.language
                FROM `tabSubtitles Table` AS sub
                WHERE sub.parent=%s""",(items[0]["records"]),as_dict=True,
            )

        else:
            subtitles = None


        completed_course = userCompletion(course_name)

        if completed_course:
            finished_survey = finishedSurvey(course_name)
        else:
            finished_survey = False

        items[0].has_next = has_next(items[0])
        
        return {
            "items": items,
            "subtitles": subtitles,
            "completed": completed_course,
            "finished_survey": finished_survey,
        }
        
        # return {"items": items, "subtitles": subtitles, "completed": userCompletion(course_name)}

    except Exception as e:
        return str(e)


@frappe.whitelist()
def itemQuiz(quiz_name, state):
    # course_name = frappe.local.request.args.get('id')
    user = frappe.session.user
    questions = []
    quiz = frappe.get_doc("Item Quiz", quiz_name)
    for qu in quiz.questions:
        images = frappe.db.sql(f"""
            SELECT i.images
            FROM `tabItem Quiz Images Table` AS i
            WHERE i.parent=%s 
            ORDER BY i.idx""",(qu.question_id),
            as_dict=True,
        )
        
        if qu.type != "Matching":
            options = frappe.db.sql("""
                SELECT o.option, o.is_correct
                FROM `tabItem Quiz Options Table` AS o
                WHERE o.parent=%s 
                ORDER BY o.idx""",(qu.question_id),
                as_dict=True,
            )
            matching_questions = None
            matching_answers = None
        else:
            options = None
            matching_questions = frappe.db.sql("""
                SELECT o.option, o.matching_number
                FROM `tabMatching Table` AS o
                WHERE o.parent=%s AND o.parentfield=%s
                ORDER BY o.idx""",(qu.question_id, "matching_questions"),
                as_dict=True,
            )
            matching_answers = frappe.db.sql("""
                SELECT o.option
                FROM `tabMatching Table` AS o
                WHERE o.parent=%s AND o.parentfield=%s
                ORDER BY o.idx""",(qu.question_id, "matching_answers"),
                as_dict=True,
            )


        if state == "Finished":
            subm = frappe.db.sql(f"""
                SELECT s.type, s.answer, s.checked_options, s.matching_values
                FROM `tabItem Quiz Submission` AS s
                WHERE s.quiz=%s AND s.question=%s AND s.user=%s
                ORDER BY s.creation DESC""",(quiz.name, qu.question_id, user),
                as_dict=True,
            )[0]

            answer_state = "correct"
            answers = str(subm.answer).split(",")
            checked_options = str(subm.checked_options).split(",")
            matching_values = str(subm.matching_values).split(",")

            answer_state = get_answer_state(subm.type, answers)
            
            questions.append({
                "question_id": qu.question_id,
                "question": qu.question,
                "type": qu.type,
                "images": images,
                "options": options,
                "answers": answers,
                "matching_questions": matching_questions,
                "matching_answers": matching_answers,
                "checked_options": checked_options,
                "answer_state": answer_state,
                "matching_values": matching_values,
            })
        else:
            questions.append({
                "question_id": qu.question_id,
                "question": qu.question,
                "type": qu.type,
                "images": images,
                "options": options,
                "matching_questions": matching_questions,
                "matching_answers": matching_answers,
            })

    return questions


def get_answer_state(type: str, answers: list):
    if type == "Multichoice" or type == "Matching":
        number_of_correct = 0
        for a in answers:
            a = int(a)

            if a == 1:
                number_of_correct += 1
                
        if number_of_correct == len(answers):
            answer_state = "correct"

        elif number_of_correct == 0:
            answer_state = "incorrect"

        else:
            answer_state = "partially_correct"

        return answer_state

    elif type == "Choice":
        number_of_correct = 0
        for a in answers:
            a = int(a)

            if a == 1:
                number_of_correct += 1

        if number_of_correct == len(answers):
            answer_state = "correct"
        else:
            answer_state = "incorrect"

        return answer_state
    

@frappe.whitelist()
def validateQuiz(quiz_name, answered_questions, course_item):
    try:
        full_mark = 0
        questions_no = len(answered_questions)
        question_percent =  (1 / questions_no) * 100
        questions = []
        quiz = frappe.get_doc("Item Quiz", quiz_name)
        for qu in quiz.questions:
            
            options = frappe.db.sql(f"""
                SELECT o.option, o.is_correct
                FROM `tabItem Quiz Options Table` AS o
                WHERE o.parent=%s 
                ORDER BY o.idx""",(qu.question_id),as_dict=True,)

            matching_answers = frappe.db.sql(f"""
                SELECT o.option, o.matching_number
                FROM `tabMatching Table` AS o
                WHERE o.parent=%s AND o.parentfield=%s
                ORDER BY o.idx""",(qu.question_id, "matching_answers"),as_dict=True,)
            
            questions.append({
                "question_id": qu.question_id,
                "question": qu.question,
                "type": qu.type,
                "options": options,
                "matching_answers": matching_answers,
            })

        answers = []
        for i, q in enumerate(questions):
            q_answers = []
            checked_options = []
            matching_values = []

            if q["type"] == "Matching":
                ans_options = answered_questions[i]["matching_answers"]
                matching_answers = q["matching_answers"]
                option_percent =  (1 / len(ans_options)) * 100
                matching_percent = (option_percent / 100) * question_percent

                for j, o in enumerate(matching_answers):
                    if str(ans_options[j]["matching_number"]) == str(matching_answers[j]["matching_number"]):
                        full_mark += matching_percent
                        q_answers.append(1)

                    else:
                        q_answers.append(0)
                    
                    matching_values.append(str(ans_options[j]["matching_number"]))

            else:
                ans_options = answered_questions[i]["options"]
                options = q["options"]
                option_no = 0

                ## Only options with value "1"
                for o in options:
                    option_no += o["is_correct"]

                if q["type"] == "Multichoice":
                    ## Example: Each question has 20% of the total percentage (5 questions)
                    ## If it's "Multichoice", each option with value "1" has a percent of the 20%
                    ## 25% of the 20% = 5% of the total percentage

                    option_percent =  (1 / option_no) * 100
                    multichoice_percent = (option_percent / 100) * question_percent

                    for j, o in enumerate(options):
                        if ans_options[j]["is_correct"] == 1 and options[j]["is_correct"] == ans_options[j]["is_correct"]:

                            full_mark += multichoice_percent

                        ###
                        ### Register answers if they are correct or not
                        checked_options.append(ans_options[j]["is_correct"])
                        
                        if options[j]["is_correct"] == ans_options[j]["is_correct"]:
                            q_answers.append(1)
                            
                        else:
                            q_answers.append(0)


                else:
                    for j, o in enumerate(options):
                        if ans_options[j]["is_correct"] == 1 and options[j]["is_correct"] == ans_options[j]["is_correct"]:
                            full_mark += question_percent

                        ###
                        ### Register answers if they are correct or not
                        checked_options.append(ans_options[j]["is_correct"])

                        if options[j]["is_correct"] == ans_options[j]["is_correct"]:
                            q_answers.append(1)
                            
                        else:
                            q_answers.append(0)

            answers.append(q_answers)

            answers_str = ",".join(str(a) for a in q_answers)
            checked_options_str = ",".join(str(o) for o in checked_options)
            matching_values_str = ",".join(str(a) for a in matching_values)

            user = frappe.session.user

            quiz_subm = frappe.new_doc("Item Quiz Submission")
            quiz_subm.user = user
            quiz_subm.item = course_item
            quiz_subm.quiz = quiz.name
            quiz_subm.question = q["question_id"]
            quiz_subm.type = q["type"]
            quiz_subm.answer = answers_str
            quiz_subm.checked_options = checked_options_str
            quiz_subm.matching_values = matching_values_str
            quiz_subm.insert(ignore_permissions=True)
        
        has_passed = full_mark >= quiz.passing_percent

        item_state_id = frappe.get_value("Course Item State", {"user": user, "item": course_item, "type": "Quiz"})
        if item_state_id:
            item_state = frappe.get_doc("Course Item State", item_state_id)
            item_state.passed = 1 if has_passed else 0
            item_state.quiz_mark = full_mark
            item_state.save(ignore_permissions=True)

        frappe.db.commit()
            
        return {"status": 200, "passed": has_passed, "percent": full_mark, "answers": answers}
        
    
    except Exception as e:
        return {"status": 500, "error": str(e)}
    

@frappe.whitelist()
def last_quiz_submission():
    user = frappe.session.user
    


@frappe.whitelist()
def retakeQuiz():
    try:
        user = frappe.session.user
        course_item = frappe.form_dict.get("course_item")
        # course = frappe.form_dict.get('course')

        # item = frappe.get_doc("Course Item", course_item)

        item_state_id = frappe.get_value("Course Item State", {"user": user, "item": course_item})

        if item_state_id:
            item_state = frappe.get_doc("Course Item State", item_state_id)

            if item_state.state == "Finished" and item_state.type == "Quiz":
                quiz = frappe.get_doc("Item Quiz", item_state.quiz)
                max_attempts = quiz.number_of_attempts
                current_attempts = item_state.number_of_attempts

                if current_attempts < max_attempts:
                    item_state.state = "Active"
                    item_state.number_of_attempts += 1
                    item_state.save(ignore_permissions=True)

                    frappe.db.commit()

                    return {"passed": True}
                
            return {"passed": False, "error": "User exceeded maximum number of attempts!"}
        else:
            return {"passed": False, "error": "User didn't submit the quiz!"}

    except Exception as e:
        return {"passed": False, "error": str(e)}



@frappe.whitelist()
def QA(course_item=None, search=None):
    user = frappe.session.user
    course = frappe.local.request.args.get('id')

    if course_item is not None and course_item != "null":
        if search is not None and search != "":
            QAs = frappe.db.sql(f"""
                SELECT q.name, q.title, q.question, q.likes, u.user_image as image, u.full_name as full_name,
                l.qa IS NOT NULL AS liked
                FROM `tabCourse QA` AS q
                LEFT JOIN `tabUser` AS u ON u.name = q.user
                LEFT JOIN `tabCourse QA Like` AS l ON l.qa = q.name AND l.user = %s
                WHERE
                    q.course_item=%s AND (q.reference='None' OR q.reference='')
                    AND (q.title like %s OR q.question like %s) 
                ORDER BY q.likes DESC """,(user, course_item, f"%{search}%", f"%{search}%"),as_dict=True,)
        else:
            QAs = frappe.db.sql(f"""
                SELECT q.name, q.title, q.question, q.likes, u.user_image as image, u.full_name as full_name,
                l.qa IS NOT NULL AS liked
                FROM `tabCourse QA` AS q
                LEFT JOIN `tabUser` AS u ON u.name = q.user
                LEFT JOIN `tabCourse QA Like` AS l ON l.qa = q.name AND l.user = %s
                WHERE
                    q.course_item=%s AND (q.reference='None' OR q.reference='') 
                ORDER BY q.likes DESC """,(user, course_item),as_dict=True,)
        
    else:
        if search is not None and search != "":
            QAs = frappe.db.sql(f"""
                SELECT q.name, q.title, q.question, q.likes, u.user_image as image, u.full_name as full_name,
                l.qa IS NOT NULL AS liked
                FROM `tabCourse QA` AS q
                LEFT JOIN `tabUser` AS u ON u.name = q.user
                LEFT JOIN `tabCourse QA Like` AS l ON l.qa = q.name AND l.user = %s
                WHERE 
                    q.course=%s AND (q.reference='None' OR q.reference='')
                    AND (q.title like %s OR q.question like %s) 
                ORDER BY q.likes DESC """,(user, course, f"%{search}%", f"%{search}%"),as_dict=True,)
        else:
            QAs = frappe.db.sql(f"""
                SELECT q.name, q.title, q.question, q.likes, u.user_image as image, u.full_name as full_name,
                l.qa IS NOT NULL AS liked
                FROM `tabCourse QA` AS q
                LEFT JOIN `tabUser` AS u ON u.name = q.user
                LEFT JOIN `tabCourse QA Like` AS l ON l.qa = q.name AND l.user = %s
                WHERE 
                    q.course=%s AND (q.reference='None' OR q.reference='')
                ORDER BY q.likes DESC """,(user, course),as_dict=True,)
    
    return QAs

@frappe.whitelist()
def QAResponses(reference):
    mainQ = frappe.get_doc("Course QA", reference)

    try:
        QAs = frappe.db.sql(f"""
            SELECT q.name, COALESCE(q.title, 'None') AS title, q.reference, q.question, q.creation as date,
            u.user_image AS user_image, u.full_name AS full_name
            FROM `tabCourse QA` AS q
            LEFT JOIN `tabUser` AS u ON u.name = q.user
            WHERE q.reference=%s """,(reference),as_dict=True,)
        
        return {"replies": QAs, "mainQ": mainQ.title}
    
    except:
        return {"replies": [], "mainQ": mainQ.title}

@frappe.whitelist()
def likeQA(qa_name):
    try:
        user = frappe.session.user
        qa = frappe.get_doc("Course QA", qa_name)
        potLike = frappe.get_value("Course QA Like", filters={"user": user, "qa": qa_name})
        if potLike is not None:
            like = frappe.get_doc("Course QA Like", potLike)
            like.delete(ignore_permissions=True)
            
            qa.likes -= 1
            qa.save(ignore_permissions=True)
            frappe.db.commit()
            return False

        else:
            like = frappe.new_doc("Course QA Like")
            like.user = user
            like.qa = qa_name
            like.insert(ignore_permissions=True)

            qa.likes += 1
            qa.save(ignore_permissions=True)
            frappe.db.commit()
            return True
    
    except:
        return None

@frappe.whitelist()
def writeReply(qa_name, details, course_item):
    try:
        user = frappe.session.user

        reply = frappe.new_doc("Course QA")
        reply.question = details
        reply.reference = qa_name
        reply.user = user
        reply.course_item = course_item
        reply.insert(ignore_permissions=True)
        frappe.db.commit()
        return True
    
    except:
        return False


@frappe.whitelist()
def getCategories(institution="Osus"):
    courses = frappe.db.sql(f"""
        SELECT category, image
        FROM `tabCourse Category`
        ORDER BY name """,as_dict=True,)
    
    return courses


@frappe.whitelist()
def userCompletion(course_name=None):
    user = frappe.session.user
    if course_name is None:
        course_name = frappe.local.request.args.get('id')
    try:
        items = frappe.db.sql(f"""
            SELECT COUNT(i.name) = COUNT(s.name) as completed
            FROM `tabCourse Item` AS i
            LEFT JOIN `tabCourse Item State` AS s on i.name = s.item AND s.user = %s AND s.state='Finished'
            WHERE i.course=%s """,
            (user, course_name))
        # finishedStates = frappe.db.sql(f"""
        #     SELECT COUNT(s.name)
        #     FROM `tabCourse Item State` AS s
        #     WHERE s.course=%s AND s.state=%s """, # AND s.user=%s,
        #     (course_name, "Finished"))
        
        return items[0][0] == 1
    except:
        return None
    

@frappe.whitelist()
def getActiveItem():

    course_name=frappe.local.request.args.get('id')
    itemName = None
    user = frappe.session.user

    activeStates = frappe.db.sql(f"""
        SELECT s.name, s.item, ci.type, ci.course, ci.order, s.number_of_attempts AS current_attempts, iq.number_of_attempts AS max_attempts
        FROM `tabCourse Item State` AS s
        LEFT JOIN `tabCourse Item` AS ci ON s.item = ci.name
        LEFT JOIN `tabItem Quiz` AS iq ON ci.quiz = iq.name
        WHERE s.course=%s AND s.state=%s AND s.user=%s""",
        (course_name, "Active", user), as_dict=True)
    
    if len(activeStates) > 0:
        itemName = activeStates[0].item

    else:
        finishedStates = frappe.db.sql(f"""
            SELECT s.name, s.item
            FROM `tabCourse Item State` AS s
            WHERE s.course=%s AND s.state=%s AND s.user=%s
            ORDER BY s.order DESC
            LIMIT 1 """,
            (course_name, "Finished", user), as_dict=True)
        
        if len(finishedStates) > 0:
            itemName = finishedStates[0].item

    items = frappe.db.sql(f"""
        SELECT ci.name, ci.title, ci.description, ci.type, ci.article, ci.records, ci.quiz, r.attachment AS attachment, COALESCE(s.state, 'None') AS state,
        ci.course, ci.order, s.number_of_attempts AS current_attempts, iq.number_of_attempts AS max_attempts,
        s.quiz_mark AS quiz_mark, s.passed AS passed
        FROM `tabCourse Item` AS ci
        LEFT JOIN `tabCourse Item State` AS s on ci.name = s.item AND s.user=%s
        LEFT JOIN `tabRecordings` AS r ON ci.records = r.name
        LEFT JOIN `tabItem Quiz` AS iq ON ci.quiz = iq.name
        WHERE ci.name=%s """,(user, itemName),as_dict=True,)
    
    if len(items) == 0:
        items = frappe.db.sql(f"""
            SELECT ci.name, ci.title, ci.description, ci.type, ci.article, ci.records, ci.quiz, r.attachment AS attachment, COALESCE(s.state, 'None') AS state,
            ci.course, ci.order, s.number_of_attempts AS current_attempts, iq.number_of_attempts AS max_attempts,
            s.quiz_mark AS quiz_mark, s.passed AS passed
            FROM `tabCourse Item` AS ci
            LEFT JOIN `tabCourse Item State` AS s on ci.name = s.item AND s.user=%s
            LEFT JOIN `tabRecordings` AS r ON ci.records = r.name
            LEFT JOIN `tabItem Quiz` AS iq ON ci.quiz = iq.name
            WHERE ci.course=%s
            ORDER BY ci.order
            LIMIT 1 """,(user, course_name),as_dict=True,)

        if len(items) == 0:
            return None

    if items[0]["records"] is not None and items[0]["records"] != "" and items[0]["type"] == "Video":
        subtitles = frappe.db.sql(f"""
            SELECT sub.file, sub.language
            FROM `tabSubtitles Table` AS sub
            WHERE sub.parent=%s""",(items[0]["records"]),as_dict=True,
        )

    else: subtitles = None

    items[0].has_next = has_next(items[0])

    if items[0].type == "Quiz" and items[0].quiz is not None:
        return {"item": items[0], "subtitles": subtitles, "quiz": itemQuiz(items[0].quiz, items[0].state)}
    else:
        return {"item": items[0], "subtitles": subtitles, "quiz": None}


@frappe.whitelist()
def activateItem(course_item):
    try:
        user = frappe.session.user

        itemStates = frappe.db.sql(f"""
            SELECT s.name, s.state
            FROM `tabCourse Item State` AS s
            WHERE s.item=%s AND s.user=%s""", # AND s.user=%s,
            (course_item, user), as_dict=True)
        
        if len(itemStates) == 0:
            itemState = frappe.new_doc("Course Item State")
            itemState.item = course_item
            itemState.state = "Active"
            itemState.user = user
            itemState.insert(ignore_permissions=True)
            frappe.db.commit()

            return {"active": True}
            
        else:
            return {"active": False}
        
    except:
        return {"active": False}
    

@frappe.whitelist()
def completeItem(course_item):
    try:
        user = frappe.session.user
        item = frappe.get_doc("Course Item", course_item)

        itemStates = frappe.db.sql(f"""
            SELECT s.name, s.state
            FROM `tabCourse Item State` AS s
            WHERE s.item=%s AND s.user=%s""", # AND s.user=%s,
            (course_item, user), as_dict=True)
        
        # Change state "Active" --> "Finished"
        if len(itemStates) > 0:
            if itemStates[0].state != "Finished":
                itemState = frappe.get_doc("Course Item State", itemStates[0].name)
                itemState.state = "Finished"
                itemState.save(ignore_permissions=True)
                frappe.db.commit()

            else:
                return {"completed": False, "finished": userCompletion(item.course)}
        
        # No state found
        else:
            itemState = frappe.new_doc("Course Item State")
            itemState.state = "Finished"
            itemState.user = user
            itemState.item = course_item
            itemState.save(ignore_permissions=True)
            frappe.db.commit()            

        return {"completed": True, "finished": userCompletion(item.course)}
        
    except:
        return {"completed": False, "finished": userCompletion(item.course)}
        
    
    
@frappe.whitelist()
def nextItem(course_item):
    try:
        user  = frappe.session.user
        item = frappe.get_doc("Course Item", course_item)
        nextItem = frappe.get_value("Course Item", filters={"course": item.course, "order": int(item.order+1)})

        if nextItem is not None:

            itemStates = frappe.db.sql(f"""
                SELECT s.name
                FROM `tabCourse Item State` AS s
                WHERE s.item=%s AND s.user=%s """,
                (nextItem, user),as_dict=True,)

            if len(itemStates) == 0:
                itemState = frappe.new_doc("Course Item State")
                itemState.state = "Active"
                itemState.item = nextItem
                itemState.user = user
                itemState.insert(ignore_permissions=True)

            next_item = getNextItem(nextItem)
            completed_course = userCompletion(item.course)

            if completed_course:
                finished_survey = finishedSurvey(item.course)
            else:
                finished_survey = False

            next_item["item"].has_next = has_next(next_item["item"])

            
            return {
                "item": next_item["item"],
                "subtitles": next_item["subtitles"],
                "completed": completed_course,
                "finished_survey": finished_survey,
            }

        else:
            return {"item": None}
    except Exception as e:
        return {"item": None, "error": str(e)}
        

def has_next(item):
    next_item_id = frappe.get_value("Course Item", filters={"course": item.course, "order": int(item.order+1)})

    return next_item_id is not None



def getNextItem(course_item):
    user = frappe.session.user
    items = frappe.db.sql(f"""
        SELECT
            ci.name, ci.title, ci.description, ci.type, ci.article, ci.records, ci.quiz, r.attachment AS attachment, COALESCE(s.state, 'None') AS state,
            ci.course, s.order, s.number_of_attempts AS current_attempts, iq.number_of_attempts AS max_attempts,
            s.quiz_mark AS quiz_mark, s.passed AS passed
        FROM `tabCourse Item` AS ci
        LEFT JOIN `tabCourse Item State` AS s on ci.name = s.item AND s.user=%s
        LEFT JOIN `tabRecordings` AS r ON ci.records = r.name
        LEFT JOIN `tabItem Quiz` AS iq ON ci.quiz = iq.name
        WHERE ci.name=%s """,(user, course_item),as_dict=True,)
    
    if len(items) > 0:
        item = items[0]
        if item["records"] is not None and item["records"] != "" and item["type"] == "Video":
            subtitles = frappe.db.sql(f"""
                SELECT sub.file, sub.language
                FROM `tabSubtitles Table` AS sub
                WHERE sub.parent=%s""",(item["records"]),as_dict=True,
            )

        else: subtitles = None

            
        return {"item": item, "subtitles": subtitles}
    else:
        return None


@frappe.whitelist()
def singleCourse():
    course_id=frappe.local.request.args.get('id')

    # if not frappe.db.exists(
    #     "Course Purchase",
    #     {"user": frappe.session.user, "course": course_id, "is_refunded": 0},
    # ):
    #     frappe.throw("You need to purchase this course")

    course = frappe.db.sql(f"""
        SELECT c.name, c.course_name, c.hero_image, c.description, c.created_by, c.price AS priceold, c.category,
        COALESCE(AVG(r.rating), 0) AS average_rating, COUNT(r.rating) AS rate_count,
        COALESCE(FLOOR(AVG(r.rating)), 0) AS full_stars, ROUND(c.price * (1 - c.discount / 100), 2) AS price,
        CASE WHEN AVG(r.rating) - FLOOR(AVG(r.rating)) >= 0.5 THEN 1 ELSE 0 END AS half_star, 5 AS total_stars
        FROM `tabCourse` AS c
        LEFT JOIN `tabCourse Ratings` AS r ON c.name = r.course
        WHERE c.standalone = 1 AND c.name= %s AND c.activee = 1
         """,
        (course_id,),as_dict=True,)

    if not course[0]["name"]:
        frappe.local.flags.redirect_location = f'courses'
        raise frappe.Redirect
    
    points = frappe.db.sql(f"""
        SELECT p.title
        FROM `tabWhat Will Be Learnt` AS p
        WHERE p.parent=%s
        ORDER BY p.idx """,(course[0].name),as_dict=True,)

    coursesList = frappe.db.sql(f"""
        SELECT c.name, c.course_name, c.hero_image, c.description, c.created_by, c.price AS priceold, c.category,
        COALESCE(AVG(r.rating), 0) AS average_rating, COUNT(r.rating) AS rate_count,
        COALESCE(FLOOR(AVG(r.rating)), 0) AS full_stars, ROUND(c.price * (1 - c.discount / 100), 2) AS price,
        CASE WHEN AVG(r.rating) - FLOOR(AVG(r.rating)) >= 0.5 THEN 1 ELSE 0 END AS half_star, 5 AS total_stars
        FROM `tabCourse` AS c
        LEFT JOIN `tabCourse Ratings` AS r ON c.name = r.course
        WHERE c.standalone = 1 AND c.name<> %s AND c.activee = 1
        LIMIT 4
         """,
        (course_id,),as_dict=True,)

    return {"course": course[0], "points": points,"coursesList": coursesList}

@frappe.whitelist()
def online_link():
    course_id=frappe.local.request.args.get('id')
    course = frappe.get_doc("Course", course_id)

    if course.online_lecture == 1:
        meeting = frappe.get_doc("Meeting Room", course.meeting_link)
        return {
            "link": f"https://meeting.wowdigital.sa/?room={meeting.room_code}",
            "start_time": course.start_time,
            "end_time": course.end_time,
        }
    
    return None

# @frappe.whitelist()
# def getOptions(template):
#     questions = frappe.db.sql("""
#         SELECT sq.name, sq.question, sq.type
#         FROM `tabSurvey Questions Table` AS q
#         LEFT JOIN `tabSurvey Question` AS sq ON sq.name = q.question
#         WHERE q.parent = %s
#         ORDER BY q.idx
#     """, (template), as_dict=True)

#     for question in questions:
#         if question.type != "Text":
#             options = frappe.db.sql("""
#                 SELECT o.option
#                 FROM `tabSurvey Options Table` AS o
#                 WHERE o.parent = %s
#                 ORDER BY o.parent AND o.idx
#             """, (question.name), as_dict=True)
#         else:
#             options = None

#         question["options"] = options

#     return questions
