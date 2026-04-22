function runCode() {
    console.log("RUN BUTTON CLICKED");   // 👈 detect multiple clicks

    let code = document.getElementById("code").value;
    let language = document.getElementById("language").value;

    let outputBox = document.getElementById("output");

    fetch("http://127.0.0.1:5000/run", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            code: code,
            language: language
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("RESPONSE:", data);

        if (data.output && data.output.trim() !== "") {
            outputBox.innerText = data.output;
        } else if (data.error && data.error.trim() !== "") {
            outputBox.innerText = data.error;
        }
    })
    .catch(err => {
        console.log("ERROR:", err);
    });
}