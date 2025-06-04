document.addEventListener("DOMContentLoaded", (e) => {
  const brandName = document.body.getAttribute("data-brand");
  const institution = document.body.getAttribute("data-inst");
  const loginBlock = document.getElementById("login-block");
  const otpBlock = document.getElementById("otp-block");
  const toEmail = document.getElementById("to-email");
  const preLoader = document.getElementById("preloader");
  const timer = document.getElementById("timer")
  // const registerBtn = document.getElementById("login-btn")

  // registerBtn.onclick = login

  hideLoader();

  function login() {
    let email = $("#email").val().trim();
    let password = $("#password").val().trim();

    if (email === "" || password === "") {
        alert("يرجى إدخال البريد الإلكتروني وكلمة المرور");
        return;
    }

    showLoader();

    $.ajax({
        url: "/api/method/login",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ usr: email, pwd: password }),
        success: function (response) {
            if(response.message === "Logged In") {
                setCookie("institution", institution, 7);
                window.location.href = "/";
            }
            else if(response && response.verification && response.verification.token_delivery == true) {
                otpBlock.style.display = "block";
                loginBlock.style.display = "none";
                tmp_id = response.tmp_id;
                toEmail.textContent = email;
                startTimer();
            }
            hideLoader();
        },
        error: function (xhr, status, error) {
            hideLoader();
            alert("فشل تسجيل الدخول! يرجى التحقق من بياناتك.");
        }
    });
  }

  function confirmOTP() {
    const email = $("#email").val().trim();
    const password = $("#password").val().trim();
    const otp = $("#otp").val().trim();

    if (!otp || otp.length < 6) {
        alert("يرجى إدخال الرمز المرسل إلى البريد الإلكتروني");
        return;
    }

    showLoader();

    $.ajax({
        url: "/api/method/moneymaker.www.login.confirm_otp",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(
            {
                email: email,
                password: password,
                "tmp_id": tmp_id,
                "otp": otp
            }
        ),
        success: function (response) {
            if(response.message.status == 200) {
                if(response.message.message) {
                    location.reload();
                }
            } else {
                hideLoader();
                alert("الرمز المدخل غير صحيح");
            }
        },
        error: function (xhr, status, error) {
            hideLoader();
            alert("فشل تسجيل الدخول! يرجى التحقق من بياناتك.");
        }
    });
  }

  function startTimer() {
    $("#resend-otp").prop("disabled", true);

    let timeLeft = 60;

    const countdown = setInterval(() => {
      if (timeLeft <= 0) {
        clearInterval(countdown);
        timer.textContent = "0";
        $("#resend-otp").prop("disabled", false);
      } else {
        timer.textContent = timeLeft;
        timeLeft--;
      }
    }, 1000);
  }
  
  $("#login-form").on("submit", function (event) {
    event.preventDefault();
    login();
  });

  $("#otp-form").on("submit", function (event) {
    event.preventDefault();
    confirmOTP();
  });

  $("#resend-otp").on("click", function (event) {
    login();
  });

  function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + "; path=/" + expires;
  }

  function hideLoader() {
    preLoader.style.display = "none";
  }

  function showLoader() {
    preLoader.style.display = "inline";
  }
})