
document.addEventListener("DOMContentLoaded", (e) => {
     const preLoader = document.getElementById("preloader");
     var pass=document.getElementById("pass");
     var conf_pass=document.getElementById("conf_pass");
     hideLoader();

    $("#edit-form").on("submit", async function(event) {
        event.preventDefault(); // Prevent default form submission
        if(pass.value && pass.value != conf_pass.value) {
            conf_pass.style="border-color: red;"
            alert("كلمة السر غير متطابقة");
            return;
        } else{
            conf_pass.style="border-color: none;"
        }

        const formData = new FormData(this);
        const params = new URLSearchParams();
        const jsonData = Object.fromEntries(formData.entries());
    
        formData.forEach((value, field) => {
            if (!(value instanceof File)) {
                if(value!="")
                {params.append(field, value);}
            }
        });
        showLoader();
  
        $.ajax({
            url: "/api/method/moneymaker.www.api.edit_profile.edit_profile",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(jsonData),
            success: async function (response) {
                if(response.message && response.message.passed == true) {
                    hideLoader();
                    window.location.href="profile";
                }
            },
            error: function (xhr, status, error) {
                 hideLoader();
                alert("حدث خطأ أثناء تحديث بياناتك.");
                console.log(error);
            }
        });
    });

    function hideLoader() {
        preLoader.style.display = "none";
    }
    
    function showLoader() {
        preLoader.style.display = "inline";
    }

    $("#conf_pass").on("change", async function(event) {
        event.preventDefault();
        console.log(this.value);
        if(pass.value!=this.value)
        {
            this.style="border-color: red;"
        }else{
            this.style="border-color: none;"
            console.log("ok");
        }
    });
})