class ProductCards extends React.Component {

	constructor(props){
		super(props);

		this.state = {
			'url' : props.url,
			'loaded' : false,
			'list' : new Array(),
			'page' : 0,
			'hasMore' : true
		};

		this.loadMore = this.loadMore.bind(this);
	}

	getProductURL(uid){
		return '/space/product/'+uid.toString()+'/';
	}

	fetchData(){
		fetch(this.state.url+'&page='+this.state.page)
		.then(response => response.json())
		.then(data =>{
			if (data.length != 0) {
				const results = data.map((item) => 
					<div className="col-auto mb-3">
	                    <figure className="card-container fixed-card">
	                        <img src={item.logo_url}/>
	                        <figcaption>
	                            <h5 className="title">{item.title}</h5>
	                            <h6>{item.space}</h6>
	                            <h6>@{item.price} TK</h6>
	                            <div>
	                                <button className="react-btn">
	                                    <i className="em em---1"></i>
	                                    <span className="badge badge-success">{item.react_good}</span>
	                                </button>
	                                 <button className="react-btn">
	                                    <i className="em em--1"></i>
	                                    <span className="badge badge-warning">{item.react_bad}</span>
	                                </button>
	                                 <button className="react-btn">
	                                    <i className="em em-rage"></i>
	                                    <span className="badge badge-danger">{item.react_fake}</span>
	                                </button>
	                            </div>
	                        </figcaption>
	                        <a href={this.getProductURL(item.uid)}></a>
	                    </figure>
	                </div>
				);

				this.setState({
					list : this.state.list.concat(results),
					loaded : true,
					page : this.state.page + 1
				});
			}
			else{
				this.setState({
					loaded : true,
					hasMore : false
				});
			}
		});
	}

	loadMore(event){
		this.setState({
			loaded : false,
		});
		this.fetchData();
	}

	componentDidMount(){
		this.fetchData();
	}


	render(){
		if(! this.state.loaded){
			return(
				<div class="container-fluid">
					<div className="row justify-content-center"> 
						{this.state.list}
					</div>
					<div className="d-flex justify-content-center">
						<div className="col-md-6">
							<button className="btn btn-block btn-outline-secondary mb-5 disabled">Loading...</button>
						</div>
					</div>
				</div>
			);
		}
		else if(! this.state.hasMore){
			return(
				<div class="container-fluid">
					<div className="row justify-content-center"> 
						{this.state.list}
					</div>
					<div className="d-flex justify-content-center">
						<div className="col-md-6">
							<button className="btn btn-block btn-outline-secondary mb-5 disabled">No More</button>
						</div>
					</div>
				</div>
			);
		}
		return(
			<div class="container-fluid">
				<div className="row justify-content-center"> 
					{this.state.list}
				</div>
				<div className="d-flex justify-content-center">
					<div className="col-md-6">
						<button className="btn btn-block btn-outline-secondary mb-5" onClick={this.loadMore}>Load More</button>
					</div>
				</div>
			</div>
		);
	}
}


function getContext(dom, key){
	return dom.getAttribute(key).toString();
}

const dom = document.getElementById('cards-container');
const block = document.getElementById(getContext(dom, 'renderID'));

const element = (<ProductCards url={getContext(dom, 'url')}/>);

ReactDOM.render(element, block);