var serviceHostName = "127.0.0.1";
function getCart() {
    
    /* Definition */
    var customerID = sessionStorage.getItem('userId');
    var content = document.getElementById('content');

    var products = [];

    var total_quatity = 0;
    var total_price = 0;

    var priceEle = document.getElementById('total_price');
    var quantityEle = document.getElementById('total_quantity');

    /* Inventory API stuff */
    $(async () => {
        var serviceURL = "http://" + serviceHostName + ":8000/api/v1/products";
        try {
            const response = await fetch(serviceURL, { method: 'GET' });
            const result = await response.json()

            if (response.ok) {
                products = result;
                $(async () => {
                    var serviceURL = "http://" + serviceHostName + ":8000/api/v1/check";

                    var obj = {
                        "customerID": customerID
                    }
                    try {
                        const response =
                            await fetch(
                                serviceURL, {
                                method: 'POST',
                                headers: {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'
                                }
                                , body: JSON.stringify(obj)
                            });

                        const result = await response.json();

                        if (response.status === 200 || response.status === 201) {
                            var obj = result.data;
                            cartData = obj['check_vcart_result']
                            cartItems = cartData.data.cartItems
                            
                            if (cartItems.length == 0) {
                                content.innerHTML = '<h5 class="text-center">Your cart is empty</h5>'
                            } else {
                                for (let i = 0; i < cartItems.length; i++) {
                                    id = cartItems[i][0]
                                    quantity = cartItems[i][1]

                                    /* Check against inventory */
                                    for (let j = 0; j < products.length; j++) {
                                        if (products[j].id == id) {
                                            product = products[j]
                                            break;
                                        }
                                    }
                                    item_price = product.price * quantity
                                    total_price += item_price
                                    total_quatity += quantity
                                    idString = id.toString()  
                                    storeString = product.storeId.toString();


                                    names_lower = product.name.toLowerCase()
                                    try { // try to get image
                                        img = "./img/" + names_lower + ".png"
                                    }
                                    catch {
                                        img = "./img/default.png"
                                    }
                                    /* Create HTML */
                                    var codeString =
                                        `
                                    <li class="flex items-center justify-between py-4">
                                    <div class="flex items-start">
                                        <img class="flex-shrink-0 object-cover w-16 h-16 rounded-lg"
                                            src="` + img + `"/>

                                        <div class="ml-4">
                                            <p class="text-sm">`+ product.name + `</p>

                                            <dl class="mt-1 space-y-1 text-xs text-gray-500">
                                                <div>
                                                    <dt class="inline">Description:</dt>
                                                    <dd class="inline">`+ product.description + `</dd>
                                                </div>
                                                <div>
                                                    <dt class="inline">Quantity:</dt>
                                                    <dd class="inline">`+ quantity + `</dd>
                                                </div>
                                                <div>
                                                <dt class="inline">Price:</dt>
                                                <dd class="inline">$`+ product.price + `</dd>
                                            </div>
                                            </dl>
                                        </div>
                                    </div>

                                    <div class="flex items-center -space-x-4 hover:space-x-1">
                                <button
                                class="z-20 block p-4 text-blue-700 transition-all bg-blue-100 border-2 border-white rounded-full active:bg-blue-50 hover:scale-110 focus:outline-none focus:ring"
                                onclick="redirect(`+ idString + `, ` + storeString+`)" type="button">
                                <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                </svg>
                            </button>
                    
                            <button
                                class="z-30 block p-4 text-red-700 transition-all bg-red-100 border-2 border-white rounded-full hover:scale-110 focus:outline-none focus:ring active:bg-red-50"
                                onclick="deleteItem(`+ id + `)" type="button">
                                <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                            </button>
                            </div>
                                </li>
                                    `
                                    content.innerHTML += codeString
                                }
                            }
                            priceEle.innerHTML = '$' + total_price
                            quantityEle.innerHTML = total_quatity
                            sessionStorage['cartItems'] = cartItems.length
                        }
                    } catch (error) {
                        console.log(error);
                    }
                });
            }
        } catch (error) {
            console.log(error);
        }
    });
}

function checkout() {
    document.getElementById('checkoutSubmit').className = "mt-4 block w-full px-5 py-3 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 hidden"
    document.getElementById('checkoutLoading').className = "mt-4 w-full text-white bg-green-600 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-3 text-center"
    var customerID = sessionStorage.getItem('userId');

    $(async () => {
        var serviceURL = "http://" + serviceHostName + ":8000/api/v1/checkout";
        var obj = {
            "cid": customerID
        }
        try {
            const response =
                await fetch(
                    serviceURL, {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                    , body: JSON.stringify(obj)
                });

            const result = await response.json();

            if (response.status === 200 || response.status === 201) {
                var obj = result.data;
                orderid = Date.now() + Math.random();
                //After checkout finish
                document.getElementById('checkoutLoading').innerHTML = `Checkout Success!`
                document.getElementById('checkoutSuccessAlert').innerHTML = 
                `<div class="flex">
                    <div class="py-1">
                        <svg class="fill-current h-6 w-6 text-teal-500 mr-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z"/>
                        </svg>
                    </div>
                    <div>
                        <p class="font-bold">Your items have been checked out. Your order ID is `+orderid+`.</p>
                        <p class="text-sm">Thank you for using the Smart Checkout System.</p>
                    </div>
                </div>`
                document.getElementById('checkoutSuccessAlert').className = "bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-4 py-3" 
                document.getElementById('content').innerHTML = '<h5 class="text-center">Your cart is empty</h5>'
                var priceEle = document.getElementById('total_price');
                var quantityEle = document.getElementById('total_quantity');
                priceEle.innerHTML = '$0'
                quantityEle.innerHTML = '0'
                document.getElementById('cartItems').className = 'absolute items-center justify-center px-2 py-0\.5 text-2xs font-bold text-white transform translate-x-3 -translate-y-3 bg-gray-600 rounded-full hidden'
                sessionStorage['cartItems'] = 0
            }
        }
        catch (error) {
            console.log(error)
            document.getElementById('checkoutUnsuccessfulAlert').className = "bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
            document.getElementById('checkoutSubmit').className = "mt-4 block w-full px-5 py-3 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700"
            document.getElementById('checkoutLoading').className = "mt-4 w-full text-white bg-green-600 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-3 text-center hidden"
        }
    })


    
}

function deleteItem(id) {
    customerID = sessionStorage['userId']
    productID = id
    obj = {
        "customerID": customerID,
        "productID": productID
    }

    console.log(obj)
    var serviceURL = "http://" + serviceHostName + ":8000/api/v1/remove_from_cart";
    axios.post(serviceURL, json = obj)
        .then(response => {
            console.log(response)
            alert("Item removed from cart successfully!")
            sessionStorage['cartItems'] = sessionStorage['cartItems'] - 1
            window.location.reload();
        });
}

function redirect(id, prod){
    console.log(id)
    console.log(prod)
    result = id + "_" + prod
    window.location = './product_item.html?item=' + result;
}