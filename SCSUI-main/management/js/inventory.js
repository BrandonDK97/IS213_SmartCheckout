// load all stores
function loadStore() {
    // from InventoryAPI, GET product details and display
    console.log("Load store")
    $(async () => {
        var serviceURL = "http://localhost:8000/api/v1/products";
        try {
            const response = await fetch(serviceURL, { method: 'GET' });
            const result = await response.json()
            if (response.ok) {
                console.log("Loading store")
                inventoryTable = document.getElementById("inventoryTable")
                inventoryTable.innerHTML = ""
                for (let i = 0; i < result.length; i++) {
                    id = result[i].id
                    names = result[i].name
                    desc = result[i].description
                    price = result[i].price
                    quantity = result[i].quantity

                    inventoryTable.innerHTML += `<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <td>` + id + `</td> 
                    <td class="px-6 py-4 font-medium text-gray-900 dark:text-white whitespace-nowrap">` + names + `</td>
                    <td>` + desc + `</td>
                    <td> $` + price + `</td>
                    <td>` + quantity + `</td> </tr>`
                }
            }
        } catch (error) {
            alert('There was an error: ' + error);
        } // error
    });
}
// change store view
function changeStore(event) {
    event.preventDefault()
    console.log("Change store")

    // from InventoryAPI, GET specific product details based on store selected
    $(async () => {
        var serviceURL = "http://localhost:8000/api/v1/products";
        try {
            const response = await fetch(serviceURL, { method: 'GET' });
            const result = await response.json()

            if (response.ok) {
                console.log("Changing store")
                const selectedStore = document.getElementById("storeID").value
                // scuffed bc storeId is an int
                if (selectedStore == "SMU") {
                    storeCode = 400
                }
                else if (selectedStore == "Tampines") {
                    storeCode = 300
                }
                inventory = document.getElementById("inventoryTable")
                inventory.innerHTML = ""
                for (let i = 0; i < result.length; i++) {
                    if (result[i].storeId == storeCode) {
                        id = result[i].id
                        names = result[i].name
                        desc = result[i].description
                        price = result[i].price
                        quantity = result[i].quantity

                        inventoryTable.innerHTML += `<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                        <td>` + id + `</td> 
                        <td class="px-6 py-4 font-medium text-gray-900 dark:text-white whitespace-nowrap"
                        >` + names + `</td>
                        <td>` + desc + `</td>
                        <td> $` + price + `</td>
                        <td>` + quantity + `</td> </tr>`
                    }
                }
            }
        } catch (error) {
            alert('There was an error: ' + error);
        }
    });
}

// add and reduce quantity
function addInven() {
    console.log("Adding Stock to Product")
    productId = document.getElementById("addID").value
    newQty = document.getElementById("addQty").value
    console.log(productId)
    console.log(newQty)

    $(async () => {
        var serviceURL = "http://localhost:8000/api/v1/products/add/" + productId + "/" + newQty;
        try {
            const response = await fetch(serviceURL, { method: 'GET' });
            const result = response.status
            console.log(result)
            if (response.ok) {
                loadStore()
                alert("Successfully updated inventory")
            }
            else {
                if (result == 404) {
                    alert("Product not found")
                }
            }
        } catch (error) {
            alert('There was an error: ' + error);
        }
    });
}

function removeInven() {
    console.log("Removing Stock from Product")
    productId = document.getElementById("removeID").value
    newQty = document.getElementById("removeQty").value
    console.log(productId)
    console.log(newQty)

    $(async () => {
        var serviceURL = "http://localhost:8000/api/v1/products/" + productId + "/" + newQty;
        try {
            const response = await fetch(serviceURL, { method: 'GET' });
            const result = response.status
            console.log(result)
            if (response.ok) {
                loadStore()
                alert("Successfully updated inventory")
            }
            else {
                if (result == 404) {
                    alert("Product not found")
                }
            }
        } catch (error) {
            alert('There was an error: ' + error);
        }
    });
}
// search for product by id
function search() {
    console.log("Searching for a product")
    productId = document.getElementById("searchID").value
    console.log(productId)

    $(async () => {
        var serviceURL = "http://localhost:8000/api/v1/products/" + productId;
        try {
            const response = await fetch(serviceURL, { method: 'GET' });
            const status = response.status
            const result = await response.json()
            console.log(status)

            if (response.ok) {
                inventory = document.getElementById("inventoryTable")
                console.log(response)
                id = result.id
                names = result.name
                desc = result.description
                price = result.price
                quantity = result.quantity

                inventory.innerHTML = `<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                <td>` + id + `</td> 
                <td class="px-6 py-4 font-medium text-gray-900 dark:text-white whitespace-nowrap">` + names + `</td>
                <td>` + desc + `</td>
                <td> $` + price + `</td>
                <td>` + quantity + `</td> </tr>`
            }
        }
        catch (error) {
            alert('There was an error: ' + error);
        }
    })
}


const store = document.querySelector('#storeView');
store.addEventListener('change', changeStore);