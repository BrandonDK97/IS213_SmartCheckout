var serviceHostName = "127.0.0.1";

function getCart() {
    /* Definition */
    var customerID = sessionStorage.getItem('userId');
    var content = document.getElementById('content');
    var tableContent = document.getElementById('tableContent');

    var products = [];

    var total_quatity = 0;
    var total_price = 0;

    var priceEle = document.getElementById('total_price');
    var quantityEle = document.getElementById('total_quantity');
    var priceCEle = document.getElementById('priceConfirm');
    var quantityCEle = document.getElementById('quantityConfirm');

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
                                    /* Create HTML */
                                    var codeString =
                                        `
                                        <div class="card rounded-3 mb-4">
                                        <div class="card-body p-4 text-center">
                                            <div class="row d-flex justify-content-between align-items-center">
                                                <div class="col-md-2 col-lg-2 col-xl-2">
                                                    <p class="lead fw-normal mb-2"><b>`+ product.name + `</b></p>
                                                    <p><span class="text-muted">`+ product.description + `</p>
                                                </div>
                                                <div class="col-md-2 col-lg-2 col-xl-2">
                                                    <p class="lead fw-normal mb-2"> Price of product </p>
                                                    <p><span class="text-muted">`+ product.price + `</p>
                                                </div>
                                                <div class="col-md-2 col-lg-2 col-xl-2">
                                                    <p class="lead fw-normal mb-2"> Quantity Selected </p>
                                                    <p><span class="text-muted">`+ quantity + `</p>
                                                </div>
                                                <div class="col-md-2 col-lg-2 col-xl-2 text-center">
                                                    <p class="lead fw-normal mb-2">Total price:</p>
                                                    <p ><span>$`+ item_price + `</p>
                                                </div>
                                                <div class="col-md-2 col-lg-2 col-xl-2 text-center">
                                                    <a name="" id="" class="btn btn-dark" href="../product/product.html" role="button">Edit Quantity</a>
                                                </div>
                                                <div class="col-md-2 col-lg-2 col-xl-2 text-center">
                                                    <button name="" id="" class="btn btn-dark" role="button" onclick="deleteItem(`+ id + `)">Remove item from cart</button>
                                                </div>
                                            </div>
                                        </div>
                                        </div>
                                        `
                                    content.innerHTML += codeString

                                    /*Table content */
                                    var tableString =
                                        `
                                    <tr>
                                        <td>`+ product.name + `</td>
                                        <td>` + product.price + `</td>
                                        <td>` + quantity + `</td>
                                        <td>` + item_price + `</td>
                                    </tr>
                                    `
                                    tableContent.innerHTML += tableString
                                }
                            }
                            priceEle.innerHTML = '$' + total_price;
                            quantityEle.innerHTML = total_quatity;
                            priceCEle.innerHTML = total_price;
                            quantityCEle.innerHTML = total_quatity;
                        }
                    }
                    catch (error) {
                        content.innerHTML = '<h5 class="text-center">Your cart is empty</h5>'
                        console.log(error)
                    }
                })
            }
        } catch (error) {
            console.log(error)
        }
    })

    /* Get cart ID from customer */

}

function checkout() {
    var customerID = sessionStorage.getItem('userId');
    var body = document.getElementById('modal-body');

    var backBtn = document.getElementById('backBtn');
    var successBtn = document.getElementById('successBtn');
    var closeBtn = document.getElementById('closeBtn');


    /* Process payment */
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
                alert("Checkout successful")
                orderid = Date.now() + Math.random();
                successBtn.style.display = 'none';
                closeBtn.style.display = 'none';
                backBtn.style.display = 'block';
                body.innerHTML = "";
                body.innerHTML = `
                <div class="alert alert-success text-center" role="alert">
                    <h4 class="alert-heading">Success!</h4>
                    <p>Your order has been placed successfully!</p>
                    <p>Your payment has been fulfilled by your Stripe account.</p>
                    <hr>
                    <p>Thank you for shopping with us!</p>
                    <p class="mb-0">Your order ID is: ` + orderid + `</p>
                </div>
                `
            }
        }
        catch (error) {
            console.log(error)
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
            window.location.reload();
        });
}


function logOut() {
    sessionStorage.removeItem('userId')
    sessionStorage.removeItem('location')
}
