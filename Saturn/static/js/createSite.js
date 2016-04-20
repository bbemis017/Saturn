$('#domain').on('input',replaceSpaces);
$('#addSection').click(addSection);
$('#domain').focusout(checkDomain);

//variables
var csrf_token = $.cookie('csrftoken');
var domainApproved = false;
var numSection = 1;
var sections = [];

/**
 * Adds additional text box and corresponding delete button
 * @param string- id name to reference
 * @param array- array of textbox elements
 * @param counter- number of textboxes
 * @param value- optional parameter, value to insert into box
 * @return new value of counter
 */
function addBox(string,array,counter,value){
  if( value === undefined ){
    value = "";
  }
  ++counter;

  var div = $("#container_" + string + 1).clone();

  var id = "container_" + string + counter;
  div.attr("id", id);

  var textBox = div.find("#" + string + "1");
  textBox.attr('id',id);
  textBox.val(value);

  array.push( textBox );

  var dId = "d" + string + counter;

  var del = createDelete(dId);
  var delDiv = div.find("#" + string + "Del");
  delDiv.append(del);

  $("#" + string).append(div);

  $("#" + dId).click(function(){
    var d = this.id.substr(1,this.id.length);
    var index = array.indexOf( textBox );
    array.splice(index,1);
    $("#container_" + d).remove();
    $("#" + d).remove();
    $("#" + this.id).remove();
  });

  return counter;
}

/**
 * Creates a delete button with id
 */
function createDelete(id){
  var btn = document.createElement("button");
  btn.setAttribute("id",id);
  btn.setAttribute("type","button");
  btn.setAttribute("class","btn btn-danger btn-sm");
  btn.innerHTML = "Delete";
  return btn;
}

/**
 * creates new text box with id and name equal to id
 */
function createTextBox(id){
  var textBox = document.createElement("input");
  textBox.setAttribute("id",id);
  textBox.setAttribute("name",id);
  textBox.setAttribute("type","text");
  textBox.setAttribute("class","form-control");
  return textBox;
}

/**
 * Takes an array of html elements and returns a
 * stringified version of the values in those elements
 */
function getValues(elementArray){
  var newArray = [];
  for(var i = 0; i < elementArray.length; i++){
    newArray.push( elementArray[i].val());
  }

  return JSON.stringify(newArray);
}

/**
 * Takes a string and converts it into an array, adds text boxes and
 * inserts values back into new text boxes
 * @param string - this is the string that contains an array
 * @param id - this is the main id that we are targeting
 * @param elementArray - this is the array that stores the corresponding text boxes
 * @param counter - this is the counter for the number of boxes that exist
 */
function setInitialValues(string,id,elementArray,counter){
  if ( string === undefined )
    return counter;
  var array = JSON.parse( string );
  for( var i = 0; i < array.length; i++){
    if( i == 0){
     $("#" + id + "1").val( array[i] ); 
    }
    else
      counter = addBox(id,elementArray,counter,array[i]);
  }

  return counter;
}

/**
 * Sends data to url through ajax adds csrf token to data
 * Calls responseFailure on a failed connection
 * @param url - String to url
 * @param data - data to send to the server
 * @param sucessCall - function to call after successful connection
 */
function sendAjax(url,data, successCall){
  data['csrfmiddlewaretoken'] = csrf_token;
  $.ajax({url: url, type : "POST", data: data, success : successCall, error : responseFailure });
}

/**
 * adds subdomain and Basic site information to the data
 * Then calls sendAjax to send information to the server
 * Calls responseFailure on a failed connection
 * @param url - String to url
 * @param data - data to send to the server
 * @param successCall - function to call after successfull connection
 */
function submit(url,data,successCall){
  data['submit'] = 1;
  data['domain'] = $('#domain').val();
  data['title'] = $('#title').val();
  data['author'] = $('#author').val();
  data['description'] = $('#description').val();
  data['sections'] = getSectionValues();
  sendAjax(url,data,successCall);
}

/**
 * send domain that the user entered to the backend
 */
function checkDomain(){
  var domain = $('#domain').val()
  var data = {domain_check : '1', domain_json : domain};
  sendAjax("/sites/createSite/",data,domainResponse);
}

