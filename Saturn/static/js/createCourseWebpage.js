$('#addInstructor').click(addInstructor);
$('#addTa').click(addTa);
$('#addExam').click(addExam);
$('#addGrade').click(addGrade);

$('#submit').click(submitForm);

//variables
var numInstructors = 1;
var numTas = 1;
var numExams = 1;
var numGrades = 1;

//arrays to store dynamic fields
var instructors = [];
var tas = [];
var exams = [];
var grades = [];

//add first element of each to the array
instructors.push( $('#instructor1') );
tas.push( $('#ta1') );
exams.push( $('#exam1') );
grades.push( $('#grade1') );

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


  //data to send to server, submit 1 signifies that this ajax is a form submission
  var data = { courseTemplate : "1", grades : gradeVal, exams : examVal, tas : taVal, instructors : instructorVal, sections : sectionVal, aboutCourse : $('#aboutCourse').val(), syllabus : $('#syllabus').val() };

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
