class NotificationList extends React.Component {

    constructor(props){
        super(props);

        this.state = {
            'loaded' : false,
            'data' : new Array(),
            'url' : props.url,
            'token' : props.token
        };
    }

    getSeenClassName(seen){
        if(seen){
            return 'fa fa-check';
        }
        return 'em em-new';
    }

    getTimeDate(timeDate){
        return new Date(timeDate).toLocaleString();
    }

    getLabel(label){
        switch(label){
            case 'Ad': return 'Advertise';
            case 'Sc': return 'Security';
            case 'Of': return 'Offer';
            default: return 'General';
        }
    };

    getRouteURL(action, uid, seen){
        if(seen){
            return action;
        }
        return '/notification/'+uid.toString()+'/action/?token='+this.state.token+'&action='+action
    }

    fetchData(url){
        fetch(url)
        .then(response => response.json())
        .then(data =>{
            if(data.length > 0){
                const results = data.map((item) =>
                    <div className="list-group-item">
                        <div>
                            <h6 className="btn btn-info btn-sm disabled mt-0 mb-0">{this.getLabel(item.label)}</h6>
                            <h6 className="float-right">{this.getTimeDate(item.time_date)}</h6>
                        </div>
                        <h6 className="list-group-item list-group-item-secondary">
                            {item.title} <i className={this.getSeenClassName(item.seen)} ></i>
                        </h6>
                        <a href={this.getRouteURL(item.action, item.uid, item.seen)} className="list-group-item list-group-item-action">
                            {item.message}
                        </a>
                    </div>  
                );

                this.setState({
                    loaded : true,
                    data : results
                });
            }
            else {
                this.setState({
                    loaded : true
                });
            }
        });
    }

    componentDidMount(){
        this.fetchData(this.state.url);
    }

    
    render(){

        if(this.state.loaded){
            if(this.state.data.length == 0){
                return (
                    <h6 align="center">Empty</h6>
                );    
            }
            else{
                return (
                    this.state.data
                );
            }
        }
        else{
            return(
                <h6 align="center">Loading...</h6>
            );
        }
    }
}



function getContext(dom, key){
    return dom.getAttribute(key).toString();
}

const dom = document.getElementById('notification-container');
const block = document.getElementById(getContext(dom, 'renderID'));

const element = (<NotificationList url={getContext(dom, 'url')} token={getContext(dom, 'token')} />);

ReactDOM.render(element, block);