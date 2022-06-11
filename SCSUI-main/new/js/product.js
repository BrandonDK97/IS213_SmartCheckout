function productItemRedirect(itemID, storeID) {
    result = itemID + "_" + storeID
    window.location = './product_item.html?item=' + result;

}
console.log(sessionStorage)
function loadProductPage() {

    store = sessionStorage['location']

    storeArr = {
        "SMU Store": 400,
        "Tampines Store": 300
    }

    curr = storeArr[store]
    // curr = 400

    document.getElementById('store').innerText = store
    

    $(async () => {
        var serviceURL = "http://localhost:8000/api/v1/products";
        try {
            const response = await fetch(serviceURL, { method: 'GET' });
            const result = await response.json();
            if (response.ok) {
                console.log(result);
                products = document.getElementById('products')
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
                            img = "./img/" + names_lower + ".png"
                        }
                        catch {
                            img = "./img/default.png"
                        }
                        products.innerHTML +=
                            `
                            <a onclick='productItemRedirect(`+ id + `,` + storeid + `)' class="block cursor-pointer transition ease-in-out delay-100 hover:-translate-y-1 hover:scale-105 duration-300">
                                
                            <div class="max-w-sm rounded-xl overflow-hidden shadow-lg ">
                            <img class="object-contain w-96 h-96" src="`+img+`">
                            <div class="px-6 py-4">
                            <div class="font-semibold md:text-sm lg:text-md mb-2">`+names+`</div>
                            <p class="text-gray-700 text-base">
                                <span class="inline-block py-1 text-md font-semibold text-gray-600 mb-2">$`+price+`</span>
                            </p>
                            </div>
                        </div>

                            </a>

                            `
                    }
                }
                document.getElementById('productsLoading').className = 'hidden'
                document.getElementById('products').className = 'grid xs:grid-cols-1 sm:grid-cols-2 mt-8 lg:grid-cols-3 gap-x-4 gap-y-8'
                
            }
        }
        catch (error) {
            ('There was an error: ' + error);
        }
    })

}


