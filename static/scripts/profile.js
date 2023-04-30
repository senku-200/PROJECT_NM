popup_initiliser = document.querySelector('.popup_initiliser');
container = document.querySelector('.container');
popup = document.querySelector('.popup');
popup_exit = document.querySelector('.exit img');
image_getter_exit = document.querySelector('.get_image_exit img');
change = document.querySelector('.change');
get_image = document.querySelector('.get_image');

popup_initiliser.onclick = () =>{
    popup.classList.add('activate_popup')
    container.classList.add('activate_container')
}   
popup_exit.onclick = () =>{
    popup.classList.remove('activate_popup')
    container.classList.remove('activate_container')
}
change.onclick = () =>{
    popup.classList.remove('activate_popup')
    get_image.classList.add('activate_get_image')
}
image_getter_exit.onclick = () =>{
    get_image.classList.remove('activate_get_image')
    popup.classList.add('activate_popup')
}