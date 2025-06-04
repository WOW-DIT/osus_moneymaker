document.addEventListener("DOMContentLoaded", (e) => {
    const password = document.getElementById("pass");
    const confirmPassword = document.getElementById("cpass");
    const submit = document.getElementById("submit-btn");
    const termsCheckbox = document.getElementById("terms-checkbox");
    const passError = document.getElementById("pass-error");
    const preLoader = document.getElementById("preloader");
    hideLoader();
    
    function enableDisableBtn() {
        if (password.value !== confirmPassword.value) {
            passError.style.display = "inline";
            confirmPassword.classList.add("error-input")
        } else {
            passError.style.display = "none";
            confirmPassword.classList.remove("error-input")
        }
    }
    
    password.addEventListener("input", enableDisableBtn);
    confirmPassword.addEventListener("input", enableDisableBtn);
    termsCheckbox.addEventListener("change", (e) => {
        if(e.target.checked) {
            submit.disabled = false;
        } else {
            submit.disabled = true;
        }
    });
    
    document.getElementById("reg_form").addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent default form submission
    
        const formData = new FormData(this);
        const jsonData = Object.fromEntries(formData.entries());
        console.log(jsonData);
        
        // Add files
        const files = [];
    
        formData.forEach((value, field) => {
            if (value instanceof File) {
                files.push({ field, file: value });
            }
        });

        showLoader();

        $.ajax({
            url: "/api/method/moneymaker.www.register_user.register",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(jsonData),
            success: async function (response) {
                
                if(response.message && response.message.passed == true) {
                    try {
                        const profileName = response.message.profile_name;
                        const uploadPromises = files.map(({ field, file }) => uploadFile(field, file, profileName));
                        
                        // Wait for all files to upload
                        const results = await Promise.all(uploadPromises);
                
                        console.log("All files uploaded successfully:", results);
                        
                        window.location.href = "/login";
    
                    } catch (error) {
                        hideLoader();
                        console.error("Error uploading files:", error);
                        alert("Failed to upload one or more files.");
                    }
                }
            },
            error: function (xhr, status, error) {
                alert("فشل تسجيل الدخول! يرجى التحقق من بياناتك.");
                console.log(error);
            }
        });
    
    
        async function uploadFile(field, file, profileName) {
            return new Promise((resolve, reject) => {
                const fileFormData = new FormData();
                fileFormData.append("file", file);
                fileFormData.append("is_private", 1); // 0 for public, 1 for private
                fileFormData.append("doctype", "Profile"); // Change this based on where the file should be linked
                fileFormData.append("docname", profileName); // Adjust this to match your use case
                fileFormData.append("fieldname", field); // Attach the file to the correct field
                $.ajax({
                    url: "/api/method/upload_file",
                    type: "POST",
                    processData: false,
                    contentType: false,
                    data: fileFormData,
                    success: function (response) {
                        console.log("File uploaded successfully:", response);
                        resolve(response);
                    },
                    error: function (xhr, status, error) {
                        console.error(`File upload failed for field: ${field}`, error);
                        reject({ field, error }); // Return field name and error
                    }
                });
            });
        }    
    });

    function hideLoader() {
        preLoader.style.display = "none";
    }
    
    function showLoader() {
        preLoader.style.display = "inline";
    }
})
