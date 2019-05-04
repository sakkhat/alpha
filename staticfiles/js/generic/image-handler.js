var previewImage = function(event, view_id, activator) {
	$(view_id).css('opacity', '0.2');
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function(){
    	$(view_id).attr('src', reader.result);
    	$(view_id).css('opacity', '1.0');
    	$(activator).css('display', 'block');
    };
    reader.readAsDataURL(input.files[0]);
};

var upload = function(uploader, form_id){

    var button = $("#"+uploader)
    button.html('Uploading <span class="spinner-border spinner-border-sm"></span>');
    button.attr('disabled', true);

	var form = document.getElementById(form_id);
    var formData = new FormData(form);

    var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        const url = '/api/media/update/';
        fetch(url, {
            method: 'PUT',
            body : formData,
            headers: {
                "X-CSRFToken": $crf_token,
                Accept: 'application/json, text/plain, */*',
            },
        })
        .then(response => response.json())
        .then(data =>{
            console.log(data);
            button.css('display', 'none');
        })
        .catch((error) => {
            console.log(data);
            button.css('display', 'none');
        });
}	