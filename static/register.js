function register()
{
    const username = document.getElementById('username').value;

    fetch('/register',{
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
            window.alert("Username is invalid")
        }
        else if(res['data']=="already")
        {
            window.alert("Username is already avaialable")
        }
        else{
            window.alert("Success Username added")
        }
    }
    )
}