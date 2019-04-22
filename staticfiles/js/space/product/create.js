var openFile1 = function(event) {
    var input = event.target;

    var reader = new FileReader();
    reader.onload = function(){
        var dataURL = reader.result;
        var output = document.getElementById('img-view-1');
        output.src = dataURL;
    };
    reader.readAsDataURL(input.files[0]);
};
var openFile2 = function(event) {
    var input = event.target;

    var reader = new FileReader();
    reader.onload = function(){
        var dataURL = reader.result;
        var output = document.getElementById('img-view-2');
        output.src = dataURL;
    };
    reader.readAsDataURL(input.files[0]);
};
var openFile3 = function(event) {
    var input = event.target;

    var reader = new FileReader();
    reader.onload = function(){
        var dataURL = reader.result;
        var output = document.getElementById('img-view-3');
        output.src = dataURL;
    };
    reader.readAsDataURL(input.files[0]);
};