const baseUrl = "https://osus.wowdigital.sa"

this.elements = document.getElementsByClassName("lecture-item");
const lectureItems = document.querySelectorAll(".lecture-item");
const lecturesContainer = document.querySelector(".lectures");
const videoCard = document.querySelector(".video-card");
const video = document.querySelector(".video");
const article = document.querySelector(".article");
const qaItemSelector = document.getElementById("qa-item-selector");
const searchField = document.getElementById("search-qa");
const qaFilterSelector = document.getElementById("qa-filter-selector");
const completeBtn = document.getElementById("complete-btn");
const titleElement = document.getElementById("det-title");
const descriptionElement = document.getElementById("det-description");
const numberOfQuestions = document.getElementById("num-of-qa");
const questionsContainer = document.getElementById("accordionExample");
const repliesContainer = document.querySelector(".all-replies");
const replyField = document.getElementById("reply-field")
const replyBtn = document.getElementById("reply-btn");
const surveyBtn = document.getElementById("survey-btn");


const nextItemDialog = document.getElementById("next-item-dialog");

let videoCompleted = false;
let currentItemName = lecturesContainer.getAttribute("data-active");
let currentQName = "";

// qaItemSelector.addEventListener("change", (e)=> {
//   console.log(e.value)
// })


video.addEventListener('timeupdate', () => {
  const ninetyPercent = video.duration * 0.9;
  if (video.currentTime >= ninetyPercent && !videoCompleted) {
    videoCompleted = true;
    completeItem()
  }
  if (video.currentTime == video.duration) {
    nextItemDialog.classList.remove("next-dialog-hide")
    document.exitFullscreen();
  } else {
    nextItemDialog.classList.add("next-dialog-hide")
  }
});

// this.handleClick = this.handleClick.bind(this);

// Add event listeners to all elements with the specified class name
Array.from(lectureItems).forEach(element => {
  element.addEventListener('click', function(e){
    const itemName = e.target.getAttribute('data-id');
    const sameItem = itemName == currentItemName;

    if(!sameItem) {
      video.pause();
      currentItemName = itemName;
      const title = e.target.getAttribute('data-title');
      const det = e.target.getAttribute('data-det');
      // const type = e.target.getAttribute('data-type');
      titleElement.innerText=title;
      descriptionElement.innerText=det;
      const urlParams = new URLSearchParams(window.location.search);
      const courseId = urlParams.get('id');
      fetch(baseUrl+`/api/method/moneymaker.www.Osus.course_content.itemContent?id=${courseId}&course_item=${currentItemName}`)
      .then(response => response.json())
      .then(async res => {

        if(res.message.items && res.message.items.length > 0) {
          const course_item = res.message.items[0];
          
          await setMainContent(course_item)

          const userCompleted = res.message.completed;
          if(userCompleted === true) {
            completeBtn.style.display = "none";
            surveyBtn.style.display = "flex";
          } else {
            completeBtn.style.display = "flex";
          }
          activateItem(e.target);
        }
      })
      .catch(error => {
          console.log(error)
      });
      // frappe.call({
      //   method: "moneymaker.www.Osus.course_content.itemContent",
      //   args: {
      //       course_item: itemName
      //   },
      //   callback: function (res) {
      //     if(res.message.items && res.message.items.length > 0) {
      //       const course_item = res.message.items[0];
      //       setMainContent(course_item)
      //       const userCompleted = res.message.completed;
      //       if(userCompleted === true) {
      //         completeBtn.style.display = "none";
      //       }
      //       activateItem();
      //     }
      //   }
      // });
    }
  });
});

function searchQA(e) {
  const urlParams = new URLSearchParams(window.location.search);
  const courseId = urlParams.get('id');

  fetch(baseUrl+`/api/method/moneymaker.www.Osus.course_content.QA?id=${courseId}&search=${searchField.value}&course_item=${qaItemSelector.value}`)
    .then(response => response.json())
    .then(res => {
      updateQuestions(res.message)
    })
    .catch(error => {
        console.log(error)
    });
}

