document.querySelector("#investment-type-stocks").addEventListener("click", function() {
    if(document.querySelector("#investment-type-stocks").checked && document.querySelector("#investment-type-stocks")) {
        document.querySelector(".investment-interest-area").style.display = "block";
    } 
})