const contendorCLientes = document.querySelector("#contenedorClientes")
const btn_agregar_cliente = document.querySelector("#btnAgregar")
const btn_borrar_cliente = document.querySelector("#borrar_cliente")

btn_agregar_cliente.addEventListener("click", agregarCliente)


const clientesArray = Array(contendorCLientes.children);
console.log(clientesArray)
clientesArray.forEach(Element =>{
    console.log(Element)
})

function agregarCliente(){
    fetch('../../funciones/clientes.py/borrar_cliente', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => {
          console.log(data.mensaje);  // Mostrar el mensaje de éxito
        })
        .catch(error => {
          console.error('Error:', error);
        });
}

fetch('../../JSON/clientes.json')
.then(response => response.json())
.then(data => {
  console.log(data)
   data.forEach(Element => {
        let person =  document.createElement("a")
        person.classList.add("contenedor_persona")
        let contenedor_btns = document.createElement("div")
        contenedor_btns.classList.add("contenedor_btns")
        let btn_delete = document.createElement("button")
        let btn_modify = document.createElement("button")
        btn_delete.classList.add("btn")
        btn_delete.classList.add("delete")
        btn_modify.classList.add("btn")
        btn_modify.classList.add("modify")
        btn_delete.innerHTML = "Borrar"
        btn_modify.innerHTML = "Editar"
        btn_delete.id = Element.id

        contenedor_btns.appendChild(btn_delete)
        contenedor_btns.appendChild(btn_modify)
        person.href = "#"
        person.innerHTML = Element.nombre
        person.appendChild(contenedor_btns)
        contendorCLientes.appendChild(person)
        

   });
})
.catch(error => console.error('Error al obtener los datos:', error));