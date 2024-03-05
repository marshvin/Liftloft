document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");

    signupForm.addEventListener("submit", async function (event) {
      event.preventDefault();

      const formData = new FormData(signupForm);

      const response = await fetch("/signup", {
        method: "POST",
        body: formData,
      });

      const responseData = await response.json();
      const messageElement = document.getElementById("response-message");

      if (response.ok) {
        messageElement.textContent = responseData.message;
      } else {
        // Handle error messages here
        messageElement.textContent = responseData.message;
      }
    });
  });