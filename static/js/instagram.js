let dropContainer = document.getElementById(`dropContainer`)
let fileInput = document.getElementById(`fileInput`)
dropContainer.ondragover = dropContainer.ondragenter = e => {
    dropContainer.style.border = "2px dashed #47f"
    e.preventDefault();
}
dropContainer.ondragleave = e => {
    dropContainer.style.border = "2px dashed #aaa"
    e.preventDefault();
}
dropContainer.onclick = () => fileInput.click()
dropContainer.ondrop = function(evt) {
    fileInput.files = evt.dataTransfer.files;
    const dT = new DataTransfer();
    Array(...evt.dataTransfer.files).forEach(e => {
        // if (e.type.split("/")[0] == 'image'){
            dT.items.add(e);
        // }
    })
    fileInput.files = dT.files;
    evt.preventDefault();
}

document.querySelector("#addUser").addEventListener("click",e => {
    e.preventDefault();
    let username = document.querySelector("input[name='allUsername']").value
    if(username != ""){
        let badge = document.querySelector("#userNamesBadges").appendChild(
            Object.assign(document.createElement("span"),{className: "badge bg-dark m-1",innerHTML: 
            `${username}`
        })
        )
        
        badge.setAttribute("data-username",username)
        badge.appendChild(Object.assign(document.createElement("span"),
        {className:"dark px-2 removeUserBadge",innerHTML: '<i class="fas fa-times float-end"></i>'})).onclick = e => {
            e.preventDefault();
            e.target.closest(".badge").remove();
        }
        badge.appendChild(Object.assign(document.createElement("input"),
        {style:"display:none",name:"username",value: username})).nodeValue = username

        // par.scrollTo(0,par.scrollHeight);        
        document.querySelector("input[name='allUsername']").value = ""
    }
})

document.querySelector("#submitUsers").addEventListener("click",e => {
    e.preventDefault()
    if(Array(...document.querySelectorAll("span[data-username]")).length)
        e.target.closest("form").submit()
})



document.querySelectorAll('input[name="radioOption"]').forEach(e => {
    e.addEventListener("change", ev => {
        if(ev.target.value == "imageRadio"){
            document.querySelector("#textInput").disabled = true;
            document.querySelector("#fileInput").disabled = false;
        }else{
            document.querySelector("#fileInput").disabled = true;
            document.querySelector("#textInput").disabled = false;
        }
    //   console.log(item);
    });
  });
// console.log(document.querySelectorAll("input[name='radioOption']"))