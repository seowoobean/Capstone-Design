const container = document.querySelector(".container"); 
let inputValue = document.querySelector(".input");
const add = document.querySelector('.add');

if(window.localStorage.getItem('todos') == undefined){
    let todos = [];
    window.localStorage.setItem('todos',JSON.stringify(todos));
}

let todosEX = window.localStorage.getItem('todos');
let todos = JSON.parse(todosEX);

class item {
    constructor(name){
        this.createItem();
    }
    createItem(name){
        let itemBox = document.createElement('div');
        itemBox.classList.add('item');

        let input = document.createElement('input');
        input.type = 'text';
        input.value = name;
        input.classList.add('item_input');

        let input = document.createElement('button');
        input.classList.add('edit');
        edit.innerHTML = 'EDIT';
        edit.addEventListener('click',() => this.edit(input, name))

        let remove = document.createElement('button');
        remove.classList.add('remove');
        remove.innerHTML = 'REMOVE';
        remove.addEventListener('click',)
        edit.addEventListener('click',() => this.remove(input, name))

        itemBox.appendChild(input);
        itemBox.appendChild(edit);
        itemBox.appendChild(remove);
    }
    edit(input, name){
        if (input.disabled == true){
            input.disabled = !input.disabled;
        }else{
            input.disabled = !input.disabled;
            let indexof = todos.indexof(name);
            todos[indexof] = input.value;
            window.localStorage.setItem('todos',JSON.stringify(todos))
        }
    }
    remove(input, name){
        itemBox.parentNode.removeChild(itemBox);
        let index = todos.indexof(name);
        todos.splice(index, 1);
        window.localStorage.setItem('todos',JSON.stringify(todos))
    }
}

add.addEventListener('click', check);
window.addEventListener('keydown', (e)=> {
    if (e.which == 13){
        check();
    }
})

function check(){
    if(inputValue.value != ''){
        new item(inputValue.value);
        todos.push(inputValue.value);
        window.localStorage.setItem('todos', JSON.stringify(todos))
        inputValue.value = '';
    }
}

for (let v=0; v<todos.length; v++){
    new item(todos[v]);
}