let heladoAgua = 0.6;
let heladoCrema = 1;
let bombomHeladix = 1.6;
let bombomHeladovich = 1.7;
let bombomHelardo = 1.8;
let potecitoConfites = 2.9;
let poteCuarto = 2.9;

let monto = prompt("Ingrese el monto que tiene disponible:");

if (monto >= 2.9) {
    alert(`Puede comprar Potecito de helado con confites U$S ${potecitoConfites}
        y potecito de 1/4kg U$S ${poteCuarto}`);
    let vuelto = monto - poteCuarto;
    alert(`Su vuelto es U$S ${vuelto}`);
}

else if (monto < 0.6) {
    alert("No tiene suficiente dinero para comprar nada");
}

else if (monto >= 0.6 && monto < 1) {
    alert(`Puede comprar un helado de agua U$S ${heladoAgua}`);
    let vuelto = monto - heladoAgua;
    alert(`Su vuelto es U$S ${vuelto}`);
}

else if (monto >= 1 && monto < 1.6) {
    alert(`Puede comprar un helado de crema U$S ${heladoCrema}`);
    let vuelto = monto - heladoCrema;
    alert(`Su vuelto es U$S ${vuelto}`);
}

else if (monto >= 1.6 && monto < 1.7) {
    alert(`Puede comprar un bombom heladix U$S ${bombomHeladix}`);
    let vuelto = monto - bombomHeladix;
    alert(`Su vuelto es U$S ${vuelto}`);
}

else if (monto >= 1.7 && monto < 1.8) {
    alert(`Puede comprar un bombom heladovich U$S ${bombomHeladovich}`);
    let vuelto = monto - bombomHeladovich;
    alert(`Su vuelto es U$S ${vuelto}`);
}

else if (monto >= 1.8 && monto < 2.9) {
    alert(`Puede comprar un bombom helardo U$S ${bombomHelardo}`);
    let vuelto = monto - bombomHelardo;
    alert(`Su vuelto es U$S ${vuelto}`);
}
