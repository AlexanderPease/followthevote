// Loads URL once DOM is ready
chrome.tabs.getSelected(null,function(tab) {
  $('#title').html('<h4>Showing correspondence with ' + clean_url(tab.url) + '</h4>');

  names = ['Albert', 'Andy', 'Brad', 'Brian', 'Brittany', 'Fred', 'John', 'Nick', 'Zander']
  for (i=0; i<names.length; i++){
      var html = "<tr class=\"account_row\" id=\""
      html += names[i] + "\"><td>"
      html += names [i] + "</td><td class=\"account_row_total_emails_in\">loading...</td><td class=\"account_row_latest_email_in\"></td><td class=\"account_row_total_emails_out\"></td><td class=\"account_row_latest_email_out\"></td></tr>"
      $('.table tr:last').after(html);
  }

  $('.account_row').each(function() {
    var query = clean_url(tab.url);
    if (query) {
      //$(this).show();
      var url = "www.usv.com/admin/gmailapi?";
      url += "q=" + query; 
      url += "&n=" + $(this).attr('id');
      
      console.log("Querying " + url);
      $.ajax("http://" + url, { // For some reason only works when string + url variable
            error: function(jqxhr, status, error) {
              console.log("Error: " + error);
            },
            success: function(data, status, jqxhr) {            
              updateRow(data);
            }
          });
    }
  });
});

// Just splits out base url from href
function clean_url(url) {
  if (url.indexOf("http://") != -1) {
    url = url.split("http://")[1];
  }
  else if (url.indexOf("https://") != -1) {
    url = url.split("https://")[1];
  }
  if (url.indexOf("www.") != -1) {
    url = url.split("www.")[1];
  }
  if (url.indexOf("/") != -1) {
    url = url.split("/")[0];
  }
  return url;
}

// Updates row upon successful API call
function updateRow(data) {
  var correspondence = JSON.parse(data);
  var name = correspondence['name'];
  if (correspondence['err']) {
    $('#' + name).children('.account_row_total_emails_in').text(0);
    $('#' + name).children('.account_row_latest_email_in').text('N/A');
    $('#' + name).children('.account_row_total_emails_out').text(0);
    $('#' + name).children('.account_row_latest_email_out').text('N/A');
  }
  else {
    $('#' + name).children('.account_row_total_emails_in').text(correspondence['total_emails_in']);
    $('#' + name).children('.account_row_latest_email_in').text(correspondence['latest_email_in']);
    $('#' + name).children('.account_row_total_emails_out').text(correspondence['total_emails_out']);
    $('#' + name).children('.account_row_latest_email_out').text(correspondence['latest_email_out']);
  } 
}
