let typedWords = [];
let expectedWords = [];
let timer = null;
let timeLeft = 30;
let username = "";


document.getElementById("startBtn").onclick = async function() {
    username = document.getElementById("username").value.trim();
    if (!username) { alert("Podaj username!"); return; }

    const res = await fetch('/api/game/words');
    const data = await res.json();
    expectedWords = data.words;

    let html = "";
    for(let i=0; i<expectedWords.length; ++i) {
        html += `<span class="word" id="word${i}">${expectedWords[i]}</span> `;
    }
    document.getElementById("words").innerHTML = html;
    document.querySelectorAll('.current').forEach(el => el.classList.remove('current'));
    document.getElementById("word0").classList.add("current");

    typedWords = [];
    timeLeft = 30;
    document.getElementById("setup").style.display = "none";
    document.getElementById("game").style.display = "block";
    document.getElementById("result").style.display = "none";
    document.getElementById("timer").innerText = timeLeft;
    document.getElementById("inputArea").value = "";
    document.getElementById("inputArea").disabled = false;
    document.getElementById("inputArea").focus();
    document.getElementById("liveWPM").innerText = "0";
    document.getElementById("liveAcc").innerText = "0";
    document.getElementById("liveStats").style.display = "block";

    window.ended = false;

    timer = setInterval(() => {
        timeLeft -= 1;
        document.getElementById("timer").innerText = timeLeft;
        updateLiveStats();
        if (timeLeft <= 0) {
            clearInterval(timer);
            endGame();
        }
    }, 1000);
};

document.getElementById("inputArea").addEventListener("keydown", function(e) {
    if (e.key === " " || e.key === "Enter") {
        e.preventDefault();
        if (typedWords.length >= expectedWords.length) return this.value = "";

        let word = this.value.trim();
        if (word) {
            let idx = typedWords.length;
            typedWords.push(word);
            updateLiveStats();

            const wspan = document.getElementById("word" + idx);
            if (wspan) {
                wspan.classList.add("used");
                wspan.classList.add(word === expectedWords[idx] ? "correct" : "incorrect");
                wspan.classList.remove("current");
            }
            const next = document.getElementById("word" + (idx + 1));
            if (next) next.classList.add("current");
        }
        this.value = "";

        if (typedWords.length >= expectedWords.length) {
            document.getElementById("inputArea").disabled = true;
            clearInterval(timer);
            endGame();
        }
    }
});

function updateLiveStats() {
    let correct = 0;
    let totalChars = 0;
    let now = 30 - timeLeft;
    if (now === 0) now = 1;

    for (let i = 0; i < typedWords.length; ++i) {
        if (typedWords[i] === expectedWords[i]) correct++;
        totalChars += typedWords[i].length;
    }
    let wpm = Math.round((totalChars / 5) / (now / 60));
    let accuracy = typedWords.length ? Math.round((correct / typedWords.length) * 100) : 0;
    document.getElementById("liveWPM").innerText = wpm;
    document.getElementById("liveAcc").innerText = accuracy;

}

function goHome() {
    document.getElementById("setup").style.display = "block";
    document.getElementById("game").style.display = "none";
    document.getElementById("result").style.display = "none";
    document.getElementById("inputArea").value = "";
    document.getElementById("username").focus();
    window.ended = false;
}

async function endGame() {
    if (window.ended) return;
    window.ended = true;
    document.getElementById("inputArea").disabled = true;
    document.getElementById("liveStats").style.display = "none";

    const res = await fetch('/api/game/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ username, typed_words: typedWords, expected_words: expectedWords, time: 30 })
    });
    const result = await res.json();

    document.getElementById("game").style.display = "none";
    document.getElementById("result").innerHTML = `
        <h2>Koniec gry!</h2>
        <p>Użytkownik: <span id="usernameSummary">${username}</span></p>
        <p>WPM: <b>${result.wpm}</b></p>
        <p>Accuracy: <b>${result.accuracy}</b>%</p>
        <button onclick="location.reload()">Zagraj jeszcze raz</button>
    `;
    document.getElementById("result").style.display = "block";
    document.getElementById("result").innerHTML = `
    <h2>Koniec gry!</h2>
    <p>Użytkownik: <span id="usernameSummary">${username}</span></p>
    <p>WPM: <b>${result.wpm}</b></p>
    <p>Accuracy: <b>${result.accuracy}</b>%</p>
    <button onclick="location.reload()">Zagraj jeszcze raz</button>
    <button onclick="goHome()">Home</button>
`;
}

document.getElementById("showHighscoresBtn").onclick = async function() {
    const res = await fetch('/api/highscores');
    const data = await res.json();
    let html = `<h3>Top 10 – Global</h3>`;
    html += `<table><tr><th>#</th><th>User</th><th>WPM</th><th>Acc (%)</th></tr>`;
    data.forEach((s, i) => {
        html += `<tr><td>${i + 1}</td><td>${s.username}</td><td>${s.wpm}</td><td>${s.accuracy}</td></tr>`;
    });
    html += `</table>`;
    document.getElementById("modalBody").innerHTML = html;
    document.getElementById("modal").style.display = "flex";
};

document.getElementById("showMyHighscoresBtn").onclick = async function() {
    let uname = document.getElementById("username").value.trim();
    if (!uname) { alert("Najpierw wpisz swój username!"); return; }
    const res = await fetch(`/api/highscores/user?username=${encodeURIComponent(uname)}`);
    const data = await res.json();
    let html = `<h3>Twoje TOP 10</h3>`;
    html += `<table><tr><th>#</th><th>User</th><th>WPM</th><th>Acc (%)</th></tr>`;
    data.forEach((s, i) => {
        html += `<tr><td>${i + 1}</td><td>${s.username}</td><td>${s.wpm}</td><td>${s.accuracy}</td></tr>`;
    });
    html += `</table>`;
    document.getElementById("modalBody").innerHTML = html;
    document.getElementById("modal").style.display = "flex";
};

function closeModal(event) {
    document.getElementById("modal").style.display = "none";
}