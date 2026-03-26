window.onload = function () {
    loadTickets();
};

function handleSelectChange() {
    const select = document.getElementById("ticketSelect").value;
    const title = document.getElementById("title");
    const description = document.getElementById("description");

    if (select === "new") {
        title.style.display = "block";
        description.style.display = "block";
    } else {
        title.style.display = "none";
        description.style.display = "none";
    }
}

async function createTicket() {
    const select = document.getElementById("ticketSelect").value;

    let title, description;

    if (select === "new") {
        title = document.getElementById("title").value;
        description = document.getElementById("description").value;
    } else if (select !== "") {
        const selectedTicket = JSON.parse(select);
        title = selectedTicket.title;
        description = selectedTicket.description;
    } else {
        return;
    }

    const btn = document.querySelector("button");
    const result = document.getElementById("result");

    btn.disabled = true;
    btn.textContent = "Analyzing...";
    result.textContent = "";

    const response = await fetch("/ticket", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            description: description
        })
    });

    const data = await response.json();

    document.getElementById("title").value = "";
    document.getElementById("description").value = "";
    result.textContent = "Priority: " + data.priority;

    btn.disabled = false;
    btn.textContent = "Analyze with AI";

    await loadTickets();

    const ticketSelect = document.getElementById("ticketSelect");
    ticketSelect.value = "new";
    handleSelectChange();
}

async function loadTickets() {
    const response = await fetch("/tickets");
    const data = await response.json();

    const list = document.getElementById("list");
    const select = document.getElementById("ticketSelect");

    list.innerHTML = "";

    select.innerHTML = `
        <option value="">Select a ticket</option>
        <option value="new">+ New Ticket</option>
    `;

    data.forEach(ticket => {
        const item = document.createElement("div");
        item.innerText = `${ticket.title} - ${ticket.priority}`;
        item.dataset.priority = ticket.priority;
        list.appendChild(item);

        const option = document.createElement("option");
        option.value = JSON.stringify(ticket);
        option.text = ticket.title;
        select.appendChild(option);
    });

    if (data.length === 0) {
        select.value = "new";
        handleSelectChange();
    }
}

