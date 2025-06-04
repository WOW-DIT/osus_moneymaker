document.addEventListener("DOMContentLoaded", function () {
  // Function to be executed when the button is clicked
  function handleClick(event) {
    //event.preventDefault();
    $.ajax({ 
      url: 'http://192.168.1.84/api/method/moneymaker.applicant.applyStudent', 
      type: 'POST', 
      headers: { 
        "Content-Type": "application/json"   
      }, 
      data: JSON.stringify({ 
        "gender" : "fwdfdfwfw"  // Replace with the actual gender value you want to send
      }), 
      success: function(response) { 
          console.log("Fetching...");
          console.log(response.message) 
      }, 
      error: function(error) { 
        console.log(error); 
      } 
    }) 
  }
  // Get the button element
  // Add the click event listener
  document.getElementById('form1').addEventListener('submit', function(evt){
    evt.preventDefault();
    handleClick();
  })
});