$('#addMajor').click(addMajor);
$('#addLanguage').click(addLanguage);
$('#addSkill').click(addSkill);
$('#addSection').click(addSection);

$('#submit').click(submitForm);

//variables
var numMajors = 1;
var numLanguages = 1;
var numSkills = 1;
var numSection = 1;

//arrays to store dynamic fields
var majors = [];
var languages = [];
var skills = [];
var sections = [];

//add first element of each to the array
majors.push( $('#major1') );
languages.push( $('#language1') );
skills.push( $('#skill1') );

/**
 * Submit button is clicked
 */
function submitForm(){
  console.log("submit");
  //TODO:do some error checking
  //backend should expect errors in data anyways

  var skillVal = getValues(skills);
  var languageVal = getValues(languages);
  var majorVal = getValues(majors);

  var sectionVal = getSectionValues();


  //data to send to server, submit 1 signifies that this ajax is a form submission
  var data = { skills : skillVal, languages : languageVal,
    majors : majorVal, sections : sectionVal, name : $('#name').val(),
    education : $('#education').val(), gpa : $('#gpa').val(),
    experience : $('#experience').val(), summary : $('#summary').val() };

  submit("/sites/createSite/",data,resumeResponse);
}

/**
 * recieves response from from server after form submission
 */
function resumeResponse(json){
  //respond to errors specific to creating a resume

  //always calls submitResponse from createSite.js
  //to respond to errrors general to creating a site and redirecting to
  //the next page
  submitResponse(json);
}

/**
 * Adds text box for major
 */
function addMajor(){
  numMajors = addBox("major",majors,numMajors);
}

/**
 * Adds text box for language
 */
function addLanguage(){
  numLanguages = addBox("language",languages,numLanguages);
}

/**
 * Adds text box for skills
 */
function addSkill(){
  numSkills = addBox("skill",skills,numSkills);
}

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
