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
                document.getElementById('initial').style.display = "none";
                document.getElementById('payment').style.display = "";
                //Add payment details
                sessionStorage.setItem('userId', obj.userid);
            }
            else if (response.status === 400) {
                var obj = result.data;
                message = result.message
                document.getElementById('signuperror').innerText = message
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
            if(message){
                message = message.split(':')
                document.getElementById('addpaymenterror').innerText = message[1]
            }
            else{
                document.getElementById('addpaymenterror').innerText = "Error while adding payment details"
            }        
        }
        else{
            document.getElementById('addpaymenterror').innerText = ''
            window.location="/smartCheckOutSystemUI/location.html";
        }
        
        console.log(content);
    })();
}

const secondForm = document.querySelector('#payment');
secondForm.addEventListener('submit', handlePayment);




