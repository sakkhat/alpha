
class ProductReact extends React.Component {

    constructor(props){
        super(props);

        if(props.obj.auth){

            var reactCodeDic = {'None':'N', 'Good':'G', 'Bad':'B', 'Fake':'F'};
            var reactStateDic ={'N':true, 'G':false,'B':false,'F':false};

            this.state = {
                'good' : 0,
                'bad' : 0,
                'fake' : 0,

                'goodClass' : 'btn btn-sm btn-outline-success',
                'badClass' : 'btn btn-sm btn-outline-warning',
                'fakeClass' : 'btn btn-sm btn-outline-danger',

                'currentReact' : 'N',
                'url' : '/api/product/'+props.obj.uid+'/activity/react/',
                'auth' : true,

                'reactCodeDic' : reactCodeDic,
                'reactStateDic' : reactStateDic
            };
        }
        else {

            this.state = {
                'good' : 0,
                'bad' : 0,
                'fake' : 0,

                'goodClass' :'btn btn-sm btn-outline-success disabled',
                'badClass' : 'btn btn-sm btn-outline-warning disabled',
                'fakeClass' : 'btn btn-sm btn-outline-danger disabled',
                'auth' : false,

                'currentReact' : 'N',
                'url' : '/api/product/'+props.obj.uid+'/activity/react/',
            };
        }
        

        this.handleGood = this.handleGood.bind(this);
        this.handleBad = this.handleBad.bind(this);
        this.handleFake = this.handleFake.bind(this);
    }

    componentDidMount(){

        if(this.props.has_react){

            const _currentReact = this.props.currentReact;
            var reactStateDic = this.state.reactStateDic;
            reactStateDic[_currentReact] = true;
            reactStateDic[this.state.reactCodeDic['None']] = false;

            this.setState({
                currentReact : _currentReact,
                reactStateDic : reactStateDic
            });
            this.updateColor(reactStateDic);

        }
        

        this.updateReacts();
    }

    getGoodColor(state){
        return (state ? 'btn btn-sm btn-success' : 'btn btn-sm btn-outline-success');
    }

    getBadColor(state){
        return (state ? 'btn btn-sm btn-warning' : 'btn btn-sm btn-outline-warning');
    }

    getFakeColor(state){
        return (state ? 'btn btn-sm btn-danger' : 'btn btn-sm btn-outline-danger');
    }

    updateColor(reactStateDic){

        this.setState({
            goodClass : this.getGoodColor(reactStateDic[this.state.reactCodeDic['Good']]),
            badClass : this.getBadColor(reactStateDic[this.state.reactCodeDic['Bad']]),
            fakeClass : this.getFakeColor(reactStateDic[this.state.reactCodeDic['Fake']])
        });
    }

    updateReacts(){
        fetch(this.state.url+'?format=json')
        .then(response => response.json())
        .then(data => {

            const obj = data;
            this.setState({
                good : data.react_good,
                bad : data.react_bad,
                fake : data.react_fake
            });
        });
    }


    handle(name){

        var reactCodeDic = this.state.reactCodeDic;
        var reactStateDic = this.state.reactStateDic;

        var keys = Object.keys(reactCodeDic);


        if(reactStateDic[reactCodeDic[name]]){
            for(var item=0; item<keys.length; item++){
                reactStateDic[reactCodeDic[keys[item]]] = false;
            }

            fetch(this.state.url+'?react=None&format=json')
            .then(response => response.json())
            .then(date =>{
                this.setState({
                    currentReact : reactCodeDic['None'],
                    reactStateDic : reactStateDic,
                    reactCodeDic : reactCodeDic,
                });
                this.updateReacts();
                this.updateColor(reactStateDic);
            });
        }
        else{
            for(var item=0; item<keys.length; item++){
                reactStateDic[reactCodeDic[keys[item]]] = false;
            }
            reactStateDic[reactCodeDic[name]] = true


            fetch(this.state.url+'?react='+name+'&format=json')
            .then(response => response.json())
            .then(date =>{
                this.setState({
                    currentReact : reactCodeDic[name],
                    reactStateDic : reactStateDic,
                    reactCodeDic : reactCodeDic
                });
                this.updateReacts();
                this.updateColor(reactStateDic);
            });
        }
    }

    handleGood(){

        {% if request.user == product.space.owner%}
        return;
        {% endif %}

        if(this.state.auth == false){
            return;
        }
        this.handle('Good');
    }

    handleBad(){

        {% if request.user == product.space.owner%}
        return;
        {% endif %}

        if(this.state.auth == false){
            return;
        }
        this.handle('Bad');
    }

    handleFake(){
        {% if request.user == product.space.owner%}
        return;
        {% endif %}

        if(this.state.auth == false){
            return;
        }
        this.handle('Fake');
    }

    render(){
        return (
                        
            <div className="bt-config">
                <button className={this.state.goodClass} onClick={this.handleGood}>
                    <i className="em em---1"></i><span className="badge badge-light">{this.state.good} Good</span>
                </button>
                <button className={this.state.badClass} onClick={this.handleBad}>
                    <i className="em em--1"></i><span className="badge badge-light">{this.state.bad} Bad</span>
                </button>
                <button className={this.state.fakeClass} onClick={this.handleFake}>
                    <i className="em em-face_with_symbols_on_mouth"></i><span className="badge badge-light">{this.state.fake} Fake</span>
                </button>
            </div>
        );
    }
}

class ProductPin extends React.Component{
    constructor(props){
        super(props);
        
        if(props.obj.has_pin){
            this.state = {
                'btClassName' : 'btn btn-sm btn-dark',
                'pinned' : true,
                'text' : 'remove',
                'url' : '/api/product/'+'{{product.uid}}'+'/activity/pin/'
            };
        }

        else {

            this.state = {
                'btClassName' : 'btn btn-sm btn-outline-dark',
                'pinned' : false,
                'text' : 'add',
                'url' : '/api/product/'+'{{product.uid}}'+'/activity/pin/'
            };
        }

        this.handlePin = this.handlePin.bind(this);
    }

    handlePin(){
        if(this.state.pinned){
            this.setState({
                btClassName : 'btn btn-sm btn-outline-dark',
                pinned : false,
                text : 'add'
            });
            fetch(this.state.url+'?req=remove&format=json')
            .then(response => response.json())
            .then(data => {
            });
        }
        else{
            this.setState({
                btClassName : 'btn btn-sm btn-dark',
                pinned : true,
                text : 'remove'
            });
            fetch(this.state.url+'?req=add&format=json')
            .then(response => response.json())
            .then(data => {
            });
        }
        return;
    }

    render(){
        return(
            <button className={this.state.btClassName} onClick={this.handlePin}>
                <i className="em em-pushpin"></i><span className="badge badge-light">{this.state.text}</span>
            </button>
        )
    }
}

const element = (
    <div className="row">
        <div className="col-sm-9">
            <ProductReact/>
        </div>
        {% if request.user.is_authenticated %}
            {% if not product.space.owner == request.user %}
                <div className="col-sm-3 bt-config">
                    <ProductPin/>    
                </div>
            {% endif %}
        {% endif %}
    </div>
        
);



ReactDOM.render(element, document.getElementById('product-react-pin'));