$('#addInstructor').click(addInstructor);
$('#addTa').click(addTa);
$('#addExam').click(addExam);
$('#addGrade').click(addGrade);
$('#addLink').click(addLink);

$('#submit').click(submitForm);

//variables
var numInstructors = 1;
var numTas = 1;
var numExams = 1;
var numGrades = 1;
var numLinks = 1;

//arrays to store dynamic fields
var instructors = [];
var tas = [];
var exams = [];
var grades = [];
var links = [];

//add first element of each to the array
instructors.push( $('#instructor1') );
tas.push( $('#ta1') );
exams.push( $('#exam1') );
grades.push( $('#grade1') );
links.push( $('#link1') );

/**
 * Submit button is clicked
 */
function submitForm(){
  console.log("submit");
  //TODO:do some error checking
  //backend should expect errors in data anyways

  var gradeVal = getValues(grades);
  var examVal = getValues(exams);
  var taVal = getValues(tas);
  var instructorVal = getValues(instructors);

  var sectionVal = getSectionValues();

  var link_domains = getValues(links);

  //data to send to server, submit 1 signifies that this ajax is a form submission
  var data = { courseTemplate : "1", grades : gradeVal, exams : examVal, tas : taVal, instructors : instructorVal, sections : sectionVal, aboutCourse : $('#aboutCourse').val(), syllabus : $('#syllabus').val(), link_domains : link_domains };

  submit("/sites/createSite/",data,courseWebpageResponse);
}

/**
 * recieves response from from server after form submission
 */
function courseWebpageResponse(json){
  //respond to errors specific to creating a resume

  //always calls submitResponse from createSite.js
  //to respond to errrors general to creating a site and redirecting to
  //the next page
  submitResponse(json);
}

/**
 * Adds select for link
 */
function addLink(){
  var string = "link"

  ++numLinks;

  var div = $('#container_' + string + 1).clone();

  var id = "container_" + string + numLinks;
  div.attr("id",id);

  var select = div.find("#" + string + "1");
  select.attr('id',id);
  select.val("");

  links.push( select );

  var dId = "d" + string + numLinks;

  var del = createDelete(dId);
  var delDiv = div.find("#" + string + "Del");
  delDiv.append(del);

  $('#' + string).append(div);

  $("#" + dId).click(function(){
    var d = this.id.substr(1,this.id.length);
    var index = links.indexOf( select );
    links.splice(index,1);
    $("#container_" + d).remove();
    $("#" + d).remove();
    $("#" + this.id).remove();
  });

}

/**
 * Adds text box for instructor
 */
function addInstructor(){
  numInstructors = addBox("instructor",instructors,numInstructors);
}

/**
 * Adds text box for ta
 */
function addTa(){
  numTas = addBox("ta",tas,numTas);
}

/**
 * Adds text box for exam
 */
function addExam(){
  numExams = addBox("exam",exams,numExams);
}

/**
 * Adds text box for grade
 */
function addGrade(){
  numGrades = addBox("grade",grades,numGrades);
}
