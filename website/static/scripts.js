function fadeFlash(){
    $(window).load(function(){
        setTimeout(function(){
            $(".alert-success").fadeOut()
        }, 5000);
    });
}