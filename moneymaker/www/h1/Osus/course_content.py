import frappe
from frappe import _

def get_context(context):
    content = getWebContent()
    context = {
        "content":content,
        "category":getCategories(content.institution),
        "course": singleCourse(),
        "course_items": courseItems(),
        "active_item": getActiveItem(),
        "finished_items": finishedItems(),
        "QAs": QA(),
        "user_completion": userCompletion(),
        "logged_in": isLoggedIn(),
        "finishedSurvey": finishedSurvey(),
        "user": frappe.session.user,
        # "course_langs": courseLangs(),
        # "number_of_students": numberOfStudents()
        # "blogger":getBlogger(),
        # "news":getNews(),
        # "plans":getplans()
    }
    return context

def getInstitutionName():
    with open("/Osus/name.txt", "r") as f:
        institution = f.read()
    return institution


@frappe.whitelist(allow_guest=True)
def isLoggedIn():
    return frappe.session.user != "Guest"

@frappe.whitelist()
def finishedSurvey():
    course_id=frappe.local.request.args.get('id')
    user = frappe.session.user

    if frappe.db.exists("User Survey Answer", {"user": user, "course": course_id}):
        return True
    
    return False

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
def courseItems():
    course_id=frappe.local.request.args.get('id')
    user = frappe.session.user

    items = frappe.db.sql(f"""
        SELECT ci.name, ci.title, ci.description, (ci.time/60) AS time, ci.order,
        s.state AS state,
        CAST((ci.time/60) AS INT) AS minutes,
        CAST(((ci.time/60) - CAST((ci.time/60) AS INT)) * 60 AS INT) AS seconds
        FROM `tabCourse Item` AS ci
        LEFT JOIN `tabCourse Item State` AS s ON ci.name = s.item AND s.user=%s
        WHERE ci.course=%s
        ORDER BY ci.order """,(user, course_id),as_dict=True,)
    
    return items

@frappe.whitelist(allow_guest=True)
def finishedItems():
    course_id=frappe.local.request.args.get('id')
    user = frappe.session.user
    
    items = frappe.db.sql(f"""
        SELECT COUNT(s.name)
        FROM `tabCourse Item State` AS s
        WHERE s.course=%s AND s.state='Finished' AND s.user=%s""",(course_id, user))
    
    return items[0][0]


@frappe.whitelist(allow_guest=True)
def itemVideo():
    course_item=frappe.local.request.args.get('item')

    recording = frappe.db.sql(f"""
        SELECT ci.attachment
        FROM `tabCourse Item` AS ci
        WHERE ci.item=%s """,(course_item),as_dict=True,)
    
    return recording

@frappe.whitelist(allow_guest=True)
def itemContent(course_item):
    course_name = frappe.local.request.args.get('id')
    user = frappe.session.user
    
    itemContent = frappe.db.sql(f"""
        SELECT ci.type, ci.article, ci.records, ci.quiz, r.attachment AS attachment, COALESCE(s.state, 'None') AS state
        FROM `tabCourse Item` AS ci
        LEFT JOIN `tabCourse Item State` AS s on ci.name = s.item AND s.user=%s
        LEFT JOIN `tabRecordings` AS r ON ci.records = r.name
        LEFT JOIN `tabItem Quiz` AS iq ON ci.quiz = iq.name
        WHERE ci.name=%s """,(user, course_item),as_dict=True,)
    
    return {"items": itemContent, "completed": userCompletion(course_name)}

@frappe.whitelist(allow_guest=True)
def itemQuiz(quiz_name):
    # course_name = frappe.local.request.args.get('id')
    questions = []
    quiz = frappe.get_doc("Item Quiz", quiz_name)
    for qu in quiz.questions:
        
        options = frappe.db.sql(f"""
            SELECT o.option
            FROM `tabItem Quiz Options Table` AS o
            WHERE o.parent=%s 
            ORDER BY o.idx""",(qu.question_id),as_dict=True,)
        
        questions.append({
            "question": qu.question,
            "type": qu.type,
            "options": options,
        })
    
    return questions

@frappe.whitelist(allow_guest=True)
def validateQuiz(quiz_name, answered_questions):
    # course_name = frappe.local.request.args.get('id')
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
        
        questions.append({
            "question": qu.question,
            "type": qu.type,
            "options": options,
        })

    answers = []
    for i, q in enumerate(questions):
        q_answers = []
        # ans_question = answered_questions[i]
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
                    # return ans_options[j]["is_correct"]
                    full_mark += multichoice_percent

                ###
                ### Register answers if they are correct or not
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
                if options[j]["is_correct"] == ans_options[j]["is_correct"]:
                    q_answers.append(1)
                    
                else:
                    q_answers.append(0)
        
        answers.append(q_answers)

    if full_mark >= quiz.passing_percent:
        return {"passed": True, "percent": full_mark, "answers": answers}
    
    return {"passed": False, "percent": full_mark, "answers": answers}
    


@frappe.whitelist(allow_guest=True)
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

@frappe.whitelist(allow_guest=True)
def QAResponses(reference):
    mainQ = frappe.get_doc("Course QA", reference)

    try:
        QAs = frappe.db.sql(f"""
            SELECT q.name, COALESCE(q.title, 'None') AS title, q.reference, q.question,
            u.user_image AS user_image, u.full_name AS full_name
            FROM `tabCourse QA` AS q
            LEFT JOIN `tabUser` AS u ON u.name = q.user
            WHERE q.reference=%s """,(reference),as_dict=True,)
        
        return {"replies": QAs, "mainQ": mainQ.title}
    
    except:
        return {"replies": [], "mainQ": mainQ.title}

@frappe.whitelist(allow_guest=True)
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

