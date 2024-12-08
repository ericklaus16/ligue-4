checkedStocks = false;
checkedFunds = false;

document.querySelector("#investment-type-stocks").addEventListener("click", () => {
    checkedStocks = !checkedStocks;
    toggleInvestmentInterest()
})

document.querySelector("#investment-type-funds").addEventListener("click", () => {
    checkedFunds = !checkedFunds;
    toggleInvestmentInterest()
})

function toggleInvestmentInterest() {
    document.querySelector('.investment-interest-area').style.display = (checkedStocks || checkedFunds) ? 'block' : 'none';
}

function handleCalculateInvestment() {
    let investmentAmount = document.querySelector("#investment-amount").value;
    let investmentType = document.querySelector("#investment-type-stocks:checked").value;
    let investmentInterest = document.querySelector("#investments").value.split(",").map(item => item.trim()).filter(item => item);
    let investmentRisk = document.querySelector('input[name="risk"]:checked').value;

    let timerInterval;
    let startTime = Date.now();

    Swal.fire({
        title: "Olá, tudo bem?",
        html: "Por favor aguarde enquanto nosso sistema faz alguns cálculos!", 
        didOpen: () => {
            Swal.showLoading();
            const timer = Swal.getPopup().querySelector("b");
            timerInterval = setInterval(() => {
                timer.textContent = `${(Swal.getTimerLeft() / 1000).toFixed(2)}`;
            }, 100);
        },
        willClose: () => {
            clearInterval(timerInterval); 
        }
    });
    
    fetch('/calcular-risco', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            investmentAmount,
            investmentType,
            investmentInterest,
            investmentRisk
        })
    })
    .then(response => response.json()) 
    .then(data => {
        Swal.close(); 
        window.location = '/results'; 
    })
    .catch(error => {
        Swal.close();
        console.error("Erro ao calcular risco:", error); 
        Swal.fire('Erro!', 'Houve um problema ao processar os dados. Tente novamente mais tarde.', 'error');
    });
}