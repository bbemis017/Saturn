
$('#domain').on('input',replaceSpaces);

$('#domain').focusout(checkDomain);

$('#addMajor').click(addMajor);
$('#addLanguage').click(addLanguage);
$('#addSkill').click(addSkill);
$('#addSection').click(addSection);

//variables
var domainApproved = false;
var numMajors = 1;
var numLanguages = 1;
var numSkills = 1;
var numSection = 0;

/**
 * adds Section
 */
function addSection(){
  if( numSection == 0){
    $('#section1').show();
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
 * send domain that the user entered to the backend
 */
function checkDomain(){
  var domain = $('#domain').val()
  $.ajax({url : "/sites/createSite/", type : "POST",
  data : { csrfmiddlewaretoken: csrf_token , domain_json : domain },
    success : domainResponse,
    error : responseFailure
  });
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
