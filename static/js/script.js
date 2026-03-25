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

    document.getElementById("result").innerText = "Priority: " + data.priority;

    loadTickets();
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
        list.appendChild(item);

        const option = document.createElement("option");
        option.value = JSON.stringify(ticket);
        option.text = ticket.title;
        select.appendChild(option);
    });

    // Se não houver tickets, abre automaticamente o formulário de novo ticket
    if (data.length === 0) {
        select.value = "new";
        handleSelectChange();
    }
}

window.onload = function () {
    loadTickets();
};
