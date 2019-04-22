$('.fade-slider').slick({
	slidesToShow: 1,
	slidesToScroll: 1,
	arrows: false,
	fade: true,
	asNavFor: '.category-slider',
});

$('.category-slider').slick({
	asNavFor: '.fade-slider',
	focusOnSelect: true,

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

