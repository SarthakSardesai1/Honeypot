document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);

        // Send login attempt to server
        fetch('/wp-login.php', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);
            return response.text();
        })
        .then(text => {
            console.log('Response text:', text);
            try {
                return JSON.parse(text);
            } catch (error) {
                console.error('Error parsing JSON:', error);
                throw new Error('The server response was not valid JSON');
            }
        })
        .then(data => {
            console.log('Parsed data:', data);
            if (data.status === 'success') {
                window.location.href = data.redirect;
            } else {
                errorMessage.textContent = data.message;
                errorMessage.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = `An error occurred: ${error.message}. Please try again.`;
            errorMessage.style.display = 'block';
        });
    });
});
