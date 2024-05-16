const formQr = document.getElementById("formQr");
const inputDataQr = document.getElementById("dataQr");
var clickSubmit = false;

formQr.addEventListener("submit", (event) => {
  event.preventDefault();
  if (clickSubmit) {
    console.log("Ya ha creado, Esperar...");
    infoAutoClose("Agregando, Esperar...", 2500);
    return;
  }
  infoAutoClose("Agregando, Esperar...", 3000);
  clickSubmit = true;
  const dataQr = inputDataQr.value.trim();
  // const reasonSinSaltos = textAreaReason.value.trim().replace(/\n/g, ' ');
  if (dataQr == "") {
    console.log("Verificar QR");
    Swal.fire({
      icon: "error",
      title: "Verificar",
      text: "QR Vacío!!"
    });
    clickSubmit = false;
    return;
  }
  console.log('fomrQR', formQr)
  const formData = new FormData(formQr);
  formData.forEach(function(value, key){
        console.log(key, value);
    });
  // return
  fetch(`/api/create_comprobante`, {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        // Si la respuesta no está en el rango de 200-299
        console.log(response, response.json());
        throw new Error(`La solicitud no fue exitosa`);
      }
      return response.json;
    })
    .then((responseJson) => {
      console.log(responseJson, responseJson.ok, responseJson.message);
      // Notificación
      // buscar la forma de q solo se actualice la tabla y no toda la página y se limpie el input QR
      // SIMULAR UN POS.
      // Se puede poner un spinner mientras se agrega el comprobante
      alert('Agregado')
      inputDataQr.value = "";
      location.reload()
      clickSubmit = false
    })
    .catch((error) => {
      console.error(error);
      Swal.fire("No se creo!", `${error}`, "error");
      clickSubmit = false
    })
});
