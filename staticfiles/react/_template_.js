class ProductReact extends React.Component {

	constructor(props){

		this.setState = {
			'good' : 0,
			'bad', 0,
			'fake' : 0,

			'goodClass' : 'btn-outline-success',
			'badClass' : 'btn-outline-warning',
			'fakeClass' : 'btn-outline-danger',


		};

		super(props);
	}

	componentDidMount(){

	}
	
	render(){
		return (

		);
	}
}


const element = (
	<ProductReact/>
);

ReactDOM.render(element, document.getElementById('product-react'));