function likeQA(e) {
  const element = $(e);
  const parentElement = element.parent().parent().parent().parent();
  let numberOfLikes = parentElement.find(".clock").children()[1];
  const arrowElement = element.find(".fal");

  fetch(baseUrl+`/api/method/moneymaker.www.Osus.course_content.likeQA?qa_name=${parentElement.attr("data-question-id")}`)
  .then(response => response.json())
  .then(res => {

    if(res.message !== null) {

      if(res.message == true) {
        element.find(".txt").text(" useless ");
        numberOfLikes.innerHTML = parseInt(numberOfLikes.innerHTML.trim()) + 1
        arrowElement.removeClass("fa-arrow-up")
        arrowElement.addClass("fa-arrow-down")
      }else {
        element.find(".txt").text(" useful ");
        numberOfLikes.innerHTML = parseInt(numberOfLikes.innerHTML.trim()) - 1
        arrowElement.removeClass("fa-arrow-down")
        arrowElement.addClass("fa-arrow-up")
      }

    }
  })
  .catch(error => {
      console.log(error)
  });
}

function getQName(e) {
  const element = $(e);
  const parentElement = element.parent().parent().parent().parent();
  const qaId = parentElement.attr("data-question-id");

  currentQName = qaId;
  console.log(currentQName)
}

function writeReply(e) {

  fetch(baseUrl+`/api/method/moneymaker.www.Osus.course_content.writeReply?qa_name=${currentQName}&course_item=${currentItemName}&details=${replyField.value}`)
  .then(response => response.json())
  .then(res => {
    replyField.value = ""
  })
  .catch(error => {
      console.log(error)
  });
}

function updateQuestions(questions) {
  questionsContainer.innerHTML = ""
  let htmlStr = "";
  let index = 0;
  numberOfQuestions.innerText = `(${questions.length.toString()})`
  for (let qa of questions) {
    htmlStr += `
      <div class="accordion-item" data-question-id="${qa.name}">
          <h2 class="accordion-header">
          <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index}"
            aria-expanded="true" aria-controls="collapse${index}">
              <div class="user-info">
                  <div class="avatar">
                      <img src="https://osus.wowdigital.sa/${qa.image}" alt="" class="img-cover">
                  </div>
                  <div class="cont">
                      <h6 class="name"> ${qa.full_name} </h6>
                      <h5 class="ques"> ${qa.title} </h5>
                  </div>
              </div>
              <small class="clock" style="display: flex; justify-content: center; align-items: center; gap: 5px;"> <i class="fal fa-arrow-up"></i> <div>${qa.likes}</div> </small>
          </button>
          </h2>
          <div id="collapse${index}" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
              <div class="accordion-body">
                  <!-- <h5 class="mb-2"> ${qa.title} </h5> -->
                  <div class="text"> 
                      ${qa.question}
                  </div>
                  <div class="answer-tabs">
                      ${qa.liked ?
                        '<a type="button" onclick="return likeQA(this)"> <i class="fal fa-arrow-down"></i> <span class="txt"> useless </span> </a>':
                        '<a type="button" onclick="return likeQA(this)"> <i class="fal fa-arrow-up"></i> <span class="txt"> useful </span> </a>'
                      }
                      <a href="#0" data-bs-toggle="modal" data-bs-target="#modal-reply"> <i class="fal fa-message-arrow-up"></i> <span class="txt"> add reply </span> </a>
                      <a href="#0" data-bs-toggle="modal" data-bs-target="#modal-replies"> <i class="fal fa-eye"></i> <span class="txt" onclick="getReplies(this)"> show replies </span> </a>
                  </div>
              </div>
          </div>
      </div>
    `;
    index++;
  }
  questionsContainer.innerHTML = htmlStr;
}

function replayVideo() {
  video.currentTime = 0;
  video.play();
}

