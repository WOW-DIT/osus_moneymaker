document.addEventListener("DOMContentLoaded", (e) => {
    document.getElementById('registerBtn').addEventListener('click', function(e) {
        e.preventDefault(); // Prevent form submission

        // Get the selected register type
        let registerType = document.querySelector('input[name="registerType"]:checked').value;
        
        // Redirect based on the selected account type
        if (registerType === "oldLocation") {
            window.location.href = "/register_comp"; // Redirect to institution registration page
        } else if (registerType === "newLocation") {
            window.location.href = "/register_user"; // Redirect to individual registration page
        }
    });
})