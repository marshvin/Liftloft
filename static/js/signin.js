document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signin-form');
    const responseMessageElement = document.getElementById('response-message');

    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);
        const email = formData.get('email');
        const password = formData.get('password');

        const response = await fetch('/signin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
        });

        const responseData = await response.json();

        if (response.ok) {
            responseMessageElement.textContent = responseData.message;
            setTimeout(function() {
                window.location.href = '/';
            }, 2000); // Redirect after 3 seconds 
        } else {
            responseMessageElement.textContent = 'Wrong Password or Email';
        }
    });
});
