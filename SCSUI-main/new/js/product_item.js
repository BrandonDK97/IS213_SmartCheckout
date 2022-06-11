var serviceHostName = "127.0.0.1";
const urlParams = new URLSearchParams(window.location.search);
const myParam = urlParams.get('item');

itemID = myParam.split("_")
storeID = itemID[1]
itemID = itemID[0]
document.getElementById('productImage').className = "hidden"
document.getElementById('imageLoading').className = "w-96 h-96 flex justify-center items-center"
$(async () => {
    var serviceURL = "http://" + serviceHostName + ":8000/api/v1/products";
    try {
        const response = await fetch(serviceURL, { method: 'GET' });
        const result = await response.json();
        if (response.ok) {
            console.log(result);
            for (let i = 0; i < result.length; i++) {
                id = result[i].id
                names = result[i].name
                desc = result[i].description
                price = result[i].price
                quantity = result[i].quantity
                names_lower = names.toLowerCase()
                try { // try to get image
                    img = "./img/" + names_lower + ".png"
                }
                catch {
                    img = "./img/default.png"
                }
                console.log(img)
                document.getElementById('productImage').className = 'object-cover rounded-xl'
                document.getElementById('productImage').src = img
                document.getElementById('imageLoading').className = "w-96 h-96 flex justify-center items-center hidden"
                document.getElementById('productPrice').innerHTML = `$`+price
                storeid = result[i].storeId

                if ((id == parseInt(itemID)) && (storeid == parseInt(storeID))) {
                    item = result[i]
                    document.getElementById('prodName').innerText = names
                    document.getElementById('prodDesc').innerText = desc
                    console.log(sessionStorage)
                    break
                }
            }
        }
    }
    catch (error) {
        ('There was an error: ' + error);
    }
})

function addToCart() {
    document.getElementById('addToCart').className = "block px-5 py-3 ml-3 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-500 hidden"
    document.getElementById('addingLoading').className = "block px-5 py-3 ml-3 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-500"
    userID = sessionStorage['userId']
    qty = document.getElementById('quantity').value

    url = "http://" + serviceHostName + ":8000/api/v1/add_to_cart"

    postBody = {
        "productID": parseInt(itemID),
        "quantity": parseInt(qty),
        "customerID": userID,
        "storeID": parseInt(storeID)
    }
    console.log(postBody)
    axios.post(url, json = postBody)
        .then(response => {
            console.log(response)
            sessionStorage['cartItems'] = Number(sessionStorage['cartItems']) + 1
            window.location = "./product.html"
        });
        
    
}