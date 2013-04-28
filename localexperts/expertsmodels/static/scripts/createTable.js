function sub(id){
var parsedJson = [{user_id: "194889", 
			user_location: "Texas", 
			user_name:"hbarthwal", 
			profile_image_url:"https://si0.twimg.com/sticky/default_profile_images/default_profile_0_bigger.png", 
			user_description:"I m hcajdbva."},
			{user_id: "19894784", 
			user_location: "1", 
			user_name:"preeti", 
			profile_image_url:"https://si0.twimg.com/sticky/default_profile_images/default_profile_0_bigger.png", 
			user_description:"I m hcsjdh"},
			{user_id: "19478472", 
			user_location: "2", 
			user_name:"xxxxx", 
			profile_image_url:"https://si0.twimg.com/sticky/default_profile_images/default_profile_0_bigger.png", 
			user_description:"I m adhaiphf"},
			{user_id: "1924792", 
			user_location: "3", 
			user_name:"yyyy", 
			profile_image_url:"https://si0.twimg.com/sticky/default_profile_images/default_profile_0_bigger.png", 
			user_description:"I m fffhwie"},
			{user_id: "192438787", 
			user_location: "4", 
			user_name:"bjdb", 
			profile_image_url:"https://si0.twimg.com/sticky/default_profile_images/default_profile_0_bigger.png", 
			user_description:"I m hcfioshf"}
			];
		var div = document.getElementById(id);
		while(div.firstChild){
				div.removeChild(div.firstChild); // to make sure only one table exists if clicked on search multiple times. 
			}
			
		createTableFromJson(parsedJson,id);
}

function createTableFromJson(parsedJson,id){
	/*<div class="mrg">
		<div id="imgdiv" class="flt">
			<img src="https://si0.twimg.com/sticky/default_profile_images/default_profile_0_bigger.png" width="100px" height="100px"/> 
		</div>
		<div class="flt descntr">
		<div>UserName</div>
		<div class="desc">Description of user lots of text :P :P :P :P :P </div>
		<div>Location</div>
		</div>
	</div>
	<p class="clr"></p> */
	console.log("json objects number - "+parsedJson.length);
	
	var div = document.getElementById(id);
	div.setAttribute("class","res");
	
	
	for (i = 0; i < parsedJson.length; i++)
        {
		divCntr = document.createElement("div");
		divCntr.setAttribute('class','mrg');
	
		
		divImg = document.createElement("div");
		divImg.setAttribute('class','flt'); // applying css for float left
		pp = document.createElement("img");  //parsedJson[i].profile_image_url - <img src="img url" width="80px" height="80px"></img>
		pp.setAttribute('src',parsedJson[i].profile_image_url); 
		pp.setAttribute('width',"100px");
		pp.setAttribute('height',"100px");
		divImg.appendChild(pp);
			
		divDescCntr = document.createElement("div");
		divDescCntr.setAttribute('class','flt descntr');
		
		divUserName = document.createElement("div");
		divUserName.appendChild(document.createTextNode("User Name: "+parsedJson[i].user_name));
		
		
		divDesc = document.createElement("div");
		divDesc.setAttribute('class','desc');
		divDesc.appendChild(document.createTextNode("Description: "+parsedJson[i].user_description));
		
		divLoc = document.createElement("div");
		divLoc.appendChild(document.createTextNode("Location: "+parsedJson[i].user_location));
		
		divDescCntr.appendChild(divUserName);
		divDescCntr.appendChild(divLoc);
		divDescCntr.appendChild(divDesc);
			
		divCntr.appendChild(divImg);
		divCntr.appendChild(divDescCntr);
		
		div.appendChild(divCntr);
		
		}	
}
