let lastTimestamp = null;


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

function formatEvent(event){
    if(event.action === "PUSH"){
        return `${event.author} pushed to ${event.to_branch} on ${event.timestamp}`;
    }
    if(event.action === "PULL_REQUEST"){
        return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
    }
    if(event.action === "MERGE"){
        return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
    }

    return "";
}
fetchEvents();
setInterval(fetchEvents, 15000);

// getelementbyid