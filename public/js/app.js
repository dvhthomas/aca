var app = app || {};

/*
 * From here:http://stackoverflow.com/questions/647259/javascript-query-string
 *
 * returns: dictionary of query string parameters and values
 */
app.queryString = function () {
  var result = {}, queryString = location.search.substring(1),
      re = /([^&=]+)=([^&]*)/g,
      m;
  while (m === re.exec(queryString)) {
    result[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
  }
  return result;
};

app.parseQueryString = function (queryStringPart) {
  var result = {}, queryString,
      re = /([^&=]+)=([^&]*)/g,
      m;
  queryString = queryStringPart.substring(queryStringPart.search(/\?/)+1);
  while (m === re.exec(queryString)) {
    result[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
  }
  return result;
};

app.round = function roundNumber(num, dec) {
	var result = Math.round(num*Math.pow(10,dec))/Math.pow(10,dec);
	return result;
};

$(document).ready(function(){
    $("#nav li").hover(
        function(){ $("ul", this).fadeIn("fast"); },
        function() { }
    );

});
