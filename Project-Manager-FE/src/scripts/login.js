const base_url = "https://myprojectmanagerapi.pythonanywhere.com/api/v1"

$(document).ready(() => {
    $("#login").submit((e) => {
        $("#login-loader").toggleClass("hidden");
        $("#login-btn").toggleClass("hidden");
        e.preventDefault();

        const username = document.getElementById("username").value
        const password = document.getElementById("password").value

        $.ajax({
            url: `${base_url}/api-auth`,
            type: 'POST',
            data: JSON.stringify({ username, password }),
            contentType: "application/json",
            success: (res) => {
                $("#login-loader").toggleClass("hidden");
                $("#login-btn").toggleClass("hidden");
                localStorage.setItem("token", res.token);
                window.location.href = "../templates/home.html";
            },
            error: (xhr, status, error) => {
                $("#login-loader").toggleClass("hidden");
                $("#login-btn").toggleClass("hidden");
                $("#errors").empty()
                console.log(xhr.responseJSON)
                for (let key in xhr.responseJSON) {
                    $("#errors").append(`<li style="font-size: 10px; color: red;">${xhr.responseJSON[key][0]}</li>`)
                }
            }
        })
    })
})

