// this.elements = document.getElementsByClassName("lecture-item");
const lectureItems = document.querySelectorAll(".lecture-item");
const lecturesContainer = document.querySelector(".lectures");
const article = document.querySelector(".article");
const qaItemSelector = document.getElementById("qa-item-selector");
const searchField = document.getElementById("search-qa");
const qaFilterSelector = document.getElementById("qa-filter-selector");
const completeBtn = document.getElementById("complete-btn");
const nextBtn = document.getElementById("next-btn");
const retakeQuizBtn = document.getElementById("retake-quiz-btn");
const quizBtn = document.getElementById("quiz-btn");
const titleElement = document.getElementById("det-title");
const descriptionElement = document.getElementById("det-description");
const numberOfQuestions = document.getElementById("num-of-qa");
const questionsContainer = document.getElementById("accordionExample");
const repliesContainer = document.querySelector(".all-replies");
const replyField = document.getElementById("reply-field")
const replyBtn = document.getElementById("reply-btn");
const surveyBtn = document.getElementById("survey-btn");
const onlineBtn = document.getElementById("online-btn");
const meetingWindow = document.querySelector(".meeting-window");
const onlineFrame = document.getElementById("online-frame");
const preLoader = document.getElementById("preloader");
hideLoader();

let videoCompleted = false;
let currentItemName = lecturesContainer.getAttribute("data-active");
let currentQName = "";
let final_object = null;


completeBtn.onclick = completeItem
nextBtn.onclick = nextItem
retakeQuizBtn.onclick = retakeQuiz


if(onlineBtn !== null) {
  onlineBtn.onclick = setMeeting
}

// #####################################
//         START VIDEO CONTROLS
// #####################################
const videoCard = document.getElementById("video-wrapper");
const video = document.querySelector(".video");
const nextItemDialog = document.getElementById("next-item-dialog");
const seekBar = document.getElementById('seekBar');
const volumeSlider = document.getElementById('volumeSlider');
const muteBtn = document.getElementById("muteBtn");
const subtitleBtn = document.getElementById("subtitleBtn");
const playImg = document.getElementById("play-img")

function playPause() {
  if (video.paused) {
    video.play();
    // Switch to pause icon
    playImg.src = playImg.src.replace("play", "pause");
  } else {
    video.pause();
    // Switch to play icon
    playImg.src = playImg.src.replace("pause", "play");
  }
}

document.querySelectorAll('#custom-controls a, #custom-controls input, #next-item-dialog').forEach(el => {
  el.addEventListener('click', (e) => {
    e.stopPropagation(); // stop click from affecting video wrapper
  });
});

video.addEventListener('timeupdate', () => {
  seekBar.value = Math.floor((video.currentTime / video.duration) * 100);
  const ninetyPercent = video.duration * 0.9;
  if (video.currentTime >= ninetyPercent && !videoCompleted) {
    videoCompleted = true;
    completeItem()
  }
});

document.addEventListener('contextmenu', event => {
  if (event.target.tagName === 'VIDEO') {
    event.preventDefault();
  }
});
volumeSlider.addEventListener('input', () => {
  video.volume = volumeSlider.value;
});
// Seek bar change
seekBar.addEventListener('input', () => {
  const seekTo = (seekBar.value / 100) * video.duration;
  video.currentTime = seekTo;
});

muteBtn.addEventListener('click', function (e) {
  e.stopPropagation(); // prevent triggering play/pause
  video.muted = !video.muted;
  muteBtn.textContent = video.muted ? '🔇' : '🔊';
});

