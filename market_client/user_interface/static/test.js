
// Example of how to get information
function getClientData(){
    // Specify route
    fetch('/info')
    // Get json of response
    .then((response) => response.json())
    .then((packet) => {
        const testText = document.getElementById("testComponent");


        const {balance,id,orders, owned_shares} = packet["account"];
        console.log(orders);
        

        testText.textContent = `Balance: ${balance} Owned Shares: ${owned_shares}`; 
    })
    .catch((error) =>{
        console.error('Error:', error);
    });
}
// Used to keep track of interval call
var interval_id;
function testRepeat(){
   interval_id = setInterval(() => {getClientData()}, 1000);
}

console.log("hello");
testRepeat();