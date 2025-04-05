function signupRedirect() {
    window.location.href = "/signup";
}

function loginRedirect() {
    window.location.href = "/login";
}


let userType = '';
        let attempts = 0;
        

        function goToLogin(type) {
            document.getElementById('userTypePage').classList.add('hidden');
            document.getElementById('loginPage').classList.remove('hidden');

            userType = type;
            document.getElementById('userType').value = type;


            if (type === 'admin') {
                document.getElementById('adminFields').classList.remove('hidden');
                document.getElementById('patientFields').classList.add('hidden');
            } else {
                document.getElementById('adminFields').classList.add('hidden');
                document.getElementById('patientFields').classList.remove('hidden');
            }
        }


        function showHidePassword(inputId) {
            let input = document.getElementById(inputId);
            let btn = input.nextElementSibling;

            if (input.type == "password") {
                input.type = "text";
                btn.innerHTML = "Hide";
            } else {
                input.type = "password";
                btn.innerHTML = "Show";
            }
        }

        function validateForm() {

            const userType = document.getElementById('userType').value;

            if (userType === 'admin') {
                document.getElementById('username').value = document.getElementById('Adminusername').value;
                document.getElementById('password').value = document.getElementById('Adminpassword').value;
            } else if (userType === 'patient') {
                document.getElementById('username').value = document.getElementById('Patientusername').value;
                document.getElementById('password').value = document.getElementById('Patientpassword').value;
            }
            


            attempts++;
            if(attempts > 3) {
                alert("Too many login attempts. Please try again later.");
                return false;
            }


            return true;
        }

        window.onload = function() {
            let savedUser = localStorage.getItem('lastUserType');
            if(savedUser) {
                goToLogin(savedUser);
            }
        }