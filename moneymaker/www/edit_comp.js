document.addEventListener("DOMContentLoaded", (e) => {
    const preLoader = document.getElementById("preloader");
    hideLoader();

    $("#edit-form").on("submit", async function(event) {
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
            url: "/api/method/moneymaker.www.edit_comp.edit_profile",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(jsonData),
            success: async function (response) {
                if(response.message && response.message.passed == true) {
                    hideLoader();
                }
            },
            error: function (xhr, status, error) {
                hideLoader();
                alert("حدث خطأ أثناء تحديث بياناتك.");
                console.log(error);
            }
        });
    
    
        async function uploadFile(field, file, profileName) {
            return new Promise((resolve, reject) => {
                const fileFormData = new FormData();
                fileFormData.append("file", file);
                fileFormData.append("is_private", 0); // 0 for public, 1 for private
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