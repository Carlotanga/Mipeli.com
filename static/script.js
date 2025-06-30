// static/script.js

// Espera a que el documento esté listo
document.addEventListener("DOMContentLoaded", async () => {
  const lista = document.getElementById("lista-productos");

  try {
    // Llama a la API para obtener los productos
    const respuesta = await fetch("/productos");
    const productos = await respuesta.json();

    // Por cada carro, crea un elemento de lista
    productos.forEach((producto) => {
      const li = document.createElement("li");
      li.textContent = `ID: ${producto.id}, Marca: ${producto.marca}, Nombre: ${producto.nombre}, Cantidad:${producto.cantidad}, Fecha_caducidad: ${producto.fecha_caducidad}`;
      lista.appendChild(li);
    });
  } catch (error) {
    console.error("Error al cargar los Productos:", error);
    lista.innerHTML = "<li>Error al cargar los datos.</li>";
  }
});

//obtener los datos ingresados:
document.addEventListener("DOMContentLoaded", () => {
  const lista = document.getElementById("lista-productos");
  const form = document.querySelector("form");

  // Cargar los productos existentes al iniciar
  fetch("/productos")
    .then((res) => res.json())
    .then((productos) => {
      productos.forEach((producto) => {
        const li = document.createElement("li");
        li.textContent = `ID: ${nuevoProductoproducto.id}, Marca: ${producto.marca}, Nombre: ${producto.nombre}, Cantidad:${producto.cantidad}, Fecha_caducidad: ${producto.fecha_caducidad}`;
        lista.appendChild(li);
      });
    })
    .catch((err) => console.error("Error al cargar productos:", err));

  // Manejar el formulario
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // Evita recarga auto

    const id = document.getElementById("fname").value; //trae el id
    const marca = document.getElementById("lname").value; //trae la marca
    const nombre = document.getElementById("mname").value; //trae el nombre
    const cantidad = parseInt(document.getElementById("cname").value); //trae la cantidad
    const fecha_caducidad = document.getElementById("fcname").value; //trae la fecha de caducidad

    console.log("id:", id);
    console.log("marca:", marca);
    console.log("nombre:", nombre);
    console.log("cantidad:", cantidad);
    console.log("fecha:", fecha_caducidad);

    //por si las moscas
    if (!id || !marca || !nombre || isNaN(cantidad) || !fecha_caducidad) {
      alert("Completa todos los campos correctamente.");
      return;
    }

    const nuevoProducto = { id, marca, nombre, cantidad, fecha_caducidad };

    try {
      const res = await fetch("/productos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(nuevoProducto),
      });

      //verif correcto
      if (res.ok) {
        const li = document.createElement("li");
        li.textContent = `ID: ${nuevoProducto.id}, Marca: ${nuevoProducto.marca}, Nombre: ${nuevoProducto.nombre}, Cantidad: ${nuevoProducto.cantidad}, Fecha_caducidad: ${nuevoProducto.fecha_caducidad}`;
        lista.appendChild(li); //crear un nuevo elemento de la lista
        form.reset(); //limpiar el form
      } else {
        alert("Error al agregar el producto."); //error
      }
    } catch (err) {
      console.error("Error al enviar datos:", err);
    }
  });
});
