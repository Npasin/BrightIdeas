$(document).ready(function(){
    // partial auto-refresh
        // var $container = $("#board");
        // $container.load("partials/idea_feed.html");
        var refreshId = setInterval(function()
        {
            $.ajax({
                url: "/refresh_feed"
            })
            .done(function(response){
                $('#board').html(response);
            })
            return false
            //$container.load('partials/idea_feed.html');
        }, 4000);
    // delete button
        $('#board').on('click','#delete_button', function(){
            var del_id = $(this).attr('class');
            var link ="/delete_idea/" + del_id
            $.ajax({
                url: link
                // data: $("#idea").serialize()
            })
            .done(function(response){
                $("#board").html(response)
            })
            return false
        });
    // submit idea
        $('#idea').submit(function(){
            $.ajax({
                url: "/create_idea",
                method: "POST",
                data: $("#idea").serialize()
            })
            .done(function(response){
                $("#board").html(response)
                $('#idea_textarea').val('');
            })
            return false
        });
    // UnLike idea
    $('#board').on('click','#unlike', function(){
        var unlike_id = $(this).attr('class');
        var link ="/unlike_idea/" + unlike_id
        $.ajax({
            url: link
        })
        .done(function(response){
            $("#board").html(response)
        })
        return false
    });
    // Like idea
    $('#board').on('click','#like', function(){
        var like_id = $(this).attr('class');
        var link ="/like_idea/" + like_id
        $.ajax({
            url: link
        })
        .done(function(response){
            $("#board").html(response)
        })
        return false
    });
    // edit button
        $('#edit_idea').click(function(){
            $("#idea{{idea.idea_id}}").html("<p>test<p>")
        });
        $('.testbutton').click(function(){
            $(".testdiv").html("not working?")
        });
    })