function toggleFullscreen() {
  const wrapper = document.getElementById('video-wrapper');
  if (!document.fullscreenElement) {
    wrapper.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
}

function toggleSubtitles() {
  const tracks = video.textTracks;
  for (let i = 0; i < tracks.length; i++) {
    const track = tracks[i];

    if (track.mode === "showing") {
      track.mode = "hidden";
      subtitleBtn.textContent = "💬❌"; // update icon (optional)
    } else {
      track.mode = "showing";
        subtitleBtn.textContent = "💬"; // update icon (optional)
    }
  }
  
}

function hideAllSubtitles() {
  const tracks = video.textTracks;
  for (let i = 0; i < tracks.length; i++) {
    tracks[i].mode = "hidden";
  }
}


videoCard.addEventListener('click', () => {
  playPause();
});

// Double click = toggle fullscreen
videoCard.addEventListener('dblclick', () => {
  if (!document.fullscreenElement) {
    videoCard.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
});
// Automatically show overlay when video ends
video.addEventListener("ended", () => {
  nextItemDialog.style.display = "flex";
});

// Replay the same video
function replayVideo() {
  nextItemDialog.style.display = "none";
  video.currentTime = 0;
  video.play();
}
// #####################################
//          END VIDEO CONTROLS
// #####################################

// this.handleClick = this.handleClick.bind(this);

// Add event listeners to all elements with the specified class name
Array.from(lectureItems).forEach(element => {
  element.addEventListener('click', function(e){
    showLoader();
    const target = e.currentTarget;
    const itemName = target.getAttribute('data-id');
    const sameItem = itemName == currentItemName;

    if(!sameItem) {
      video.pause();
      currentItemName = itemName;
      const title = target.getAttribute('data-title');
      const det = target.getAttribute('data-det');
      // const type = target.getAttribute('data-type');
      titleElement.innerText=title;
      descriptionElement.innerText=det;
      const urlParams = new URLSearchParams(window.location.search);
      const courseId = urlParams.get('id');
      fetch(`/api/method/moneymaker.www.api.course_content.itemContent?id=${courseId}&course_item=${currentItemName}`)
      .then(response => response.json())
      .then(async res => {

        if(res.message.items && res.message.items.length > 0) {
          const course_item = res.message.items[0];

          await setMainContent(course_item, res.message.subtitles)

          const userCompleted = res.message.completed;
          if(userCompleted === true) {
            completeBtn.style.display = "none";

            if(course_item.has_next) {
              nextBtn.style.display = "flex";
            }

            const finishedSurvey = res.message.finished_survey;
            if(finishedSurvey) {
              surveyBtn.style.display = "none";
            } else {
              surveyBtn.style.display = "flex";
            }
            
          } else {
            // completeBtn.style.display = "flex";
          }
          activateItem(target);
        }
        hideLoader();
      })
      .catch(error => {
          console.log(error)
          hideLoader();
      });
    }
  });
});

function searchQA(e) {
  const urlParams = new URLSearchParams(window.location.search);
  const courseId = urlParams.get('id');

  fetch(`/api/method/moneymaker.www.api.course_content.QA?id=${courseId}&search=${searchField.value}&course_item=${qaItemSelector.value}`)
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

  fetch(`/api/method/moneymaker.www.api.course_content.likeQA?qa_name=${parentElement.attr("data-question-id")}`)
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

  fetch(`/api/method/moneymaker.www.api.course_content.writeReply?qa_name=${currentQName}&course_item=${currentItemName}&details=${replyField.value}`)
  .then(response => response.json())
  .then(res => {
    replyField.value = ""
  })
  .catch(error => {
      console.log(error)
  });
}

function updateButtons(type, state, has_next, can_retake=false, passed=true, finished=null) {
  // debugger
  if(state === "Finished") {
    completeBtn.style.display = "none";
    nextBtn.style.display = "flex";

    if(has_next && passed) {
      nextBtn.style.display = "flex";
    } else {
      nextBtn.style.display = "none";
    }
    
    if(type === "Quiz") {
      if(can_retake) {
        retakeQuizBtn.style.display = "flex";
      }
    } else {
      retakeQuizBtn.style.display = "none";
    }

  } else {
    completeBtn.style.display = "flex";
    nextBtn.style.display = "none";
    retakeQuizBtn.style.display = "none";

    if(type === "Quiz") {
      completeBtn.innerHTML = `
      <span class="readable">            
          حفظ
      </span>`;
      completeBtn.onclick = submitQuiz;
    } else {
      completeBtn.innerHTML = `
      <span class="readable">            
          إكمال
      </span>`;
      completeBtn.onclick = completeItem;
    }
  }
}

function updateQuestions(questions) {
  questionsContainer.innerHTML = ""
  let htmlStr = "";
  let index = 0;
  numberOfQuestions.innerText = `(${questions.length.toString()})`
  for (let qa of questions) {
    const index_string = index.toString();
    htmlStr += `
      <div class="accordion-item" data-question-id="${qa.name}">
          <h2 class="accordion-header">
          <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index_string}"
            aria-expanded="true" aria-controls="collapse${index_string}">
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
          <div id="collapse${index_string}" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
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

async function setMainContent(course_item, subtitles) {
  resetMeeting();

  video.innerHTML = "";
  nextItemDialog.style.display = "none";
  video.src = null;

  if(course_item.type === "Video") {
    videoCompleted = false;
    article.style.display = "none";
    videoCard.style.display = "flex";
    videoCard.style.flexDirection = "column";
    videoCard.style.justifyContent = "center";
    playImg.src = playImg.src.replace("play", "pause");
    
    video.src = course_item.attachment;

    if(subtitles !== null) {
      
      video.innerHTML = ""

      let tracks = ""
      for(let sub of subtitles) {
        tracks += `<track class="main-subtitle" src="${sub.file}" kind="subtitles" srclang="${sub.language}"></track>`
        break
      }
      video.innerHTML = tracks
    }
    toggleSubtitles();

  } else if(course_item.type === "Article") {
    videoCard.style.display = "none";
    article.style.display = "flex";
    article.style.flexDirection = "column";
    article.children[0].innerHTML = course_item.article

    updateButtons(course_item.type, course_item.state, course_item.has_next)

  } else if(course_item.type === "Quiz") {
    let questions = await getQuiz(course_item.quiz, course_item.state);
    
    videoCard.style.display = "none";
    article.style.display = "flex";
    article.style.flexDirection = "column";

    // Start Quiz
    let quiz_html = `
    <div class="quiz_box quiz-form">
      <div class="survey_pg">
    `;

    if(course_item.state == "Finished") {
      quiz_html += `
        <div class="d-flex justify-content-between">
          <h4 class="text-end">${parseFloat(course_item.quiz_mark).toFixed(2)}%</h4> 
          <h6>${course_item.passed=="1"? "نجحت في تخطي التقييم": "فشلت في تخطي التقييم. أعد مرة أخرى"}</h6>
        </div>
      `
    }

    quiz_html += `<div class="form_box">`

    const userAnswers = [];

    // Quiz Questions
    for(let i = 0; i < questions.length; i++) {
      let q = questions[i];
      const answerState = q.answer_state;
      const checkedOptions = q.checked_options;

      let backgroundStyle = "";

      if(course_item.state == "Finished") {
        backgroundStyle = `style="background-color: ${answerState=="correct" || answerState=="partially_correct"? "#00ff003b" : answerState == "incorrect"? "#ff00003b": "transparent"} !important"`
      }

      quiz_html += `
        <div class="ques_box quiz-question" data-type="${q.question}">
          <h6 class="title fw-bold mb-4 readable"> ${q.question} </h6>
      `;

      q.images.forEach(image => {
        quiz_html += `
          <img class="mb-5" src="${image.images}" alt="" style="width: 100%;">
        `;
      });

      // Quiz Options
      if(q.type !== "Matching") {
        for(let j = 0; j < q.options.length; j++) {
          let o = q.options[j];
  
          o["is_correct"] = 0
          
          quiz_html += `
            <div class="form-check"
              ${course_item.state == "Finished"? checkedOptions[j] == "1"? backgroundStyle : "" : ""}
            >
                <input ${course_item.state == "Finished"? "disabled" : ""} data-index="${j}" type="${q.type === "Multichoice"? "checkbox" : "radio"}" class="form-check-input" id="${q.question}-${o.option}" name="${q.question}" value="${o.option}"
                ${course_item.state == "Finished"? checkedOptions[j] == "1"? "checked" : "" : ""}
                >
                <label class="form-check-label readable" for="${q.question}-${o.option}">${o.option}</label>
            </div>
          `;
        }
      } else {
        quiz_html += `
          <div class="d-flex">
            <div class="d-flex flex-column justify-content-center align-items-start gap-3" style="width: 50%">
        `;
        q.matching_questions.forEach(mo => {
          quiz_html += `
              <div class="d-flex justify-content-start gap-2">
                  <div>${mo.matching_number}-</div>
                  <div>${mo.option}</div>
              </div>
          `;
        });
        quiz_html += `
            </div>
            <div class="d-flex flex-column justify-content-center align-items-center gap-3" style="width: 50%">
        `;

        let answer_index = 0;
        q.matching_answers.forEach(mo => {
          mo.matching_number = "";
          quiz_html += `
              <div class="d-flex justify-content-center gap-2" ${course_item.state == "Finished"? q.answers[answer_index] == "1"? backgroundStyle : "" : ""}>
                  <input
                    class="matching-input text-center w-25"
                    name="${q.question}"
                    data-index="${answer_index}"
                    type="number"
                    value="${course_item.state == "Finished"? q.matching_values[answer_index] : ""}"
                    ${course_item.state == "Finished"? "disabled" : ""}
                  >
                  <div>${mo.option}</div>
              </div>
          `;
          answer_index++;
        });
        quiz_html += `
            </div>
          </div>
          ${answerState == "partially_correct"? "<div>The answer is partially correct.</div>" : ""}
        `;
      }

      quiz_html += `</div>`;

      userAnswers.push({
        question_id: q.question_id,
        question: q.question,
        type: q.type,
        options: q.options,
        matching_answers: q.matching_answers,
      });
    }

    // Quiz Buttons
    quiz_html += `<div class="col-lg-3 ms-auto">`;
    
    quiz_html += `</div>`;

    // End Quiz
    quiz_html += `
          </div>
        </div>
      </div>
    `;

    article.children[0].innerHTML = quiz_html

    
    const canRetake = course_item.current_attempts < course_item.max_attempts;

    updateButtons(course_item.type, course_item.state, course_item.has_next, canRetake, course_item.passed=="1")

    if(course_item.state == "Active") {
      listenToQuiz(userAnswers, course_item);
    }
  }
}

