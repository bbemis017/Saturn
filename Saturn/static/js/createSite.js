
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
var numSection = 0;

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
  if( numSection == 0){
    sections.push( $('#section1') );
    sections[0].show();
    numSection++;
  }
  else{
    var newDiv = $('#section1').clone(true);//clone deep copy
    var prevId = "#section" + numSection;
    numSection++;


    //change id's and names
    newDiv.attr("id","section"+numSection);

    var title = newDiv.find("#sectionTitle1");
    var content = newDiv.find("#sectionContent1");

    title.attr("id","sectionTitle"+numSection);
    title.attr("name","sectionTitle"+numSection);

    content.attr("id","sectionContent"+numSection);
    content.attr("name","sectionContent"+numSection);

    $("#section"+(numSection - 1)).after(newDiv);
    sections.push( $("section"+(numSection - 1)) );
  }
}

/**
 * Adds text box for skills
 */
function addSkill(){
  var prevId = "#skill" + numSkills;
  ++numSkills;
  var id = "skill" + numSkills;
  var textBox = createTextBox(id);
  $(prevId).after(textBox);
  skills.push( $("#skill" + numSkills));
}

/**
 * Adds text box for language
 */
function addLanguage(){
  var prevId = "#language" + numLanguages;
  ++numLanguages;
  var id = "language" + numLanguages;
  var textBox = createTextBox(id);
  $(prevId).after(textBox);
  languages.push(textBox);
}

/**
 * Adds text box for major
 */
function addMajor(){
  var prevId = "#major" + numMajors;
  ++numMajors;
  var id = "major" + numMajors;
  var textBox = createTextBox(id);
  $(prevId).after(textBox);
  majors.push(textBox);
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
    experience : $('#experience').val()};

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
