function consultarEdad(edad){
    if(edad >= 18){
        document.write("Puedes pasar");
    }
    else {
        document.write("No puedes pasar");
    }
}
let edad = prompt("Ingrese su edad");
consultarEdad(edad);

let entrada = {
    "Pepe":0,
    "Juan":0,
    "Pedro":1,
    "Gonzalo":2,
    "Summer":2,
    "Savannah":3,

}

function horarioEntrada(entrada){
    for (let i of entrada) {
        if (i == 2){
            document.write("Puedes pasar");
        }   
    }
}

horarioEntrada()