document.addEventListener('DOMContentLoaded',() => {
    var socket = io();


    socket.on('message', data =>{
       // const p = document.createElement('div');
        const p = document.createElement('p');
        const span_username= document.createElement('span');
        const br= document.createElement('br');
        span_username.innerHTML=data.username;
        p.innerHTML=  Object.keys(data[msg]);
       //document.getElementById("display-message-section").innerHTML =data.msg;
        document.getElementById("display-message-section").append(p);
    });
   
    socket.on('some-event', data =>{
        console.log(data);
    });

    document.getElementById("send_message").addEventListener('click', () => {
        console.log(`${username}`);
        socket.send({username: username,msg: document.getElementById("user_message").value
        //socket.send({ 'msg':document.querySelector('#user_message').value
                    });
    });
})