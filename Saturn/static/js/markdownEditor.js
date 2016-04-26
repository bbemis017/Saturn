var currentEditor = null;
/**
 * inserts image url into currentEditor markdown
 */
function insertImage(url){
  var str = "![](/static/uploads/" + url;
  currentEditor.options.insertTexts.image[0] = str;
  currentEditor.options.insertTexts.image[1] = ")";
  currentEditor.drawImage();
  currentEditor = null;
  $('#selectFile').modal('hide');
}

/**
 * inserts file url into currentEditor markdown
 */
function insertFile(name,url){
  var str = name + "](/static/uploads/" + url + ")";
  currentEditor.options.insertTexts.link[0] = "[";
  currentEditor.options.insertTexts.link[1] = str;
  currentEditor.drawLink();
  currentEditor = null;
  $('#selectFile').modal('hide');
}

/**
 * Creates a markdown editor with custom settings
 * @return SimpleMDE
 */
function createEditor(id){
  var editor = new SimpleMDE({
    autofocus: false,
    autosave: {
      enabled: true,
      uniqueId: "{{ request.user.username }}_summary_{{ request.user.account.get_next_website_id }}",
      delay: 1000,
    },
    insertTexts: {
      image: ["![](http://test)"],
      link: ["[","](http://)"],
    },
    toolbar: [
    { 
      name: "bold",
      action: SimpleMDE.toggleBold,
      className: "fa fa-bold",
      title: "Bold",
    },
    {
      name: "Italics",
      action: SimpleMDE.toggleItalic,
      className: "fa fa-italic",
      title: "Italic",
    },
    {
      name: "heading",
      action: SimpleMDE.toggleHeadingSmaller,
      className: "fa fa-header",
      title: "Heading",
    },
    "|",
    { 
      name: "quote",
      action: SimpleMDE.toggleBlockquote,
      className: "fa fa-quote-left",
      title: "Quote",
    },
    {
      name: "unordered-list",
      action: SimpleMDE.toggleUnorderedList,
      className: "fa fa-list-ul",
      title: "Generice List",
    },
    {
      name: "link",
      action: SimpleMDE.drawLink,
      className: "fa fa-link",
      title: "Create Link",
    },
    {
      name: "File",
      action: function addFile(element){
        $('#selectFile').modal();
        currentEditor = element;
      },
      className: "glyphicon glyphicon-file",
      title: "Insert File",
    },
    ],
    element: $(id)[0],
    spellChecker: false,
    tabSize: 4,
  });
  editor.value("");
  return editor;
}