function listenToQuiz(userAnswers, course_item) {
  let inputs = document.querySelectorAll('.form-check-input');
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

      final_object = {
        "quiz_name": course_item.quiz,
        "answered_questions": userAnswers
      }
    });
  }

  inputs = document.querySelectorAll('.matching-input');
  for(let i = 0; i < inputs.length; i++) {
    let input = inputs[i];
    input.addEventListener('change', () => {
      const questionName = input.name;
      const answerValue = input.value;
      const optionIndex = parseInt(input.getAttribute("data-index"))

      const question = userAnswers.find(q => q.question === questionName);

      if (question) {
        question.matching_answers[optionIndex].matching_number = answerValue;
      }

      final_object = {
        "quiz_name": course_item.quiz,
        "answered_questions": userAnswers
      }
    });
  }
}

function retakeQuiz() {
  showLoader();
  fetch(
    `/api/method/moneymaker.www.api.course_content.retakeQuiz`,
    {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        "course_item": currentItemName,
      }),
    }
  )
    .then(response => response.json())
    .then(res => {
      if(res.message.passed == true) {
        location.reload()
        // completeItem()
      }
      hideLoader();
    })
    .catch(error => {
      hideLoader();
      console.log(error)
    });
}

function submitQuiz() {
  if(final_object) {
    validateQuiz(final_object)
  } else {
    alert("جميع الحقول مطلوبة")
  }
}

