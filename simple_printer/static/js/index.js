responsiveVoice.setDefaultVoice('Russian Female');
$('p').click(function() {
    responsiveVoice.speak($(this).text());
});