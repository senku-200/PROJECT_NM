
next = document.querySelector('.next');
pr1 = document.querySelector('.prj1');
pr2 = document.querySelector('.prj2');
next = document.querySelector('.next');
previous = document.querySelector('.previous');
next.onclick = () =>{
    pr1.classList.add('deactivate')
    pr2.classList.add('activate')
    previous.classList.add('btn-activate')
    next.classList.add('btn-deactivate')
}
previous.onclick = () =>{
    pr1.classList.remove('deactivate')
    pr2.classList.remove('activate')
    previous.classList.remove('btn-activate')
    next.classList.remove('btn-deactivate')
}
