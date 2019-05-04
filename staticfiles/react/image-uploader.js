class ImageUploader extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			'token' : props.token,
			'space' : props.space,
			'current' : props.current,
			'imageSrc' : props.imageSrc,
			'isChanged' : false,
			'isUploading' : false
		};

		this.preview = this.preview.bind(this);
		this.update = this.update.bind(this);
	}

	preview(event){
		var input = event.target;
	    var reader = new FileReader();
	    reader.onloadend = function(e){

			this.setState({
				'imageSrc' : reader.result,
				'isChanged' : true
			});

	    }.bind(this);
	    reader.readAsDataURL(input.files[0]);
	}

	update(){

		if(! this.state.isChanged){
			alert('no image picked');
			return;
		}

		this.setState({
            isUploading : true
        });

		var formData = new FormData();
        formData.append('image', this.state.imageSrc);

        var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        const url = '';
        fetch(url, {
            method: 'PUT',
            body : formData,
            headers: {
	            "X-CSRFToken": $crf_token,
	            Accept: 'application/json, text/plain, */*',
	        },
        })
        .then(response => response.json())
        .then(data =>{
            this.setState({
                isUploading : false
            });
        })
        .catch((error) => {
	  		this.setState({
                isUploading : false
            });
		});
	}

	render(){
		if(this.state.isUploading){
			return (
				<div className="image-container">
			        <img src={this.state.imageSrc}/>
			        <label className="btn btn-outline-secondary" for="picker">Choose new image</label>
			        <input type="file" name="image" id="picker" onChange={this.preview} />
			        <button className="btn btn-success disabled">
			        	<span className="spinner-border spinner-border-sm"></span>Uploading...
			        </button>
			    </div>
			);
		}
		return (
			<div className="image-container">
		        <img src={this.state.imageSrc}/>
		        <label className="btn btn-outline-secondary" for="picker">Choose new image</label>
		        <input type="file" name="image" id="picker" onChange={this.preview} />
		        <button className="btn btn-outline-success" onClick={this.update}>Update Confirm</button>
		    </div>
		);
	}
}



class BannerUploader extends React.Component {
	constructor(props){
		super(props);
	}

	render(){
		return (
			<div>
				<ImageUploader/>
				<ImageUploader/>
				<ImageUploader/>
			</div>
		)
	}
}


const dom = document.getElementById('hello')
ReactDOM.render(<BannerUploader/>, dom);

// function getContext(dom, key){
// 	return dom.getAttribute(key);
// }

// function reactRender(containers){
// 	var index;
// 	for(var index in containers){
// 		const dom = document.getElementById(containers[index]);
// 		const element = (
// 			<ImageUploader 
// 				token={getContext(dom, "token")} 
// 				space={getContext(dom, "space")} 
// 				current={getContext(dom, "uid")} 
// 				imageSrc={getContext(dom, "imageSrc")} 
// 			/>
// 		)
// 	}
// }

// function getContainers(list){
// 	return list.split(" ");
// }
// const manager = document.getElementById('image-uploader-manager');
// const containers = getContainers(manager.getAttribute('blockList'));
// reactRender(containers);