function validateQuiz(quiz_object) {
  showLoader();
  fetch(
    `/api/method/moneymaker.www.api.course_content.validateQuiz`,
    {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        "quiz_name": quiz_object.quiz_name,
        "answered_questions": quiz_object.answered_questions,
        "course_item": currentItemName,
      }),
    }
  )
    .then(response => response.json())
    .then(res => {
      if(res.message.status == 200) {
        disabledInputs();
        completeItem(true);
      }

      hideLoader();
    })
    .catch(error => {
        console.log(error)
        hideLoader();
        alert(error.toString())
    });
}

function disabledInputs() {
  let inputs = document.querySelectorAll('.form-check-input');
  for(let i = 0; i < inputs.length; i++) {
    const input = inputs[i];
    input.disabled = true;
  }
}

async function getQuiz(quiz_name, state) {
  return await new Promise(function(resolve, reject) {
    fetch(`/api/method/moneymaker.www.api.course_content.itemQuiz?quiz_name=${quiz_name}&state=${state}`)
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
  const question = $(e).parent().parent().parent().parent();
  const reference = question.attr("data-question-id")

  fetch(`/api/method/moneymaker.www.api.course_content.QAResponses?reference=${reference}`)
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
      <div class="data msg_data_box">
        <p class="date mb-2">
            <i class="fa-light fa-calendar-days"></i> ${reply.date.split(".")[0]}
        </p>
        <div> ${reply.full_name} </div>
        <div> ${reply.question} </div>
      </div>
    `;
  }

  repliesContainer.innerHTML = htmlStr;
}

function activateItem(lectureButton=null) {
  fetch(`/api/method/moneymaker.www.api.course_content.activateItem?course_item=${currentItemName}`)
  .then(response => response.json())
  .then(res => {
    changeItemLook(lectureButton);
  })
  .catch(error => {
      console.log(error)
  });
}

function changeItemLook(lectureButton) {
  if (lectureButton) {
    // Direct selection
    for (let lec of lectureItems) {
      lec.classList.remove("active");
    }
    lectureButton.classList.add("active");

    expandCurrentModule(lectureButton);
  } else {
    // Select next item
    let found = false;
    for (let i = 0; i < lectureItems.length; i++) {
      const lec = lectureItems[i];
      if (lec.classList.contains("active")) {
        lec.classList.remove("active");
        // Add active to the next item if it exists
        if (i + 1 < lectureItems.length) {
          lectureItems[i + 1].classList.add("active");

          expandCurrentModule(lectureItems[i + 1]);
        }
        break; // Exit loop once we've moved to the next
      }
    }
  }
}

function expandCurrentModule(lectureButton) {
  const selectedId = lectureButton.getAttribute("data-id");
  const modules = document.querySelectorAll(".module");
  // get the module where the lectureButton exists in and expand it and collapse the rest using for loop
  for(let i = 0; i < modules.length; i++) {
    const module = modules[i];

    const matchingItem = module.querySelector(`.lecture-item[data-id="${selectedId}"]`);
    const header = module.querySelector(".module-header");
    const body = module.querySelector(".module-body");

    if(matchingItem) {
      header.classList.remove("collapsed")
      header.setAttribute("aria-expanded", "true");

      body.classList.add("show");
    } else {
      header.classList.add("collapsed")
      header.setAttribute("aria-expanded", "false");

      body.classList.remove("show");
    }
  }
}


function nextItem() {
  showLoader();
  fetch(`/api/method/moneymaker.www.api.course_content.nextItem?course_item=${currentItemName}`)
  .then(response => response.json())
  .then(async res => {
    
    if(res.message.item != null) {
      // toggleSubtitles()
      const newItem = res.message.item;
      const subtitles = res.message.subtitles;

      currentItemName = newItem.name;
      titleElement.innerText = newItem.title
      descriptionElement.innerText = newItem.description

      await setMainContent(newItem, subtitles);

      const userCompleted = res.message.completed;
      
      if(userCompleted === true) {
        changeItemLook()
        if(!newItem.has_next) {
          completeBtn.style.display = "none";
        }
        
        const finishedSurvey = res.message.finished_survey;
        if(finishedSurvey) {
          surveyBtn.style.display = "none";
        } else {
          surveyBtn.style.display = "flex";
        }
      } else {
        // completeBtn.style.display = "flex";
        activateItem();
      }

    }
    hideLoader();
  })
  .catch(error => {
      console.log(error)
      hideLoader();
  });
}

function completeItem(reload=false) {
  showLoader();
  fetch(`/api/method/moneymaker.www.api.course_content.completeItem?course_item=${currentItemName}`)
  .then(response => response.json())
  .then(res => {

    if(res.message.completed) {
      completeBtn.innerHTML = `
      <span class="readable">      
        التالي
      </span>`
      completeBtn.onclick = nextItem
      
      updateItem();
    }

    if(res.message.finished == true) {
      completeBtn.style.display = "none";
      surveyBtn.style.display = "flex";
    } else {
      completeBtn.style.display = "flex";
    }
    if(reload) {
      location.reload();
    }
    hideLoader();
  })
  .catch(error => {
    hideLoader();
    console.log(error)
  });
}

function updateItem() {
  const updatedItems = lecturesContainer.querySelectorAll(`[data-id="${currentItemName}"]`);
  
  if(updatedItems.length > 0) {
    const item = updatedItems[0];
    const checkBox = item.querySelector(".form-check-input");
    checkBox.checked = true
  }
}


function setMeeting() {
  const link = onlineBtn.getAttribute("data-link")
  onlineFrame.src = link;
  video.src = "";
  article.style.display = "none";
  videoCard.style.display = "none";
  meetingWindow.style.display = "block";
  currentItemName = ""
}

function resetMeeting() {
  onlineFrame.src = "";
  meetingWindow.style.display = "none";
}

function hideLoader() {
  preLoader.style.display = "none";
}

function showLoader() {
  preLoader.style.display = "inline";
}