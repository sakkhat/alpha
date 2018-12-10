
function showLogin(){
	var divLogin = document.getElementById("sign_in_block");
	var divRegis = document.getElementById("sign_up_block");

	divRegis.style.display = 'none';
	divLogin.style.display = 'block';
}

function showRegister(){
	var divLogin = document.getElementById("sign_in_block");
	var divRegis = document.getElementById("sign_up_block");

	divRegis.style.display = 'block';
	divLogin.style.display = 'none';
}