@frappe.whitelist(allow_guest=True)
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


@frappe.whitelist(allow_guest=True)
def getCategories(institution="Osus"):
        # SELECT name, hero_image, description, created_by, price
        # FROM `tabCourse`
    
    courses = frappe.db.sql(f"""
        SELECT category, image
        FROM `tabCourse Category`
        ORDER BY name """,as_dict=True,)
    
    return courses


@frappe.whitelist(allow_guest=True)
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
    

@frappe.whitelist(allow_guest=True)
def getActiveItem():

    course_name=frappe.local.request.args.get('id')
    itemName = None
    user = frappe.session.user

    activeStates = frappe.db.sql(f"""
        SELECT s.name, s.item
        FROM `tabCourse Item State` AS s
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
        SELECT ci.name, ci.title, ci.description, ci.type, ci.article, ci.records, ci.quiz, r.attachment AS attachment, COALESCE(s.state, 'None') AS state
        FROM `tabCourse Item` AS ci
        LEFT JOIN `tabCourse Item State` AS s on ci.name = s.item AND s.user=%s
        LEFT JOIN `tabRecordings` AS r ON ci.records = r.name
        LEFT JOIN `tabItem Quiz` AS iq ON ci.quiz = iq.name
        WHERE ci.name=%s """,(user, itemName),as_dict=True,)
    
    if len(items) == 0:
        items = frappe.db.sql(f"""
            SELECT ci.name, ci.title, ci.description, ci.type, ci.article, ci.records, ci.quiz, r.attachment AS attachment, COALESCE(s.state, 'None') AS state
            FROM `tabCourse Item` AS ci
            LEFT JOIN `tabCourse Item State` AS s on ci.name = s.item AND s.user=%s
            LEFT JOIN `tabRecordings` AS r ON ci.records = r.name
            LEFT JOIN `tabItem Quiz` AS iq ON ci.quiz = iq.name
            WHERE ci.course=%s
            ORDER BY ci.order
            LIMIT 1 """,(user, course_name),as_dict=True,)

        if len(items) == 0:
            return None

    if items[0].type == "Quiz" and items[0].quiz is not None:

        return {"item": items[0], "quiz": itemQuiz(items[0].quiz)}
    else:
        return {"item": items[0], "quiz": None}


@frappe.whitelist(allow_guest=True)
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
    

@frappe.whitelist(allow_guest=True)
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
        
    
    
@frappe.whitelist(allow_guest=True)
def nextItem(course_item):
    try:
        user  = frappe.session.user
        item = frappe.get_doc("Course Item", course_item)
        nextItem = frappe.get_value("Course Item", filters={"order": int(item.order+1)})

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

            return {"item": getNextItem(nextItem), "completed": userCompletion(item.course)}

        else:
            return {"item": None}
    except:
        return {"item": None}
        
def getNextItem(course_item):
    user = frappe.session.user
    items = frappe.db.sql(f"""
        SELECT ci.name, ci.title, ci.description, ci.type, ci.article, ci.records, ci.quiz, r.attachment AS attachment, COALESCE(s.state, 'None') AS state
        FROM `tabCourse Item` AS ci
        LEFT JOIN `tabCourse Item State` AS s on ci.name = s.item AND s.user=%s
        LEFT JOIN `tabRecordings` AS r ON ci.records = r.name
        LEFT JOIN `tabItem Quiz` AS iq ON ci.quiz = iq.name
        WHERE ci.name=%s """,(user, course_item),as_dict=True,)
    
    if len(items) > 0:
        return items[0]
    else:
        return None


@frappe.whitelist(allow_guest=True)
def singleCourse():
    id=frappe.local.request.args.get('id')
    course = frappe.db.sql(f"""
        SELECT c.name, c.hero_image, c.description, c.created_by, c.price AS priceold, c.category,
        COALESCE(AVG(r.rating), 0) AS average_rating, COUNT(r.rating) AS rate_count,
        COALESCE(FLOOR(AVG(r.rating)), 0) AS full_stars, ROUND(c.price * (1 - c.discount / 100), 2) AS price,
        CASE WHEN AVG(r.rating) - FLOOR(AVG(r.rating)) >= 0.5 THEN 1 ELSE 0 END AS half_star, 5 AS total_stars
        FROM `tabCourse` AS c
        LEFT JOIN `tabCourse Ratings` AS r ON c.name = r.course
        WHERE c.standalone = 1 AND c.name= %s AND c.activee = 1
         """,
        (id,),as_dict=True,)
    
    points = frappe.db.sql(f"""
        SELECT p.title
        FROM `tabWhat Will Be Learnt` AS p
        WHERE p.parent=%s
        ORDER BY p.idx """,(course[0].name),as_dict=True,)

    coursesList = frappe.db.sql(f"""
        SELECT  c.name, c.hero_image, c.description, c.created_by, c.price AS priceold, c.category,
        COALESCE(AVG(r.rating), 0) AS average_rating, COUNT(r.rating) AS rate_count,
        COALESCE(FLOOR(AVG(r.rating)), 0) AS full_stars, ROUND(c.price * (1 - c.discount / 100), 2) AS price,
        CASE WHEN AVG(r.rating) - FLOOR(AVG(r.rating)) >= 0.5 THEN 1 ELSE 0 END AS half_star, 5 AS total_stars
        FROM `tabCourse` AS c
        LEFT JOIN `tabCourse Ratings` AS r ON c.name = r.course
        WHERE c.standalone = 1 AND c.name<> %s AND c.activee = 1
        LIMIT 4
         """,
        (id,),as_dict=True,)

    return {"course": course[0], "points": points,"coursesList": coursesList}


# @frappe.whitelist(allow_guest=True)
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