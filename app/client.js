'use strict';

var uri = "ws://" + location.host + "/websocket";
var ws = new WebSocket(uri);


$(function () {
  $('form').submit(function(){
    var $this = $(this);
    // ws.onopen = function() {
    //   console.log('sent message: %s', $('#m').val());
    // };
    ws.send($('#m').val());
    $('#m').val('');
    return false;
  });
  ws.onopen = function(evt) {
    console.log('connected');
  }
  ws.onmessage = function(msg){
    var returnObject = JSON.parse(msg.data);
    $('#messages').append($('<li>')).append($('<span id="clientId">').text(returnObject.id)).append($('<span id="clientMessage">').text(returnObject.data));
  };
  ws.onerror = function(err){
    console.log("err", err);
  };
  ws.onclose = function close() {
    console.log('disconnected');
  };
});
