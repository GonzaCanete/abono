let monto = prompt('Ingrese el monto que posee:');

let bill = 2;

let resto = monto - (bill*2);

if (monto < 2){
    alert('No tiene suficiente dinero para comprar el ticket');
}
else if (monto >= bill && monto < bill*2) {
    alert('Puedes comprar solo un ticket');
}
else if (monto >= bill*2 && monto < bill*3) {
    alert('Puedes comprar dos tickets');
}
else {
    alert('Puedes comprar dos tickets y te sobran U$S ' + resto + ' para regalar')
}