async function setMainContent(course_item) {

  if(course_item.type === "Video") {
    videoCompleted = false;
    article.style.display = "none";
    videoCard.style.display = "block";
    video.src = baseUrl+course_item.attachment;

  } else if(course_item.type === "Article") {
    videoCard.style.display = "none";
    article.style.display = "flex";
    article.style.flexDirection = "column";
    article.children[0].innerHTML = course_item.article

    if(course_item.state !== "Finished") {
      completeBtn.innerHTML = `
      <span class="txt">
                              
          Complete
          
      </span>`
      completeBtn.classList.add("butn-border")
      completeBtn.onclick = completeItem
    } else {
      completeBtn.innerHTML = `
      <span class="txt">
                              
          Next item
          
      </span>`
      completeBtn.classList.remove("butn-border")
      completeBtn.onclick = nextItem
    }

    completeBtn.innerHTML += `
    <span class="butn-icon">
        <span class="butn-icon-inner"><i class="fal fa-arrow-right"></i></span>
    </span>
    `;
  } else if(course_item.type === "Quiz") {
    let questions = await getQuiz(course_item.quiz);

    videoCard.style.display = "none";
    article.style.display = "flex";
    article.style.flexDirection = "column";
    let quiz_html = `<div class="quiz-form">`;

    const userAnswers = [];

    for(let i = 0; i < questions.length; i++) {
      let q = questions[i];
      quiz_html += `<div class="quiz-question" data-type="${q.question}" style="display: flex; flex-direction: column; align-items: start; margin-bottom: 30px; gap: 15px;">`;

      quiz_html += `
      <div style="display: flex;">
        <div style="width: 25px;"><strong>${i+1}.</strong></div>
        <div>${q.question}</div>
      </div>`

      for(let j = 0; j < q.options.length; j++) {
        let o = q.options[j];
        o["is_correct"] = 0
        quiz_html += `
          <div style="display: flex; gap: 10px; margin: 0px 25px; align-items: center">
            <input style="width: 1.1rem; height: 1.1rem; margin: 0px !important;" data-index="${j}" class="form-check" type="${q.type === "Multichoice"? "checkbox" : "radio"}" id="${q.question}-${o.option}" name="${q.question}" value="${o.option}">
            <label for="${q.question}-${o.option}">${o.option}</label>
          </div>
        `;
      }

      quiz_html += `</div>`;

      userAnswers.push({
        question: q.question,
        type: q.type,
        options: q.options
      });
    }

    console.log(userAnswers)

    quiz_html += `</div>`;
    article.children[0].innerHTML = quiz_html

    let inputs = document.querySelectorAll('.form-check');
    for(let i = 0; i < inputs.length; i++) {
      let input = inputs[i];
      input.addEventListener('change', () => {
        const questionName = input.name;
        const isChecked = input.checked;
        const optionIndex = parseInt(input.getAttribute("data-index"))

        const question = userAnswers.find(q => q.question === questionName);
        
        if (question) {
          question.options[optionIndex].is_correct = isChecked ? 1 : 0;
        }

        const final_object = {
          "quiz_name": course_item.quiz,
          "answered_questions": userAnswers
        }
        console.log(final_object)
        // validateQuiz(course_item.quiz, final_object)
      });
    }
  }
}

function validateQuiz(answered_questions) {
  fetch(
    baseUrl+`/api/method/moneymaker.www.Osus.course_content.validateQuiz`,
    {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        "quiz_name": quiz_name,
        "answered_questions": answered_questions,
      }),
    }
  )
    .then(response => response.json())
    .then(res => {
      if(res.message) {
        
      }
    })
    .catch(error => {
        console.log(error)
    });
}

async function getQuiz(quiz_name) {
  return await new Promise(function(resolve, reject) {
    fetch(baseUrl+`/api/method/moneymaker.www.Osus.course_content.itemQuiz?quiz_name=${quiz_name}`)
    .then(response => response.json())
    .then(res => {
      if(res.message) {
        resolve(res.message)
      }
    })
    .catch(error => {
        console.log(error)
        reject(error)
    });
  })
}

function getReplies(e) {
  const question = $(e).parent().parent().parent().parent().parent();
  const reference = question.attr("data-question-id")

  fetch(baseUrl+`/api/method/moneymaker.www.Osus.course_content.QAResponses?reference=${reference}`)
    .then(response => response.json())
    .then(res => {
      if(res.message) {
        const replies = res.message.replies
        const mainQ = res.message.mainQ

        $(repliesContainer).parent().children()[0].innerText = mainQ
        showReplies(replies);
      }
    })
    .catch(error => {
        console.log(error)
    });
}

