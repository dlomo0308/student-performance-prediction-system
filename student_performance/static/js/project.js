/* Project specific Javascript goes here. */

$(document).ready(function() {
    // Make an AJAX request to fetch the error message
    $.ajax({
        url: '/myhistory/',  // Replace with the actual URL
        success: function(data) {
            // Display the error message as a popup
            if (data.error_message) {
                alert(data.error_message);
            }
        }
    });
});



