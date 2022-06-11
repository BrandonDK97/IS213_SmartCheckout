var serviceHostName = "127.0.0.1";

//Initial
function handleLogin(event) {
    document.getElementById('loginerror').innerText = ''
    document.getElementById('loginSubmit').className = 'block w-full px-5 py-3 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-blue-800 hidden'
    document.getElementById('loginLoading').className = 'w-full text-white bg-indigo-600 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-3'
    event.preventDefault();
    const data = new FormData(event.target);
    const value = Object.fromEntries(data.entries());
    console.log(value)

    $(async () => {
        var serviceURL = "http://"+ serviceHostName +":8000/api/v1/verifylogin"

        try {
            const response =
                await fetch(
                    serviceURL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(value) });
            ;
            const result = await response.json();
            if (response.status === 200 || response.status === 201) {
                console.log(result)
                var obj = result.data;
                sessionStorage.setItem('userId', result.data['userid']);
                sessionStorage.setItem('cartItems', 0);
                document.getElementById('loginerror').innerText = ''
                window.location="./location.html"
                //go to shop now page
            }
            else{
                document.getElementById('loginSubmit').className = 'block w-full px-5 py-3 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-blue-800'
                document.getElementById('loginLoading').className = 'w-full text-white bg-indigo-600 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-3 hidden'
                var obj = result.data;
                message = result.message
                document.getElementById('loginerror').innerText = message
            }
        } catch (error) {
            console.log(error.code);
            console.log(error.messsage);

        }
    })
}

const form = document.querySelector('#login');
form.addEventListener('submit', handleLogin);




