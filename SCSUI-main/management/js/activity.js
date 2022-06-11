function getAllActivity() {

    activityTable = document.getElementById('activityTable');

    $(async () => {
        var serviceURL = "http://127.0.0.1:8000/api/v1/listallpayments";
        try {
            const response = await fetch(serviceURL, { method: 'GET' });
            const result = await response.json();
            if (response.ok) {
                transactions = result['data']
                for (let i = 0; i < transactions.length; i++) {
                    transaction = transactions[i]
                    amount = transaction['amount'] / 10
                    customerID = transaction['name']
                    date =   convertDate(transaction['date'])
                    card4 = transaction['last4']
                    paymentType = transaction['paymentType']

                    tempCode =
                        `
                    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                        <td class="px-6 py-4 font-medium text-gray-900 dark:text-white whitespace-nowrap">`+ date + `</td>
                        <td>`+ customerID + `</td>
                        <td>`+ paymentType + `</td>
                        <td>`+ "**** **** **** " + card4 + `</td>
                        <td>$`+ amount + `.00</td>
                    </tr>
                    `
                    activityTable.innerHTML += tempCode
                }
            }
        }
        catch (error) {
            ('There was an error: ' + error);
        }
    })
}

function convertDate(datetime) {
    const milliseconds = datetime * 1000 // 1575909015000
    
    const dateObject = new Date(milliseconds)
    
    const humanDateFormat = dateObject.toLocaleString() //2019-12-9 10:30:15

    return humanDateFormat;
}