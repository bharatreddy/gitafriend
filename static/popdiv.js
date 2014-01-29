// Jquery script to pop up the divs with info on hover
// We basically check for trigger events for all the 10 suggestions
// Written By Bharat Kunduri

$(document).ready(function() {

// Div 1
  $(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('a#trigger1').hover(function(e) {
      $('div#pop-up1').show();
        //.css('top', e.pageY + moveDown)
        //.css('left', e.pageX + moveLeft)
        //.appendTo('body');
    }, function() {
      $('div#pop-up1').hide();
    });

    $('a#trigger1').mousemove(function(e) {
      $('div#pop-up1').css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
    });

  });

// Div2
$(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('a#trigger2').hover(function(e) {
      $('div#pop-up2').show();
        //.css('top', e.pageY + moveDown)
        //.css('left', e.pageX + moveLeft)
        //.appendTo('body');
    }, function() {
      $('div#pop-up2').hide();
    });

    $('a#trigger2').mousemove(function(e) {
      $('div#pop-up2').css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
    });

  });

// Div3
$(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('a#trigger3').hover(function(e) {
      $('div#pop-up3').show();
        //.css('top', e.pageY + moveDown)
        //.css('left', e.pageX + moveLeft)
        //.appendTo('body');
    }, function() {
      $('div#pop-up3').hide();
    });

    $('a#trigger3').mousemove(function(e) {
      $('div#pop-up3').css('top', e.pageY + moveDown).css('left', e.pageX - 20 * moveLeft);
    });

  });

//Div4
$(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('a#trigger4').hover(function(e) {
      $('div#pop-up4').show();
        //.css('top', e.pageY + moveDown)
        //.css('left', e.pageX + moveLeft)
        //.appendTo('body');
    }, function() {
      $('div#pop-up4').hide();
    });

    $('a#trigger4').mousemove(function(e) {
      $('div#pop-up4').css('top', e.pageY + moveDown).css('left', e.pageX - 30 * moveLeft);
    });

  });

// Div 5
$(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('a#trigger5').hover(function(e) {
      $('div#pop-up5').show();
        //.css('top', e.pageY + moveDown)
        //.css('left', e.pageX + moveLeft)
        //.appendTo('body');
    }, function() {
      $('div#pop-up5').hide();
    });

    $('a#trigger5').mousemove(function(e) {
      $('div#pop-up5').css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
    });

  });

// Div 6
$(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('a#trigger6').hover(function(e) {
      $('div#pop-up6').show();
        //.css('top', e.pageY + moveDown)
        //.css('left', e.pageX + moveLeft)
        //.appendTo('body');
    }, function() {
      $('div#pop-up6').hide();
    });

    $('a#trigger6').mousemove(function(e) {
      $('div#pop-up6').css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
    });

  });

// Div 7
$(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('a#trigger7').hover(function(e) {
      $('div#pop-up7').show();
        //.css('top', e.pageY + moveDown)
        //.css('left', e.pageX + moveLeft)
        //.appendTo('body');
    }, function() {
      $('div#pop-up7').hide();
    });

    $('a#trigger7').mousemove(function(e) {
      $('div#pop-up7').css('top', e.pageY + moveDown).css('left', e.pageX - 20 * moveLeft);
    });

  });

// Div 8
$(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('a#trigger8').hover(function(e) {
      $('div#pop-up8').show();
        //.css('top', e.pageY + moveDown)
        //.css('left', e.pageX + moveLeft)
        //.appendTo('body');
    }, function() {
      $('div#pop-up8').hide();
    });

    $('a#trigger8').mousemove(function(e) {
      $('div#pop-up8').css('top', e.pageY + moveDown).css('left', e.pageX - 30 * moveLeft);
    });

  });


// Div 9
$(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('a#trigger9').hover(function(e) {
      $('div#pop-up9').show();
        //.css('top', e.pageY + moveDown)
        //.css('left', e.pageX + moveLeft)
        //.appendTo('body');
    }, function() {
      $('div#pop-up9').hide();
    });

    $('a#trigger9').mousemove(function(e) {
      $('div#pop-up9').css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
    });

  });

// Div 10
$(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('a#trigger10').hover(function(e) {
      $('div#pop-up10').show();
        //.css('top', e.pageY + moveDown)
        //.css('left', e.pageX + moveLeft)
        //.appendTo('body');
    }, function() {
      $('div#pop-up10').hide();
    });

    $('a#trigger10').mousemove(function(e) {
      $('div#pop-up10').css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
    });

  });

});
