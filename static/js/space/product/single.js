function copyToClipboard(data){
	data.select();
	document.execCommand("copy");
}
$(document).ready(function(){
  $('[data-toggle="popover"]').popover(); 
});


// ajex request to send message to message box
