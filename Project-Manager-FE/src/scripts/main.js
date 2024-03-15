const base_url = "https://myprojectmanagerapi.pythonanywhere.com/api/v1"

$.ajax({
    url: `${base_url}/project`,
    type: "GET",
    headers: {
        "Authorization": `Token ${localStorage.getItem("token")}`
    },
    success: (response) => {
        const table = document.getElementById("project-view");
        document.getElementById("result-length").innerHTML = `${response.length} result found`
        let row, date, new_date;
        let date_options = { month: "short", day: "2-digit", year: "numeric" }
        for (let i of response) {
            row = table.insertRow(-1);
            row.insertCell(0).innerHTML = `<img src="https://myprojectmanagerapi.pythonanywhere.com${i.image}" class="rounded-full h-6 w-6"/>`
            date = new Date(i.created_at.split("T")[0])
            new_date = date.toLocaleDateString('en-US', date_options)
            row.insertCell(1).innerHTML = `<div><p class="text-sm font-bold">${i.name}</p><span class="text-xs text-gray-400">${new_date}<span></div>`
            row.insertCell(2).innerHTML = `<span class="bg-blue-50 text-sm font-bold py-2 px-2 rounded-md">${i.due_in}</span>`
            row.insertCell(3).innerHTML = `<div><p class="text-sm font-bold">${i.done_tasks}</p><span class="text-xs text-gray-400">Tasks<span></div>`
            row.insertCell(4).innerHTML = `<div class="w-12"><div class="flex"><img src="../images/icons8-checklist-24.png" class="h-4 w-4"/><span class="text-blue-200 text-xs mr-2">Progress</span></div><progress value="${i.status}" max="100" class="task-progress"></progress></div>`
            row.insertCell(5).innerHTML = `<img src="../images/Screen Shot 2024-03-15 at 01.36.35.png" class="h-8 w-16"/>`
            row.insertCell(6).innerHTML = `<button style="width: 10px;"><img src="../images/icons8-three-dots-30.png" alt="edit" class="h-4" style="width: 10px;"/></button>`
            row.classList.add("shadow-md")
            row.classList.add("rounded-md")
            row.classList.add("items-center")
            row.classList.add("h-10")
            // row.innerHTML = `<td>${i.image}</td><td>${i.name}</td><td>${i.due_in}</td><td>${i.done_tasks}</td><td>${i.status}</td><td>${i.team}</td>`;
        }
        
    }
})


$(document).ready(() => {
    $("#sideBarToggle").bind('click', function() {
        $(".transition-all").toggleClass("hidden");
        $("#sideBarToggle").toggleClass("nav-button");
    });
});