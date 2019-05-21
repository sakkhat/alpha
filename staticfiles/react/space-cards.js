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
		return '/space/'+name+'/';
	}


	fetchData(){
		fetch(this.state.url+'&page='+this.state.page)
		.then(response => response.json())
		.then(data =>{
			if(data.length != 0){
				const results = data.map((item) => 
					<div className="col-auto mb-3">
						<div className="card text-white position-relative">
							<img src={item.logo} className="card-img"/>
					        <div className="card-img-overlay">
					        	<div className="d-flex justify-content-center">
					            	<img className="space-logo" src={item.logo}/>
						        </div>
						        <h6 className="space-name">@{item.space}</h6>
						        <div>
						            <h6 className="activity">Favorite <span className="activity-counter">{item.total_favorite}</span></h6>
						            <h6 className="activity">Pinned <span className="activity-counter">{item.total_pinned}</span></h6>
						            <h6 className="activity">Posts <span className="activity-counter">{item.total_post}</span></h6>
						            <h6 className="activity">Rating <span className="activity-counter">{item.rating}</span></h6>
						        </div>
						        <div className="space-link">
						        	<a href={this.getSpaceURL(item.space)} className="btn btn-light btn-sm">Visit</a>
						        </div>
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
	                    <div className="col-md-6">
							<button className="btn btn-block btn-outline-secondary mb-5 disabled">Loading...</button>
						</div>
	                </div>
				</div>
			);
		}
		else if(! this.state.hasMore){
			return(
				<div>
					<div className="container-fluid">
						<div className="row justify-content-center">
							{this.state.list}
						</div>
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