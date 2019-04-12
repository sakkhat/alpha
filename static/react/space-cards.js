class SpaceCards extends React.Component {
	constructor(props){
		super(props);

		this.state = {
			'url' : props.url,
			'loaded' : false,
			'list' : null
		};
	}
	getSpaceURL(name){
		return '/space/'+name.toString()+'/';
	}

	componentDidMount(){
		fetch(this.state.url)
		.then(response => response.json())
		.then(data =>{
			const results = data.map((item) => 
				<div className="col-md-3 mb-3">
					<div className="card">
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
				list : results,
				loaded : true
			});
		});
	}

	render(){
		if(! this.state.loaded){
			return(
				 <div>
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
			);
		}

		return this.state.list;
	}
}

function getURL(dom){
	return dom.getAttribute('url').toString();
}


const dom = document.getElementById('cards-container');
const element = (<SpaceCards url={getURL(dom)}/>);
ReactDOM.render(element, dom);