
$(window).load(pageLoaded);

/**
 *Once page is loaded get additional information from server about
 *about website
 */
function pageLoaded(){
  console.log("loaded");

  data = { domain : domain,
           template : editMode};
  console.log(domain);

  //requests information from server
  sendAjax("/sites/getSiteData/",data,getData);
}

/**
 * Responds to additional data returned from server
 */
function getData(json){
  console.log(json);
  if( json.error){
    if( json.error == 'INVALID'){
      window.location.href = '/accounts/sites';
    }
  }
  else if( json.template ){
    //should have data to fill into the form
    fillForm(json);
  }
  else{
    console.log("undefined response to getData in editSite.js");
    console.log(json);
  }
}

/**
 * Fills in the form with information from the json file
 */
function fillForm(json){

  console.log(json);
  if(json.template == 'resume'){
    fillResume(json);
  }
  else if(json.template == 'course'){
    fillCourse(json);
  }
 //puts basic information into form
  $('#domain').val(json.domain);
  $('#title').val(json.title);
  $('#author').val(json.author);
  $('#description').val(json.description);

  setSectionValues( json.sections );

}
