
$('#domain').on('input',replaceSpaces);

$('#domain').focusout(checkDomain);

$('#addMajor').click(addMajor);
$('#addLanguage').click(addLanguage);
$('#addSkill').click(addSkill);
$('#addSection').click(addSection);

$('#submit').click(submitForm);

//variables
var csrf_token = $.cookie('csrftoken');
var domainApproved = false;

var numMajors = 1;
var numLanguages = 1;
var numSkills = 1;
var numSection = 1;

//easier to manage
var majors = [];
var languages = [];
var skills = [];
var sections = [];

majors.push( $('#major1') );
languages.push( $('#language1') );
skills.push( $('#skill1') );


/**
 * adds Section
 */
function addSection(){
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
  title.val("");

  content.attr("id","sectionContent"+numSection);
  content.val("");

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
 * Adds text box for skills
 */
function addSkill(){
  numSkills = addBox("skill",skills,numSkills);
}

/**
 * Adds text box for language
 */
function addLanguage(){
  numLanguages = addBox("language",languages,numLanguages);
}

/**
 * Adds text box for major
 */
function addMajor(){
  numMajors = addBox("major",majors,numMajors);
}

/**
 * Adds additional text box and corresponding delete button
 * @param string- id name to reference
 * @param array- array of textbox elements
 * @param counter- number of textboxes
 * @return new value of counter
 */
function addBox(string,array,counter){
  ++counter;

  var div = $("#container_" + string + 1).clone();

  var id = "container_" + string + counter;
  div.attr("id", id);

  var textBox = div.find("#" + string + "1");
  textBox.attr('id',id);
  textBox.val("");

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
 * Stringifies the Section into an array
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
 * Submit button is clicked
 */
function submitForm(){
  console.log("submit");
  //TODO:do some error checking
  //backend should expect errors in data anyways tho

  var skillVal = getValues(skills);
  var languageVal = getValues(languages);
  var majorVal = getValues(majors);

  var sectionVal = getSectionValues();


  //data to send to server, submit 1 signifies that this ajax is a form submission
  var data = { submit : '1' , skills : skillVal, languages : languageVal,
    majors : majorVal, sections : sectionVal, domain : $('#domain').val(), 
    title : $('#title').val(), author : $('#author').val(),
    description : $('#description').val(), name : $('#name').val(),
    education : $('#education').val(), gpa : $('#gpa').val(),
    experience : $('#experience').val(), summary : $('#summary').val() };

  sendAjax("/sites/createSite/",data,submitResponse);
} 

/*
 * response from server after form is submitted
 */
function submitResponse(json){
  //TODO: display error messages if necessary
  if( json.redirect){
    window.location.href = json.redirect;
  }
  else if(json.error){
    $('html,body').animate({ scrollTop: 0},'fast');
    //TODO: display error messages
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
    console.log(json);
  }
  else{
    console.log("undefined submitResponse");
  }
}

/**
 * Sends data to url through ajax adds csrf token to data
 * @param url - String to url
 * @param data - data to send to the server
 * @param sucessCall - function to call after successful connection
 * @param errorCall - function to call if ajax fails
 */
function sendAjax(url,data, successCall){
  data['csrfmiddlewaretoken'] = csrf_token;
  $.ajax({url: url, type : "POST", data: data, success : successCall, error : responseFailure });
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

/**
 * replaces spaces in domain text box with underscores
 */
function replaceSpaces(){
  var domain = $('#domain').val();
  domain = domain.replace(" ","_");
  $('#domain').val(domain);
}