/**
 * called when backend sends json response
 */
function domainResponse(json){
  var div = $('#domainDiv');
  var icon = $('#domainIcon');
  if( json.exists == 1){
    div.addClass("has-error");
    div.removeClass("has-success");
    icon.addClass("glyphicon-remove");
    icon.removeClass("glyphicon-ok");
    $('#domainExists').show();
    domainApproved = false;
  }
  else{
    icon.addClass("glyphicon-ok");
    icon.removeClass("glyphicon-remove");
    div.addClass("has-success");
    div.removeClass("has-error");
    $('#domainExists').hide();
    domainApproved = true;
  }
}

/**
 * called when checkDomain() failed to send data
 * to backend
 */
function responseFailure(xhr,errmsg,err){
  console.log(xhr.status + ":" + xhr.responseText);
}

/*
 * response from server after form is submitted
 */
function submitResponse(json){
  //TODO: display error messages if necessary
  console.log(json);
  if( json.redirect){
    window.location.href = json.redirect;
  }
  else if(json.error_code){
    $('html,body').animate({ scrollTop: 0},'fast');
    //TODO: display error messages
    //title missing
    if( json.error_code == 3){
      $('#title_missing').show();
    }
    else{
      $('#title_missing').hide();
    }
    //domain missing
    if( json.error_code == 4)
      $('#domain_missing').show();
    else
      $('#domain_missing').hide();
    /*
    if(json.domain_missing){
      $('#domain_missing').show();
    }
    else{
      $('#domain_missing').hide();
    }
    if( json.title_missing){
      $('#title_missing').show();
    }
    else{
      $('#title_missing').hide();
    }
    */
    console.log(json);
  }
  else{
    console.log("undefined submitResponse this one");
    console.log(json);
  }
}

/**
 * replaces spaces in domain text box with underscores
 */
function replaceSpaces(){
  var domain = $('#domain').val();
  domain = domain.replace(" ","_");
  $('#domain').val(domain);
}

function addSection(){
  addSectionValues("","");
}

/**
 * adds Section
 * @param - titleValue optional parameter, value for title box
 * @param - contentValue optional parameter, value for content box
 */
function addSectionValues(titleValue,contentValue){
  console.log("title: " + titleValue);
  console.log("content: " + contentValue);

  var containerDiv = $('#container_section1');
  var dId = "dsection" + (numSection + 1);

  var newDiv = containerDiv.clone();//clone deep copy
  var prevId = "#section" + numSection;
  numSection++;


  //change id's and names
  newDiv.attr("id","container_section"+numSection);

  var title = newDiv.find("#sectionTitle1");
  var content = newDiv.find("#sectionContent1");

  title.attr("id","sectionTitle"+numSection);
  title.val(titleValue);

  content.attr("id","sectionContent"+numSection);
  content.val(contentValue);

  var del = createDelete(dId);
  var delDiv = newDiv.find("#sectionDel");
  delDiv.append(del);

  newDiv.show();

  $("#section").append(newDiv);
  newDiv = $("#container_section" + (numSection) );
  sections.push( newDiv );

  $("#" + dId).click(function(){
    var d = this.id.substr(1,this.id.length);
    var index = sections.indexOf( newDiv );
    sections.splice(index,1);
    $("#container_" + d).remove();
    $("#" + d).remove();
    $("#" + this.id).remove();
  });

}

/**
 * Stringify the Section into an array
 *   -even elements are the section title
 *   -odd elements are the content
 */
function getSectionValues(){
  var newArray = [];
  for(var i = 0; i < sections.length; i++){
    var title = sections[i].find("[name='title']");
    var content = sections[i].find("[name='content']");
    newArray.push( title.val() );
    newArray.push( content.val() );
  }
  return JSON.stringify(newArray);
}

/**
 * Accepts a string representing an array of data for the sections
 */
function setSectionValues(string){
  if( string === undefined)
    return;
  var array = JSON.parse( string );
  for( var i = 0; i < array.length; i+=2){ //incrementing by 2
    addSectionValues( array[i] , array[i+1] );
  }
}
