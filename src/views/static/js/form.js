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
    .then(response => {
      if (!response.ok) {
        // Si la respuesta no está en el rango de 200-299
        return response.json().then(errorData => {
          const error = new Error('Respuesta no satisfactoria');
          error.data = errorData;
          throw error;
        })
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
      let errorMessage;
      if (error.data){
        // Error del servidor
        errorMessage = `Error del servidor: ${error.data.message || JSON.stringify(error.data)}`;
      } else {
        // Error de red u otro tipo de error
        errorMessage = `Error: ${error.message}`;
      }
      console.error(errorMessage);
      Swal.fire("No se creo!", errorMessage, "error");
      clickSubmit = false;
    })
});
