let songscount;
let currentsong=0;
let key;
let value;
var audio;
var slider = document.createElement('input');
slider.type = "range";
var durationttime;
var currentduration;
var songs;
function playlistadder()
{
    const username = document.getElementById('username').value;
    fetch('http://127.0.0.1:5000/playlistgetter',{
        method: "POST",
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify({ "username":username}),
    })
    .then(res=>res.json())
    .then(data=>{
        if(data.data=="nouser")
        {
            window.alert("Invalid Username")
            return 0;
        }
        if(data.data=="noplay")
        {
            window.alert("Empty Playlist")
            return 0;
        }
        key =  Object.keys(data)
        value =  Object.values(data)
        songscount = key.length;
        // for (const [key, value] of Object.entries(data)) {
        //     var sound      = document.createElement('audio');
        //     sound.id       = 'audio-player';
        //     sound.controls = 'controls';
        //     sound.src      = 'static/audios/'+value[1];
        //     sound.type     = 'audio/webm';
        //     var tittle      = document.createElement('h4');
        //     tittle.innerHTML = value[0];
        //     audiotag.appendChild(tittle);
        //     audiotag.appendChild(sound);
        //   }
        songs = document.getElementById('songs')
        for (let index = 0; index < key.length; index++) {
            const list = document.createElement('button')
            list.innerHTML = value[index][0]
            list.onclick =()=> player(index)
            var mybr = document.createElement('br');
            songs.appendChild(mybr);
            songs.appendChild(list)
        }
        
        audio = new Audio('static/audios/'+value[currentsong][2])
        reuser(currentsong)
    })
}
function changer(data)
{

    if(data==0)
    {
        if(currentsong==0)
        {
            window.alert("First of playlist")
            return 0;
        }
        else
        {
            currentsong = currentsong -1;
        }
    }
    else
    {
        if(currentsong==key.length-1)
        {
            window.alert("Last of playlist")
            return 0;
        }
        else
        {
            currentsong = currentsong +1;
        }
    }
    audio.pause()
    audio = new Audio('static/audios/'+value[currentsong][2])
    
    reuser(currentsong)
    audio.play()
    


}
function play()
{
    
    audio.play()
}
function pause()
{
    audio.pause()
}

function reuser(currentsong)
{
    const audiotag = document.getElementById('audiotag')
    audiotag.replaceChildren();
    const image = document.createElement('img');
    image.id='imageid'
    image.src=value[currentsong][1]
    console.log(value[currentsong][1])
    audiotag.appendChild(image);
    durationttime = document.createElement('h4')
    currentduration  =document.createElement('h4')
    audio.addEventListener("loadedmetadata",()=>
    {
        slider.max=audio.duration; 
        durationttime.innerHTML = "Song Duration : " +audio.duration;
        
    })
    audio.ontimeupdate = ()=>{
        slider.value = audio.currentTime;
        console.log(audio.currentTime)
        currentduration.innerHTML = "Song Timeing : "+audio.currentTime;

    }
    slider.addEventListener("input",()=>
    {
        audio.currentTime = slider.value;
    })
    slider.min=0;
    slider.value=0;
    audiotag.appendChild(currentduration)
    audiotag.appendChild(durationttime)
    audiotag.appendChild(slider)
}
function player(data)
{
    audio.pause()
    audio = new Audio('static/audios/'+value[data][2])
    reuser(data)
    audio.play()
}



