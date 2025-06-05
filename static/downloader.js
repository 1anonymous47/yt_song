function downloader()
{
    const audiotag = document.getElementById('audiotag')
    audiotag.replaceChildren();
    //const username = document.getElementById('username').value;
    // const password = document.getElementById('password').value;
    const url = document.getElementById('searchurl').value;

    const status = document.getElementById('status')
    status.innerHTML="downloading...."

    fetch('/downloader',{
        method: "POST",
        headers: {
            'Content-Type': 'application/json' // Set Content-Type header for JSON data
        },
        credentials:'include',
        body: JSON.stringify({ 'url':url,'username':username, }),
    })
    .then(res=>res.json())
    .then(data=>{s
        if(data['data']=="success")
        {
            const status = document.getElementById('status')
            status.innerHTML="Success"
            var sound      = document.createElement('audio');
            sound.id       = 'audio-player';
            sound.controls = 'controls';
            sound.src      = data['audiosrc'];
            sound.type     = 'audio/webm';
            var tittle      = document.createElement('h4');
            tittle.innerHTML = data['audiotittle']
            var image = document.createElement('img')
            image.src=data['videosrc']
            var button      = document.createElement('button');
            button.onclick =()=> playlistadder(data['audioid']);
            button.innerText = "add to playlist"
            audiotag.appendChild(tittle);
            audiosrc = data['audiosrc'];
            audiotag.appendChild(image);
            audiotag.appendChild(sound);
            audiotag.appendChild(button);

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
        body: JSON.stringify({ "username":"username",'audioid':audioid }),
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