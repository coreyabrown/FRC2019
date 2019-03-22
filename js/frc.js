/**
 * This JavaScript file replaces the inline scripts previously used.
 */

 function loadGoogleCharts() {
    google.load("visualization", "1", {packages:["table"]});
    google.load("visualization", "1", {packages:["controls", "corechart"]});
    google.setOnLoadCallback(drawTable);
 }
