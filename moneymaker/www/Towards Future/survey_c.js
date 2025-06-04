
document.addEventListener("DOMContentLoaded", (e) => {
    const answerForms = document.querySelectorAll(".sur-form");
    const form = document.getElementById("survey-form");
    // const checkInputs = document.querySelectorAll(".form-check-input");
    // const answerAreas = document.querySelectorAll(".answer-area");
    const submitBtn = document.getElementById("submit-survey-btn");
    
    submitBtn.onclick = submitSurvey
    
    function submitSurvey() {
        let answers = getAnswers()
        let course_id = getQueryParam("id")

        $.ajax({
            method: 'POST',
            url: `/api/method/moneymaker.www.api.survey.submitSurvey?id=${course_id}`,
            data: JSON.stringify(answers),
            contentType: 'application/json',
            success: function(response) {
                if(response.message && response.message.successful) {
                    location.href = response.message.certificate_url
                } else {
                    alert(response.message.message)
                }
            },
            error: function(xhr) {
                console.error("Error submitting survey:", xhr.responseText);
            }
        });
    }
    
    function getAnswers() {
        let questions = {
            "questions": {},
            "survey": form.getAttribute("data-survey")
        }
        for(let form of answerForms) {
            const question = form.getAttribute("data-q")
            const formType = form.getAttribute("data-q-type")
            questions["questions"][question] = []
            if(formType === "Text") {
    
                const inputs = form.querySelectorAll(".form-answer")
                for(let input of inputs) {
                    if(input.value) {
                        questions["questions"][question].push(input.value)
                    }
                }
            } else {
                const inputs = form.querySelectorAll(".form-check-input");
                const values = form.querySelectorAll(".form-check-label");

                for(let i = 0; i < inputs.length; i++) {
                    const input = inputs[i];
                    const value = values[i].textContent.trim();
                    if(input.checked) {
                        questions["questions"][question].push(value);
                    }
                }
            }
        }
        return questions
    }

    function getQueryParam(param) {
        let urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }
    
    function getQInputs(form) {
        
    }
})