const base_url = "https://myprojectmanagerapi.pythonanywhere.com/api/v1"
const base = "https://myprojectmanagerapi.pythonanywhere.com"
$("#hold-table").hide()
$.ajax({
    url: `${base_url}/project`,
    type: "GET",
    headers: {
        "Authorization": `Token ${localStorage.getItem("token")}`
    },
    success: (response) => {
        populateTable(response);  
    }
})

$.ajax({
    url: `${base_url}/user-detail`,
    type: "GET",
    headers: {
        "Authorization": `Token ${localStorage.getItem("token")}`
    },
    success: (response) => {
        $("#profile-pic").attr("src", `${base}${response.profile_pic}`)
    }
})

$.ajax({
    url: `${base_url}/team`,
    type: "GET",
    headers: {
        "Authorization": `Token ${localStorage.getItem("token")}`
    },
    success: (response) => {
        let team_option;
        for (let i of response) {
            team_option = $("<option></option>").attr("value", i.id).text(i.name);
            $("#pick-a-team").append(team_option);
        }
    }
})

$.ajax({
    url: `${base_url}/project`,
    type: "GET",
    headers: {
        "Authorization": `Token ${localStorage.getItem("token")}`
    },
    success: (response) => {
        let project_option;
        for (let i of response) {
            project_option = $("<option></option>").attr("value", i.id).text(i.name);
            $("#pick-a-project").append(project_option);
        }
    }
})

$(document).ready(() => {
    $("#sideBarToggle").bind('click', function() {
        $(".transition-all").toggleClass("hidden");
        $("#sideBarToggle").toggleClass("nav-button");
    });

    $("#search-submit").bind('click', (event) => {
        event.preventDefault();
        const searchText = $("#search-bar").val();
        console.log(`${base_url}/project?name=${searchText}`)

        $.ajax({
            url: `${base_url}/project?name=${searchText}`,
            type: "GET",
            headers: {
                "Authorization": `Token ${localStorage.getItem("token")}`
            },
            success: (response) => {
                populateTable(response);  
            }
        })
    })

    $("#add-data").bind('click', () => {
        $(".overlay-div").toggleClass("hidden");
    })

    $("#close").bind('click', () => {
        $(".overlay-div").toggleClass("hidden");
    })

    $("#close-project").bind('click', () => {
        $("#new-model-buttons").toggleClass("hidden");
        $("#new-project-form").toggleClass("hidden");
    })

    $("#close-task").bind('click', () => {
        $("#new-model-buttons").toggleClass("hidden");
        $("#new-task-form").toggleClass("hidden");
    })

    $("#project-add").submit((e) => {
        $("#submit-loader1").toggleClass("hidden");
        $("#submit-btn1").toggleClass("hidden");
        e.preventDefault();

        const form = document.getElementById("project-add")
        const formData = new FormData(form);

        $.ajax({
            url: `${base_url}/project`,
            type: 'POST',
            headers: {
                "Authorization": `Token ${localStorage.getItem("token")}`
            },
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                $("#submit-loader1").toggleClass("hidden");
                $("#submit-btn1").toggleClass("hidden");
                $("#new-model-buttons").toggleClass("hidden");
                $("#new-project-form").toggleClass("hidden");
                $("#errors1").empty()
            },
            error: (xhr, status, error) => {
                $("#submit-loader1").toggleClass("hidden");
                $("#submit-btn1").toggleClass("hidden");
                $("#errors1").empty()
                for (let key in xhr.responseJSON) {
                    $("#errors1").append(`<li style="font-size: 10px; color: red;">${xhr.responseJSON[key][0]}</li>`)
                }
            }
        })
    })

    $("#task-add").submit((e) => {
        $("#submit-loader2").toggleClass("hidden");
        $("#submit-btn2").toggleClass("hidden");
        e.preventDefault();

        const form = document.getElementById("task-add")
        const formData = new FormData(form);

        $.ajax({
            url: `${base_url}/task`,
            type: 'POST',
            headers: {
                "Authorization": `Token ${localStorage.getItem("token")}`
            },
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                $("#submit-loader2").toggleClass("hidden");
                $("#submit-btn2").toggleClass("hidden");
                $("#new-model-buttons").toggleClass("hidden");
                $("#new-task-form").toggleClass("hidden");
                $("#errors2").empty()
            },
            error: (xhr, status, error) => {
                $("#submit-loader2").toggleClass("hidden");
                $("#submit-btn2").toggleClass("hidden");
                $("#errors2").empty()
                for (let key in xhr.responseJSON) {
                    $("#errors2").append(`<li style="font-size: 10px; color: red;">${xhr.responseJSON[key][0]}</li>`)
                }
            }
        })
    })
});

