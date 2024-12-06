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
    const investmentAmount = document.querySelector("#investment-amount").value;
    const investmentType = document.querySelector("#investment-type-stocks:checked").value;
    const investmentInterest = document.querySelector("#investments").value.split(",").map(item => item.trim()).filter(item => item);
    const investmentRisk = document.querySelector('input[name="risk"]:checked').value;
    alert(`${investmentType} ${investmentAmount} ${investmentInterest} ${investmentRisk}`);
}