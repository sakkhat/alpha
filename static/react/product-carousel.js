class ProductItemCard extends React.Component {

	constructor(props){
		super(props);

		this.state = {
			'key' : props.obj.key,
			'title' : props.obj.title,
			'price' : props.obj.price,
			'logo_url' : props.obj.logo_url,
			'good' : props.obj.react_good,
			'bad' : props.obj.react_bad,
			'fake' : props.obj.react_fake,

			'product_url' : '/space/product/',
			'react_url' : 'space/product/react/?',	
		};

		this.handleGoodReact = this.handleGoodReact.bind(this);
		this.handleBadReact = this.handleBadReact.bind(this);
		this.handleFakeReact = this.handleFakeReact.bind(this);

	}

	render() {
		return (
			<div className="card bg-light" id="product-card">
                <a href={this.state.product_url}>
                    <img src={this.state.logo_url} />
                </a>
                <div className="card-body">
                    <center>
                       <a href={this.state.product_url}><h5>{this.state.title}</h5></a>
                       <h6 className="d-inline-block">{this.state.price}</h6>            
                    </center>
                    <center>
                        <button className="btn btn-success disable" data-toggle="tooltip" title="Good">
                            <i className="em em---1"></i><span class="badge badge-light">{this.state.good}</span>
                        </button>
                        <button className="btn btn-warning disable" data-toggle="tooltip" title="Bad">
                            <i className="em em--1"></i><span class="badge badge-light">{this.state.bad}</span>
                        </button>
                        <button className="btn btn-danger disable" data-toggle="tooltip" title="Fake">
                            <i className="em em-face_with_symbols_on_mouth"></i><span class="badge badge-light">{this.state.fake}</span>
                        </button>
                    </center>
                </div>
            </div>
		);
	}
}


class ProductList extends React.Component {

	constructor(props){
		super(props);
		this.state = {
			'list' : null,
			'loaded' : false,
			'url' : '/space/product/list/?format=json'
		}
	}

	componentDidMount(){
		const url = this.state.url;
		fetch(url)
		.then(response => response.json())
		.then(data => {
			// console.log(data.results);
			const results = data.results;
			const list = results.map((i) => <ProductItemCard obj={i}/>);
			this.setState({
				list : list,
				loaded : true
			});
		});
	}

	render() {
		if(this.state.loaded){
			return(
				<div>
					<h5>Data loaded</h5>
					{this.state.list}
				</div>
			);
		}
		return (
			<h5>loading....</h5>
		);
	}
}

const element = (
	<ProductList/>
);

ReactDOM.render(element, document.getElementById('product-carousel'));