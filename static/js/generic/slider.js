$(document).ready(function(){
	$('.product-slick-container').slick({
		dots: false,
		infinite: true,
		speed: 300,
		slidesToShow: 1,
		adaptiveHeight: true,
		autoplay:true,
		autoplaySpeed:1500,
		slidesToShow: 1,
		centerMode: true,
		variableWidth: true,
		arrows:true
	});
});