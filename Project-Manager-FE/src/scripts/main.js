// const sideBarToggle = document.getElementById("sideBarToggle");
// const sidebar = document.querySelector(".transition-all");
$(function() {
    $("#sideBarToggle").bind('click', function() {
        $(".transition-all").toggleClass("hidden");
        $("#sideBarToggle").toggleClass("nav-button");
    });
});
