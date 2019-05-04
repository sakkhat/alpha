function preview(event, view_id){
	console.log('called');
	
	var input = event.target;
    var reader = new FileReader();
    reader.onloadend = function(){
    	$(view_id).attr('src', reader.result);
    }
    reader.readAsDataURL(input.files[0]);
}