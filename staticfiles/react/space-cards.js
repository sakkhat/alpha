class SpaceCards extends React.Component {
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

	getSpaceURL(name){
		return '/space/'+name.toString()+'/';
	}


	fetchData(){
		fetch(this.state.url+'&page='+this.state.page)
		.then(response => response.json())
		.then(data =>{
			if(data.length != 0){
				const results = data.map((item) => 
					<div className="col-auto mb-3">
						<div className="card space-box">
							<h5 className="card-title bg-dark text-white list-group-item">{item.space}</h5>
							<div className="card-body">
								<p className="card-text float-left mr-2 lead">Posts: {item.total_post}</p>
								<p className="card-text lead">Rating: {item.rating}</p>
								<a href={this.getSpaceURL(item.space)} class="card-link btn btn-success">Visit</a>
							</div>
						</div>
					</div>
				);

				this.setState({
					list :  this.state.list.concat(results),
					loaded : true,
					page : this.state.page+1
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
				<div>
					<div className="container-fluid">
						<div className="row justify-content-center">
							{this.state.list}
						</div>
					</div>
					<div className="d-flex justify-content-center">
	                    <div className="spinner-grow text-muted"></div>
	                    <div className="spinner-grow text-primary"></div>
	                    <div className="spinner-grow text-success"></div>
	                    <div className="spinner-grow text-info"></div>
	                    <div className="spinner-grow text-warning"></div>
	                    <div className="spinner-grow text-danger"></div>
	                    <div className="spinner-grow text-secondary"></div>
	                    <div className="spinner-grow text-dark"></div>
	                    <div className="spinner-grow text-light"></div>
	                </div>
				</div>
			);
		}
		else if(! this.state.hasMore){
			return(
				<div className="container-fluid">
					<div className="row justify-content-center">
						{this.state.list}
					</div>
				</div>
			);
		}

		return(

			<div>
				<div className="container-fluid">
					<div className="row justify-content-center">
						{this.state.list}
					</div>
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
const element = (<SpaceCards url={getContext(dom, 'url')}/>);
ReactDOM.render(element, dom);