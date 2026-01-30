let lastTimestamp = null;

//To convert ISO String to the required format
function formatTimestamp(isoString) {
    const date = new Date(isoString);

    const day = date.getUTCDate();
    const month = date.toLocaleString("en-US", { month: "long", timeZone: "UTC" });
    const year = date.getUTCFullYear();

    let hours = date.getUTCHours();
    const minutes = date.getUTCMinutes().toString().padStart(2, "0");

    const ampm = hours >= 12 ? "PM" : "AM";
    hours = hours % 12 || 12;

    return `${ordinal(day)} ${month} ${year} - ${hours}:${minutes} ${ampm} UTC`;
}

// Helper to add st, nd, rd, or th to the day
function ordinal(n) {
    if (n > 3 && n < 21) return `${n}th`;
    switch (n % 10) {
        case 1: return `${n}st`;
        case 2: return `${n}nd`;
        case 3: return `${n}rd`;
        default: return `${n}th`;
    }
}


async function fetchEvents() {
    let url = "/events";
    if(lastTimestamp){
        url+= `?since=${encodeURIComponent(lastTimestamp)}`;
    }

    const response = await fetch(url);
    const data = await response.json();

    data.forEach(event => {
        renderEvent(event);
        lastTimestamp = event.timestamp;
    });
    
}

function renderEvent(event){
    const container = document.getElementById("events");
    const div = document.createElement("div");

    div.className = "event";
    div.innerText = formatEvent(event);

    container.appendChild(div);
}

function formatEvent(event) {
    const time = formatTimestamp(event.timestamp);

    if (event.action === "PUSH") {
        return `${event.author} pushed to ${event.to_branch} on ${time}`;
    }

    if (event.action === "PULL_REQUEST") {
        return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${time}`;
    }

    if (event.action === "MERGE") {
        return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${time}`;
    }

    return "";
}
fetchEvents();
setInterval(fetchEvents, 15000);

