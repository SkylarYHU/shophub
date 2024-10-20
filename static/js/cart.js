// handle updating a user's shopping cart by sending product updates to the server
// selects all elements on the page with the class update-cart
var updateBtns = document.getElementsByClassName("update-cart")

//  iterates over all the buttons collected in updateBtns
for(i = 0; i < updateBtns.length; i++){
  // adds an event listener to each button, which listens for a "click" event. When a button is clicked, the anonymous function inside will be executed
  updateBtns[i].addEventListener('click',function(){
    // retrieves the data-product attribute from the clicked button, which contains the productId of the item
    var productId = this.dataset.product
    // retrieves the data-action attribute from the clicked button, which contains the action (e.g., "add", "remove") to be performed
    var action = this.dataset.action
    console.log('productId:', productId, "Action:", action)
  
    console.log("USER:", user)

    //  checks whether the user is authenticated
    if(user == "AnonymousUser"){
      addCookieItem(productId, action)
    }else{
      // If the user is authenticated, the updateUserOrder function is called with the productId and the action as arguments
      updateUserOrder(productId, action)
    }
  })
}

function addCookieItem(productId, action){
  console.log("User is not authenticated...")

  if(action == 'add'){
    if(cart[productId] == undefined){
      cart[productId] = {'quantity':1}
    }else{
      cart[productId]['quantity'] += 1
    }
  }

  if(action == 'remove'){
    cart[productId]['quantity'] -= 1

    if(cart[productId]['quantity'] <= 0){
      console.log("Item should be deleted")
      delete cart[productId];
    }
  }

  console.log('Cart:', cart)
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/" 
  location.reload()
}

//  responsible for sending the cart update request to the server
function updateUserOrder(productId, action){
  console.log("User is anthenticated, sending data...")

    // The URL /update_item/ is the endpoint on the server that will handle the cart update
    var url = '/update_item/'
    // A POST request is sent to the server using the fetch API
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type':'application/json',
        'X-CSRFToken': csrftoken,

      },
      body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
      // Once the server responds, this line parses the response as JSON
      return response.json();
    })
    .then((data) => {
      // The returned data is logged to the console for debugging purposes.
      location.reload()
    });
}