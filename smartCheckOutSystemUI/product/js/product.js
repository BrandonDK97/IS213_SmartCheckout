
function productItemRedirect(itemID, storeID) {
    result = itemID + "_" + storeID
    window.location = '/smartCheckOutSystemUI/product/product_item.html?item=' + result;

}

function loadProductPage() {

    store = sessionStorage['location']

    if (store != null) {
        storeText = 'You are currently shopping at the ' + store
        document.getElementById('shopLocation').innerHTML = storeText
    }

    storeArr = {
        "SMU Store": 400,
        "Tampines Store": 300
    }

    curr = storeArr[store]

    $(async () => {
        var serviceURL = "http://localhost:8000/api/v1/products";
        try {
            const response = await fetch(serviceURL, { method: 'GET' });
            const result = await response.json();
            if (response.ok) {
                console.log(result);
                products = document.getElementById('products')
                products.innerHTML = ""
                for (let i = 0; i < result.length; i++) {
                    storeid = result[i].storeId
                    if (storeid == curr) {
                        id = result[i].id
                        names = result[i].name
                        desc = result[i].description
                        price = result[i].price
                        quantity = result[i].quantity
                        names_lower = names.toLowerCase()
                        try { // try to get image
                            img = "images/" + names_lower + ".png"
                        }
                        catch {
                            img = "images/default.png"
                        }
                        products.innerHTML +=
                            `
                    <div class="card col-4 p-1 container">
                        <img class="card-img-top mx-auto" src="` + img + `"alt="Card image cap">
                        <div class="card-body text-center">
                            <h5 class="card-title">`+ names + `</h5>
                            <p class="card-text">` + desc + `</p>
                            <a onclick='productItemRedirect(`+ id + `,` + storeid + `)' class="btn btn-primary">Add to cart</a>
                        </div>
                    </div>
                    `
                    }
                }
            }
        }
        catch (error) {
            ('There was an error: ' + error);
        }
    })

}

function logOut() {
    sessionStorage.removeItem('userId')
    sessionStorage.removeItem('location')
}



