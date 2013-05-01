function createTableFromJson(parsedJson,id){
	console.log("json objects number - "+ parsedJson.length);
	
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
		anchorUserName = document.createElement("a");
		anchorUserName.setAttribute("href","http://www.twitter.com/@"+parsedJson[i].user_name);
		anchorUserName.setAttribute("target","_blank");
		anchorUserName.appendChild(document.createTextNode(parsedJson[i].user_name));
		divUserName.appendChild(anchorUserName);
		
		divDesc = document.createElement("div");
		divDesc.setAttribute('class','desc');
		txtDesc = document.createTextNode(parsedJson[i].user_description)
		divDesc.appendChild(txtDesc);
		
		divLoc = document.createElement("div");
		divLoc.appendChild(document.createTextNode("Location: "+ parsedJson[i].user_location));
		
		divDescCntr.appendChild(divUserName);
		divDescCntr.appendChild(divLoc);
		divDescCntr.appendChild(divDesc);
			
		divCntr.appendChild(divImg);
		divCntr.appendChild(divDescCntr);
		
		div.appendChild(divCntr);
		}	
}

function sub(id, query, location){
	var requestString = "getExpertSearchResults?query=" + query + "&userlocation=" + location;
	$.get(requestString ,function(jsonData,status) {
		parsedJson = JSON.parse(jsonData);
		var div = document.getElementById(id);
		while(div.firstChild){
				div.removeChild(div.firstChild); // to make sure only one table exists if clicked on search multiple times. 
			}
			
		createTableFromJson(parsedJson,id);
	});
	
}