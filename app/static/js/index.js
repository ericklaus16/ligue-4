checkedStocks = false;
checkedFunds = false;

document.querySelector("#investment-type-stocks").addEventListener("click", function() {
    checkedStocks = !checkedStocks;
    toggleInvestmentInterest()
})

document.querySelector("#investment-type-funds").addEventListener("click", function() {
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
    alert(investmentType + " " + investmentAmount + " " + investmentInterest + " " + investmentRisk);
}