function showReplies(replies) {
  repliesContainer.innerHTML = "";
  let htmlStr = "";
  
  for(let reply of replies) {
    htmlStr += `
      <div class="item">
        <div class="avatar">
          <img src="${baseUrl}${reply.user_image}" alt="" class="img-cover">
        </div>
        <div class="cont">
          <h6 class="name"> ${reply.full_name} </h6>
          <div class="text"> ${reply.question} </div>
        </div>
      </div>
    `;
  }

  repliesContainer.innerHTML = htmlStr;
}

function activateItem(lectureButton) {
  fetch(baseUrl+`/api/method/moneymaker.www.Osus.course_content.activateItem?course_item=${currentItemName}`)
  .then(response => response.json())
  .then(res => {
    console.log(res.message)
    for(let lec of lectureItems) {
      lec.classList.remove("active-item")
    }
    lectureButton.classList.add("active-item")
  })
  .catch(error => {
      console.log(error)
  });
  // frappe.call({
  //   method: "moneymaker.www.Osus.course_content.activateItem",
  //   args: {
  //       course_item: currentItemName
  //   },
  //   callback: function (res) {
  //     console.log(res.message)
  //     // if(res.message.active) {
        
  //     // }
  //   }
  // });
}

function nextItem() {
  
  fetch(baseUrl+`/api/method/moneymaker.www.Osus.course_content.nextItem?course_item=${currentItemName}`)
  .then(response => response.json())
  .then(async res => {
    console.log(res.message)
    if(res.message.item != null) {
      const newItem = res.message.item;
      currentItemName = newItem.name;
      titleElement.innerText = newItem.title
      descriptionElement.innerText = newItem.description
      nextItemDialog.classList.add("next-dialog-hide")
      await setMainContent(newItem);

      const userCompleted = res.message.completed;
      if(userCompleted === true) {
        completeBtn.style.display = "none";
        surveyBtn.style.display = "flex";
      } else {
        completeBtn.style.display = "flex";
        activateItem();
      }
    }
  })
  .catch(error => {
      console.log(error)
  });
  // frappe.call({
  //   method: "moneymaker.www.Osus.course_content.nextItem",
  //   args: {
  //       course_item: currentItemName
  //   },
  //   callback: function (res) {
  //     if(res.message.item != null) {
  //       console.log(res.message)
  //       const newItem = res.message.item;
  //       currentItemName = newItem.name;
  //       titleElement.innerText = newItem.title
  //       descriptionElement.innerText = newItem.description
  //       nextItemDialog.classList.add("next-dialog-hide")
  //       setMainContent(newItem);

  //       const userCompleted = res.message.completed;
  //       if(userCompleted === true) {
  //         completeBtn.style.display = "none";
  //       }
  //     }
  //   }
  // });
}

function completeItem() {
  fetch(baseUrl+`/api/method/moneymaker.www.Osus.course_content.completeItem?course_item=${currentItemName}`)
  .then(response => response.json())
  .then(res => {

    if(res.message.completed) {
      completeBtn.innerHTML = `
      <span class="txt">
                              
          Next item
          
      </span>`
      completeBtn.classList.remove("butn-border")
      completeBtn.onclick = nextItem
      
      completeBtn.innerHTML += `
      <span class="butn-icon">
          <span class="butn-icon-inner"><i class="fal fa-arrow-right"></i></span>
      </span>
      `;
      updateItem();
    }

    if(res.message.finished === true) {
      completeBtn.style.display = "none";
      surveyBtn.style.display = "flex";
    } else {
      completeBtn.style.display = "flex";
    }
  })
  .catch(error => {
      console.log(error)
  });
  // frappe.call({
  //   method: "moneymaker.www.Osus.course_content.completeItem",
  //   args: {
  //       course_item: currentItemName
  //   },
  //   callback: function (res) {
  //     if(res.message.completed) {
  //       updateItem();
  //     }
  //   }
  // });
}

function updateItem() {
  const updatedItems = lecturesContainer.querySelectorAll(`[data-id="${currentItemName}"]`);
 
  if(updatedItems.length > 0) {
    const item = updatedItems[0];
    const checkBox = item.querySelector(".form-check").children[0];
    checkBox.checked = true
  }
}
