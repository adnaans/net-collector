//Get metrics from the client continuously
//Store as var metric
if(metric >= 25){
  console.log("Get back to work!");
  //Make TV screen go off
  document.getElementById("msg").innerHTML = "GET BACK TO WORK!";
  document.getElementById("bg").style.backgroundColor =	"#FF0000";
}