var serviceHostName = "127.0.0.1";


//GUID
function uuidv4() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

//Initial
var serviceHostName = "127.0.0.1";


//GUID
function uuidv4() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

//Initial
function handleSubmit(event) {
    event.preventDefault();
    document.getElementById('signuperror').innerText = ''
    document.getElementById('signUpSubmit').className = 'block w-full px-5 py-3 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-blue-800 hidden'
    document.getElementById('signUpLoading').className = "w-full text-white bg-indigo-600 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-3 text-center"
    
    const data = new FormData(event.target);
    const value = Object.fromEntries(data.entries());
    value['userid'] = uuidv4();
    $(async () => {
        var serviceURL = "http://" + serviceHostName + ":8000/api/v1/createaccount"
        try {
            const response =
                await fetch(
                    serviceURL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(value) });
            ;
            const result = await response.json();

            if (response.status === 200 || response.status === 201) {
                var obj = result.data;
                //Change UI
                document.getElementById('paymentContainer').className = "max-w-screen-xl px-4 py-16 mx-auto sm:px-6 lg:px-8";
                document.getElementById('initialContainer').className = "max-w-screen-xl px-4 py-16 mx-auto sm:px-6 lg:px-8 hidden";
                //Add payment details
                sessionStorage.setItem('userId', obj.userid);
            }
            else if (response.status === 400) {
                var obj = result.data;
                message = result.message
                document.getElementById('signuperror').innerText = message
                document.getElementById('signUpSubmit').className = 'block w-full px-5 py-3 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-blue-800'
                document.getElementById('signUpLoading').className = "w-full text-white bg-indigo-600 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-3 text-center hidden"
            }
        } catch (error) {
            console.log(error.code);
            console.log(error.messsage);

        }
    })
}


const form = document.querySelector('#initial');
form.addEventListener('submit', handleSubmit);

//Initial
function handlePayment(event) {
    document.getElementById('paymenterror').innerText = ''
    document.getElementById('addPaymentSubmit').className = 'block w-full px-5 py-3 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-blue-800 hidden'
    document.getElementById('addPaymentLoading').className = "w-full text-white bg-indigo-600 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-3 text-center"
    event.preventDefault();
    const data = new FormData(event.target);
    const value = Object.fromEntries(data.entries());
    postBody = {
        "userid": sessionStorage.getItem('userId'),
        "card": {
            "number": value['number'],
            "exp_month": parseInt(value['Expiry Month']),
            "exp_year": parseInt(value['Expiry Year']),
            "cvc": value['CVC']
        }
    }
    console.log(postBody)

    $(async () => {
        const rawResponse = await fetch('http://'+ serviceHostName +':8000/api/v1/addpaymentdetails', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(postBody)
        });
        const content = await rawResponse.json();
        code = content.code
        if (code === 500){
            message = content.data.stripe_result.error
            document.getElementById('addPaymentSubmit').className = 'block w-full px-5 py-3 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-blue-800'
            document.getElementById('addPaymentLoading').className = "w-full text-white bg-indigo-600 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-3 text-center hidden"
            if(message){
                message = message.split(':')
                document.getElementById('paymenterror').innerText = message[1]
            }
            else{
                document.getElementById('paymenterror').innerText = "Error while adding payment details"
            }        
        }
        else{
            document.getElementById('paymenterror').innerText = ''
            window.location="./location.html";
        }
        
        console.log(content);
    })();
}

const secondForm = document.querySelector('#payment');
secondForm.addEventListener('submit', handlePayment);
