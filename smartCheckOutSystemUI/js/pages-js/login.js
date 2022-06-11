var serviceHostName = "127.0.0.1";

//Initial
function handleLogin(event) {
    event.preventDefault();
    const data = new FormData(event.target);
    const value = Object.fromEntries(data.entries());

    $(async () => {
        var serviceURL = "http://"+ serviceHostName +":8000/api/v1/verifylogin"

        try {
            const response =
                await fetch(
                    serviceURL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(value) });
            ;
            const result = await response.json();
            if (response.status === 200 || response.status === 201) {
                var obj = result.data;
                sessionStorage.setItem('userId', result.data['userid']);
                document.getElementById('loginerror').innerText = ''
                window.location="/smartCheckOutSystemUI/location.html"
                //go to shop now page
            }
            else{
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




