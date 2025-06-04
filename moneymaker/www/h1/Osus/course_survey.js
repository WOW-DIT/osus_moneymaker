console.log("iubhniukjnikunikuniknijknikun")
const answerForms = document.querySelectorAll(".sur-form");
// const checkInputs = document.querySelectorAll(".form-check-input");
// const answerAreas = document.querySelectorAll(".answer-area");
const submitBtn = document.getElementById("submit-survey-btn");

submitBtn.onclick = submitSurvey

function submitSurvey() {
    let answers = getAnswers()
    let course_id = ""
    console.log(answers)
    // fetch(`/api/method/moneymaker.course_survey.submitSurvey?id=${course_id}`, {
    //     method: 'POST',
    //     body: JSON.stringify({
    //         data: {
    //             answers: answers
    //         }
    //     }),
    //     headers: {
    //       'Content-type': 'application/json; charset=UTF-8',
    //     },
    //   }).then((response) => response.json())
    //     .then((json) => {
    //         if(json && json.message !== null)
    //         {
    //             location.href = json.message

    //         }
    //     });
}

function getAnswers() {
    let questions = {}
    for(let form of answerForms) {
        const question = form.getAttribute("data-q")
        const formType = form.getAttribute("data-q-type")
        questions[question] = []
        if(formType === "Text") {

            const inputs = form.querySelectorAll(".form-answer")
            for(let input of inputs) {
                questions[question].push(input.value)
            }
        }
    }
    console.log(questions)
}

function getQInputs(form) {
    
}
