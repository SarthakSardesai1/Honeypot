document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginform');
    const submitButton = document.getElementById('wp-submit');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('user_login').value;
        const password = document.getElementById('user_pass').value;

        if (username && password) {
            alert('Login attempt with:\nUsername: ' + username + '\nPassword: ' + password);
            // Here you would typically send these credentials to a server for authentication
        } else {
            alert('Please enter both username and password.');
        }
    });
});