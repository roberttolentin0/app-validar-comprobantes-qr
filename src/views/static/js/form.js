const formQr = document.getElementById("formQr");
const inputDataQr = document.getElementById("dataQr");
const formDataComprobante = document.getElementById("formDataComprobante");
var clickSubmit = false;

formQr.addEventListener("submit", (event) => {
  event.preventDefault();
  if (clickSubmit) {
    console.log("Ya ha creado, Esperar...");
    infoAutoClose("Agregando, Esperar...", 2500);
    return;
  }
  infoAutoClose("Agregando, Esperar...");
  clickSubmit = true;
  const dataQr = inputDataQr.value.trim();
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
      return response.json();
    })
    .then(responseJson => {
      const comprobante = responseJson.new_comprobante
      addComprobanteToTable(comprobante)
      successAutoClose("Comprobante agregado", 500);
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
    .finally(() => inputDataQr.value = "");
});

formDataComprobante.addEventListener("submit", (event) => {
  event.preventDefault();
  if (clickSubmit) {
    infoAutoClose("Agregando, Esperar...", 2500);
    return;
  }
  infoAutoClose("Agregando, Esperar...");
  clickSubmit = true;
  const formData = new FormData(formDataComprobante);
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
      return response.json();
    })
    .then(responseJson => {
      const comprobante = responseJson.new_comprobante
      addComprobanteToTable(comprobante)
      successAutoClose("Comprobante agregado", 500);
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
    .finally(() => inputDataQr.value = "");
});