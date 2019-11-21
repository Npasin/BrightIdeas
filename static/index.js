$(document).ready(function(){
// first and last name
$('#reg_fname').keyup(function(){
    var data = $("#reg_form").serialize()  
    $.ajax({
        method: "POST",   
        url: "/reg_fname",
        data: data
    })
    .done(function(res){
        $('#reg_error_fname').html(res) 
    })
})
$('#reg_lname').keyup(function(){
        var data = $("#reg_form").serialize()  
        $.ajax({
            method: "POST",   
            url: "/reg_lname",
            data: data
        })
        .done(function(res){
            $('#reg_error_lname').html(res) 
        })
    })
// email in use check
    $('#reg_email').keyup(function(){
        var data = $("#reg_form").serialize()   // capture all the data in the form in the variable data
        $.ajax({
            method: "POST",   // we are using a post request here, but this could also be done with a get
            url: "/reg_email_check",
            data: data
        })
        .done(function(res){
             $('#reg_error_email').html(res)  // manipulate the dom when the response comes back
        })
    })
// // pw validation
    $('#reg_pw').keyup(function(){
        var data = $("#reg_form").serialize()  
        $.ajax({
            method: "POST",   
            url: "/reg_pw",
            data: data
        })
        .done(function(res){
            $('#reg_error_pw').html(res) 
        })
    })
// // pw match check
    $('#reg_pw_match').keyup(function(){
        var data = $("#reg_form").serialize()  
        $.ajax({
            method: "POST",   
            url: "/reg_pw_match",
            data: data
        })
        .done(function(res){
            $('#reg_error_pw_match').html(res) 
        })
    })
})