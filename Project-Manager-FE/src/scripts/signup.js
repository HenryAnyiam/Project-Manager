const base_url = "https://myprojectmanagerapi.pythonanywhere.com/api/v1"

$(document).ready(() => {
    $("#signup").submit((e) => {
        e.preventDefault();

        const form = document.getElementById("signup")
        const formData = new FormData(form);

        console.log(formData.get('password'))
        $.ajax({
            url: `${base_url}/user`,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                const username = formData.get('username')
                const password = formData.get('password')
                $.ajax({
                    url: `${base_url}/api-auth`,
                    type: 'POST',
                    data: JSON.stringify({ username, password }),
                    contentType: "application/json",
                    success: (res) => {
                        localStorage.setItem("token", res.token);
                        window.location.href = "../templates/home.html";
                    },
                    error: (xhr, status, error) => {
                        console.log(xhr, status, error);
                    }
                })
            },
            error: (xhr, status, error) => {
                for (let key in xhr.responseJSON) {
                    $("#errors").append(`<li style="font-size: 10px; color: red;">${xhr.responseJSON[key][0]}</li>`)
                }
            }
        })
    })
})