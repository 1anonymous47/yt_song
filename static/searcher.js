function searcher()
{
    const list = document.getElementById('list')
    list.replaceChildren()
    window.alert("Wait until before pressing any other further request you will receive response in short time")
    const searchurl = document.getElementById('searchurl').value;
    fetch('/searcher',{
        method:"POST",
        headers:{
            'Content-Type':'application/json'
        },
        credentials:'include',
        body:JSON.stringify({'searchid':searchurl})
    })
    .then(res=>res.json())
    .then(data=>{
        if(data['data']!=="fail")
        {
            adder(data)
        }
        else{
            window.alert("No video found use manual link provider or check the video id correctly")
        }
    })
}


function adder(data)
{
    window.alert("Due to thinking about your device specs we just limits our search results sont worry you will get the expected results beore that limits")
    const list = document.getElementById('list')
    //data.data.length
    for (let i = 0; i < 5; i++) {
        const video = document.createElement('iframe')
        const button = document.createElement('button')
        video.src="https://www.youtube.com/embed/"+data.data[i]
        video.width = 420;
        video.height = 315;
        button.onclick =()=> downloader(data.data[i]);
        button.innerText = 1 + "ADD";
        list.appendChild(video)
        list.appendChild(button)
    }
}
function downloader(element)
{
    //const username = document.getElementById('username').value;
    const url = "https://www.youtube.com/watch?v="+element;

    fetch('/downloader',{
        method: "POST",
        headers: {
            'Content-Type': 'application/json' // Set Content-Type header for JSON data
        },
        credentials:'include',
        body: JSON.stringify({ 'url':url,'username':username, }),
    })
    .then(res=>res.json())
    .then(data=>{
        if(data['data']=="success")
        {
            playlistadder(data['audioid'])

        }
        else if (data['data']=="fail") 
        {
            window.alert("Invalid username")
            const status = document.getElementById('status')
            status.innerHTML="Invalid username"
        } 
        else
        {
            const status = document.getElementById('status')
            status.innerHTML="Invalid Url"
        }
    }
    );
}
function playlistadder(audioid)
{

    //const username = document.getElementById('username').value;
    fetch('/playlistadder',{
        method: "POST",
        headers: {
            'Content-Type': 'application/json' 
        },
        credentials:'include',
        body: JSON.stringify({ "username":username,'audioid':audioid }),
    })
    .then(res=>res.json())
    .then(data=>{
        if(data['data']=="success")
        {
            window.alert("Song added")
        }
        else{
            window.alert("Song is already added")
        }
    })
}