// load all products
function getAllProducts() {
    console.log("Gets all products")
    $(async () => {
        var serviceURL = "http://localhost:8000/api/v1/products";
        try {
            const response = await fetch(serviceURL, { method: 'GET' });
            const result = await response.json()
            if (response.ok) {
                console.log("hello2")
                productTable = document.getElementById("productTable")
                productTable.innerHTML = ""
                for (let i = 0; i < result.length; i++) {
                    id = result[i].id
                    names = result[i].name
                    desc = result[i].description
                    price = result[i].price
                    storeID = result[i].storeId

                    productTable.innerHTML += `<tr id="` + i + `"  class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                        <td>` + id + `</td> 
                        <td class="px-6 py-4 font-medium text-gray-900 dark:text-white whitespace-nowrap">` + names + `</td>
                        <td>` + desc + `</td>
                        <td>$` + price + `</td>
                        <td>` + storeID + `</td>
                        <td><button type="button" class="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2 text-center mr-2 mb-2" onclick="generateQR(`+ i + `)">Show QR Code</button></td>
                        </tr>`
                }
            }
        } catch (error) {
            ('There was an error: ' + error);
        } // error
    });
}


function createProduct() {
    console.log("Creates a product")
    let productName = document.getElementById("addName").value
    let productPrice = parseInt(document.getElementById("addPrice").value)
    let productDesc = document.getElementById("addDesc").value
    let productQty = parseInt(document.getElementById("addQty").value)
    let productStore = parseInt(document.getElementById("addId").value)

    data = { "Name": productName, "Price": productPrice, "Description": productDesc, "Quantity": productQty, "StoreId": productStore }
    console.log(data)
    $(async () => {
        serviceURL = "http://localhost:8000/api/v1/products/"
        try {
            const response = await fetch(serviceURL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
            const result = response.status;
            console.log(result)
            console.log(JSON.stringify(data))
            if (response.ok) {
                getAllProducts();
                alert("Product Created!")
            }
            else {
                alert("Failed to create!")
            }
        } catch (error) {
            console.log('There was an error: ' + result);
         } // error
    })
}


const addBtn = document.querySelector("#addBtn");
addBtn.addEventListener('click', createProduct);

function removeProduct() {
    console.log("Removes a product")
    let productID = parseInt(document.getElementById("removeID").value)

    $(async () => {
        serviceURL = "http://localhost:8000/api/v1/products/" + productID
        try {
            const response = await fetch(serviceURL, { method: 'DELETE' });
            const result = response.status;
            console.log(result)
            if (response.ok) {
                getAllProducts();
                alert("Product deleted")
            }
            else {
                alert("Product not deleted!")
            }
        } catch (error) {
            console.log('There was an error: ' + result);
        } // error
    })
}
const removeBtn = document.querySelector('#deleteBtn');
removeBtn.addEventListener('click', removeProduct);


function generateQR(id) {
    // add QR Code Function here
    console.log("Generate QR Code")
    tr = document.getElementById(id)
    productID = tr.cells[0].innerHTML
    storeID = tr.cells[4].innerHTML
    document.getElementById("qrcode").innerHTML = ""
    str = "esdstore_" + productID + "_" + storeID + "";
    console.log(str);
    const makeQR = (str) => {
        let qrcodeContainer = document.getElementById("qrcode");
        qrcodeContainer.innerHTML = "";
        new QRious({
            element: qrcodeContainer,
            value: str,
            size: 250,
            padding: 50,
        }); // generate QR code in canvas
        downloadQR(); // function to download the image
    }

    
    function downloadQR() {
        console.log("Downloading QR")
        var link = document.createElement('a');
        link.download = productID + storeID + '.png';
        link.href = document.getElementById('qrcode').toDataURL()
        link.click();
    }

    makeQR(str)
}

