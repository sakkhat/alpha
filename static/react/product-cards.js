class ProductCards extends React.Component {

	constructor(props){
		super(props);

		this.state = {
			'url' : props.url,
			'loaded' : false,
			'list' : null
		};
	}

	getProductURL(uid){
		return '/space/product/'+uid.toString()+'/';
	}

	componentDidMount(){

		fetch(this.state.url)
		.then(response => response.json())
		.then(data =>{
			const results = data.map((item) => 
				<div className="col-auto mb-3">
                    <figure className="card-container fixed-card">
                        <img src={item.logo_url}/>
                        <figcaption>
                            <h5 className="title">{item.title}</h5>
                            <h6>{item.price}</h6>
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
const element = (<ProductCards url={getURL(dom)}/>);
ReactDOM.render(element, dom);