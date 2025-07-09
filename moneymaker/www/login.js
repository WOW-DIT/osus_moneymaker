$(document).ready(function () {
    const loginBlock = document.getElementById("login-block");
    const otpBlock = document.getElementById("otp-block");
    const toEmail = document.getElementById("to-email");
    const preLoader = document.getElementById("preloader");
    let tmp_id = null;
    // checkLogin();

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
                    window.location.href = "/";
                }
                else if(response && response.verification && response.verification.token_delivery == true) {
                    otpBlock.style.display = "flex";
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
        loginDemo();
    });

    $("#otp-form").on("submit", function (event) {
        event.preventDefault();
        confirmOTP();
    });

    $("#resend-otp").on("click", function (event) {
        loginDemo();
    });

    function checkLogin() {
        const isLogged = document.body.getAttribute("data-login")

        if(isLogged === "True") {
            location.href = "/";
        }
    }

    function getCookie(name) {
        const cookieString = document.cookie;
        const cookies = cookieString.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            console.log(cookie)
            // Check if the cookie starts with the desired name
            if (cookie.startsWith(name + "=")) {
                // Extract and return the cookie value
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
      
        return null; // Cookie not found
    }

    function hideLoader() {
        preLoader.style.display = "none";
    }
    
    function showLoader() {
        preLoader.style.display = "inline";
    }

    function loginDemo() {
      let email = $("#email").val().trim();
      let password = $("#password").val().trim();

      if (email === "" || password === "") {
          alert("يرجى إدخال البريد الإلكتروني وكلمة المرور");
          return;
      }

      // Simulate OTP requirement
      otpBlock.style.display = "block";
      loginBlock.style.display = "none";
      toEmail.textContent = email;
      startTimer();

      // Wait for OTP form submit (simulating backend asking for OTP)
      $("#otp-form").off("submit").on("submit", function (event) {
          event.preventDefault();
          
          const otp = $("#otp").val().trim();
          if (otp !== "123456") {
              alert("رمز التحقق غير صحيح (استخدم 123456 للتجربة)");
              return;
          }

          showLoader();

          // Now perform real login
          $.ajax({
              url: "/api/method/login",
              type: "POST",
              contentType: "application/json",
              data: JSON.stringify({ usr: email, pwd: password }),
              success: function (response) {
                  if (response.message === "Logged In") {
                    //   setCookie("institution", institution, 7);
                      location.href = "/";
                  } else {
                      hideLoader();
                      alert("فشل تسجيل الدخول! يرجى التحقق من بياناتك.");
                  }
              },
              error: function (xhr, status, error) {
                  hideLoader();
                  alert("فشل تسجيل الدخول! يرجى التحقق من بياناتك.");
              }
          });
      });
    }
});