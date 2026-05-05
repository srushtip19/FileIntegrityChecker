const socket = io();

socket.on("connect", () => {
    console.log("✅ Connected to server");
});

socket.on("connect_error", (err) => {
    console.log("❌ Connection failed:", err);
});

let barChart, pieChart;

const barCtx = document.getElementById('barChart').getContext('2d');
const pieCtx = document.getElementById('pieChart').getContext('2d');

barChart = new Chart(barCtx, {
    type: 'bar',
    data: {
        labels: ['Modified', 'Deleted', 'New'],
        datasets: [{
            data: [0, 0, 0],
            backgroundColor: ['orange', 'red', 'green']
        }]
    }
});

pieChart = new Chart(pieCtx, {
    type: 'pie',
    data: {
        labels: ['Modified', 'Deleted', 'New'],
        datasets: [{
            data: [0, 0, 0]
        }]
    }
});

socket.on("update", (data) => {
    console.log("🔥 DATA RECEIVED:", data);

    document.getElementById("critical").innerText = data.deleted;
    document.getElementById("warning").innerText = data.modified;
    document.getElementById("new").innerText = data.new;

    barChart.data.datasets[0].data = [data.modified, data.deleted, data.new];
    barChart.update();

    pieChart.data.datasets[0].data = [data.modified, data.deleted, data.new];
    pieChart.update();

    let log = document.createElement("p");
    log.innerText = `[${new Date().toLocaleTimeString()}] ${data.log}`;
    document.getElementById("logBox").prepend(log);

    let alert = document.createElement("p");
    alert.innerText = "🚨 " + data.log;
    alert.style.color = "red";
    document.getElementById("alertBox").prepend(alert);
});


function createBaseline() {
    fetch('/create_baseline')
    .then(res => res.json())
    .then(() => alert("✅ Baseline Created"));
}

function startMonitor() {
    fetch('/start');
}

function stopMonitor() {
    fetch('/stop');
}

function startMonitor() {
    console.log("▶ Monitoring Started");

    const status = document.getElementById("status");
    status.innerText = "● Running";
    status.style.color = "lime";   // 🟢 Green
}

function stopMonitor() {
    console.log("⏹ Monitoring Stopped");

    const status = document.getElementById("status");
    status.innerText = "● Stopped";
    status.style.color = "red";    // 🔴 Red
}