const populateTable = (response) => {
    const table = document.getElementById("project-view");
    $("#project-view").find("tr").remove();
    $("#hold-table").hide()
        document.getElementById("result-length").innerHTML = `${response.length} result found`
        let row, date, new_date;
        let date_options = { month: "short", day: "2-digit", year: "numeric" }
        for (let i of response) {
            row = table.insertRow(-1);
            row.insertCell(0).innerHTML = `<img src="${base}${i.image}" class="rounded-full h-6 w-6"/>`
            date = new Date(i.created_at.split("T")[0])
            new_date = date.toLocaleDateString('en-US', date_options)
            row.insertCell(1).innerHTML = `<div><p class="text-sm font-bold">${i.name}</p><span class="text-xs text-gray-400">${new_date}<span></div>`
            row.insertCell(2).innerHTML = `<span class="bg-blue-50 text-sm font-bold py-2 px-2 rounded-md">${i.due_in}</span>`
            row.insertCell(3).innerHTML = `<div><p class="text-sm font-bold">${i.done_tasks}</p><span class="text-xs text-gray-400">Tasks<span></div>`
            row.insertCell(4).innerHTML = `<div class="w-12"><div class="flex"><img src="../images/icons8-checklist-24.png" class="h-4 w-4"/><span class="text-blue-200 text-xs mr-2">Progress</span></div><progress value="${i.status}" max="100" class="task-progress"></progress></div>`
            // row.insertCell(5).innerHTML = `<img src="../images/Screen Shot 2024-03-15 at 01.36.35.png" class="h-8 w-16"/>`
            let row5 = row.insertCell(5)
            row.insertCell(6).innerHTML = `<button style="width: 10px;"><img src="../images/icons8-three-dots-30.png" alt="edit" class="h-4" style="width: 10px;"/></button>`
            row.classList.add("shadow-md")
            row.classList.add("rounded-md")
            row.classList.add("items-center")
            row.classList.add("h-10")
            // row.innerHTML = `<td>${i.image}</td><td>${i.name}</td><td>${i.due_in}</td><td>${i.done_tasks}</td><td>${i.status}</td><td>${i.team}</td>`;
            $.ajax({
                url: `${base_url}/team-detail/${i.team}`,
                type: "GET",
                headers: {
                    "Authorization": `Token ${localStorage.getItem("token")}`
                },
                success: (response) => {
                    const members = response.members;
                    const length = members.length;
                    const pictures = []
                    for (let i of members) {
                        if (i.profile_pic) {
                            pictures.push(i.profile_pic);
                        }
                    }
                    let diff = pictures.length - members.length;
                    let images;
                    if (diff == 0) {
                        diff = pictures.length - 2;
                    }
                    if (pictures.length >= 3) {
                        images = `<img src="${base}${pictures[0]}" class="h-6 w-6 rounded-full"/><img src="${base}${pictures[2]}" class="h-6 w-6 rounded-full"/>`
                    } else if (pictures.length == 2) {
                        images = `<img src="${base}${pictures[0]}" class="h-6 w-6 rounded-full"/><img src="${base}${pictures[1]}" class="h-6 w-6 rounded-full"/>`
                    } else if (pictures.length == 1) {
                        images = `<img src="${base}${pictures[0]}" class="h-6 w-6 rounded-full"/>`
                    }
                    let extra = ""
                    if (diff >= 0) {
                        extra = `<div class="rounded-full h-6 w-6 bg-blue-300 flex items-center justify-center"><span class="text-xs text-gray-400">+${diff}</span></div>`
                    }
                    row5.innerHTML = `<div class="flex">${images}${extra}</div>`
                }
            })
        }
    $("#hold-table").slideDown(3000)
}