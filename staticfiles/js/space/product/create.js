var openFile = function(event, view_id) {

    var input = event.target;
    var reader = new FileReader();
    reader.onload = function(){
        var dataURL = reader.result;
        var output = document.getElementById(view_id);
        output.src = dataURL;
    };
    reader.readAsDataURL(input.files[0]);
};
