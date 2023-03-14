const updateBtns = document.querySelectorAll('.update-cart')

updateBtns.forEach(btn => {
    btn.addEventListener('click' , function() {
        
        let productId = this.dataset.product
        let action = this.dataset.action
        if(user == 'AnonymousUser') {
            addCookieItem(productId , action)
            console.log('User is not authenticated');
        } else {
            updateUserOrder(productId , action  )
        }
    })
});


function addCookieItem (productId , action) {
    if(action == "add") {
        if(cart[productId] == undefined) {
            cart[productId] = {'quantity' : 1}
        } else {
            cart[productId]['quantity'] += 1
        } 
    }

    if(action == "remove") {
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0) {
            console.log('Remove Item');
            delete cart[productId]
        }
    }

    console.log(cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload()
}


// ###############################
const updateUserOrder = (productId , action ) => {
    console.log('User is authenticated, sending data...');

    let url = '/uptade_item/'
    fetch(url ,{
        method: 'POST',
        headers : {
            'Content-type' : 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body : JSON.stringify({'productId':productId , 'action' : action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log({data});
        location.reload()
    })
}
