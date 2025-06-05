function login()
{
    const username = document.getElementById('username').value;

    fetch('/login',{
        method:'POST',
        headers:{
            'Content-type':'application/json'
        },
        body:JSON.stringify({'username':username})
    })
    .then(n=>n.json())
    .then(res=>
    {
        if(res['data']=="fail")
        {
            window.alert("Invaid username")
        }
        else
        {
            window.location.href=res['redirect'];
        }
    }
    )
}