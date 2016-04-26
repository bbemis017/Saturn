$('#addMajor').click(addMajor);
$('#addLanguage').click(addLanguage);
$('#addSkill').click(addSkill);
$('#openSelectImage').click(openSelectImage);


$('#submit').click(submitForm);

//variables
var numMajors = 1;
var numLanguages = 1;
var numSkills = 1;


//arrays to store dynamic fields
var majors = [];
var languages = [];
var skills = [];

//markdown editors
var summary;
var experience;

//image content added by button
var summaryImage;


//add first element of each to the array
majors.push( $('#major1') );
languages.push( $('#language1') );
skills.push( $('#skill1') );

if(!editorsDefined){
  summary = createEditor('#summary');
  experience = createEditor('#experience');
  editorsDefined = true;
}

/**
 * Opens modal to Add Image to Summary Section
 */
function openSelectImage(){
  $('#selectImage').modal('show');
}

/**
 * Stores Image url in summaryImage to be sent
 * through ajax later
 */
function addImage(filecontent){
  summaryImage = filecontent;
  $('#selectImage').modal('hide');
  $('#displayImage').attr('src','/static/uploads/' + filecontent);
}

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
  var data = { resumeTemplate : "1", skills : skillVal, languages : languageVal,
    majors : majorVal, sections : sectionVal, name : $('#name').val(),
    education : $('#education').val(), gpa : $('#gpa').val(),
    experience : experience.value(), summary : summary.value(), summaryImage : summaryImage };

  if( editMode == "")
    submit("/sites/createSite/",data,resumeResponse);
  else
    submit("/sites/editSite/",data,resumeResponse);
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
 * Fills in the resume with information when user decides to edit
 * existing resume
 */
function fillResume(json){

  if (!editorsDefined){
    summary = createEditor('#summary');
    experience = createEditor('#experience');
    editorsDefined = true;
  }

  summary.value(json.summary);
  $('#name').val(json.name);
  $('#education').val(json.education);
  $('#gpa').val(json.gpa);
  experience.value(json.experience);

  if( json.summaryImage != undefined){
    addImage( json.summaryImage);
  }
  console.log(json.summaryImage);


  numMajors = setInitialValues( json.majors, 'major', majors, numMajors);
  numLangauges = setInitialValues( json.languages, 'language', languages, numLanguages);
  numSkills = setInitialValues( json.skills, 'skill', skills, numSkills);
}



