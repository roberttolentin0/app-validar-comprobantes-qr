const loading = document.getElementById("jsLoading");
const dataTablesOptions = {
  responsive: true,
  order: [[0, "desc"]],
  autoWidth: false,
  orderCellsTop: true, // Para que el ordenar solo afecte la primera fila
  // language: {
  //   entries: {
  //     _: "Entradas",
  //     1: "Entrada",
  //   },
  //   search: "Buscar: ",
  // },
  language: {
    "url": "https://cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json"
  },
  layout: {
    topStart: {
      search: {
        placeholder: "Ingresa busqueda",
      },
    },
    topEnd: "info",
    bottomStart: {
      paging: {
        numbers: 5,
      },
    },
    bottomEnd: "pageLength",
    bottom2End: "buttons",
  },
  buttons: [
    {
      extend: "excel",
      text: "Exportar",
      exportOptions: {
        modifier: {
          page: "current",
        },
      },
    },
    {
      extend: "print",
      text: "Print",
    },
  ],
  pageLength: 100,
  initComplete: function () {
    // Búsqueda por columnas
    this.api()
      .columns()
      .every(function () {
        var that = this;

        // Aplica la búsqueda al input de cada columna
        $('input', this.header()).on('keyup change clear', function () {
          if (that.search() !== this.value) {
            that.search(this.value).draw();
          }
        });
      });
  },
};

const tablaComprobantes = new DataTable(
  "#tablaComprobantes ",
  dataTablesOptions
).columns
  .adjust()
  .responsive.recalc();

function addComprobanteToTable(comprobante) {
  tablaComprobantes.row
    .add([
      `<span style="font-size: 0.7rem"}>${comprobante.id}</span>`,
      comprobante.created_at,
      comprobante.ruc,
      comprobante.fecha_emision,
      comprobante.serie,
      comprobante.numero,
      comprobante.monto,
      comprobante.tipo_comprobante,
      renderRowStatus(comprobante.estado_comprobante),
      renderRowStatus(comprobante.estado_ruc),
      renderRowStatus(comprobante.cod_domiciliaria_ruc),
      `<span style="font-size: 0.7rem"}>${comprobante.observaciones || ''}</span>`,
      renderRowOptions(comprobante),
    ])
    .draw();
}

/** Agregar filas */
comprobantes.forEach((comprobante) => addComprobanteToTable(comprobante));

function renderRowStatus(status) {
  const colorStatus = {
    "NO EXISTE": "badge text-bg-secondary",
    ACEPTADO: "badge badge-success",
    ANULADO: "badge text-bg-danger",
    // EstadoRuc
    ACTIVO: "badge badge-success",
    // ConDomRuc
    HABIDO: "badge badge-success",
    default: "badge text-bg-secondary",
  };
  return `<span class='px-2 py-1 ${
    colorStatus[status] || colorStatus["default"]
  }'>${status}</span>`;
}

function renderRowOptions(comprobante) {
  const observaciones = comprobante.observaciones || "Sin Observaciones";
  const buttonValidar = `
        <button onclick="validar(${comprobante.id})" class="btn btn-light col-3 col-sm-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        </button>
    `;
  const buttonEliminar = `
        <button onclick="eliminar(${comprobante.id})" class="btn btn-light col-3 col-sm-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fca5a5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
        </button>
    `;
  const buttonDetails = `
        <button onclick="showDetails('${observaciones}')" class="btn btn-light col-3 col-sm-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" style="width:100%;height:100%;transform:translate3d(0,0,0);content-visibility:visible" viewBox="0 0 500 500"><defs><clipPath id="a"><path d="M0 0h500v500H0z"/></clipPath><clipPath id="c"><path d="M0 0h500v500H0z"/></clipPath><clipPath id="b"><path d="M0 0h500v500H0z"/></clipPath></defs><g clip-path="url(#a)"><g clip-path="url(#b)" style="display:block"><g class="primary design" style="display:none"><path fill="none" class="primary"/></g><g class="primary design" style="display:none"><path class="primary"/><path fill="none" class="primary"/></g><g class="primary design" style="display:none"><path fill="#4a90e2" d="m427.222 397.726-75.488-75.488c21.017-27.245 33.661-61.281 33.661-98.234 0-89.152-72.488-161.432-161.432-161.432-88.945 0-161.433 72.28-161.433 161.432 0 88.944 72.488 161.433 161.433 161.433 37.014 0 71.071-12.686 98.338-33.745l75.467 75.488a20.773 20.773 0 0 0 14.727 6.103 20.773 20.773 0 0 0 14.727-6.103c8.144-8.145 8.144-21.31 0-29.454zm-203.26-293.494c66.032 0 119.773 53.741 119.773 119.772s-53.741 119.773-119.772 119.773c-66.032 0-119.773-53.742-119.773-119.773 0-66.03 53.741-119.772 119.773-119.772z" class="primary"/></g><g class="primary design" style="display:block"><path fill="#4a90e2" d="m427.222 397.726-75.488-75.488c21.017-27.245 33.661-61.281 33.661-98.234 0-89.152-72.488-161.432-161.432-161.432-88.945 0-161.433 72.28-161.433 161.432 0 88.944 72.488 161.433 161.433 161.433 37.014 0 71.071-12.686 98.338-33.745l75.467 75.488a20.773 20.773 0 0 0 14.727 6.103 20.773 20.773 0 0 0 14.727-6.103c8.144-8.145 8.144-21.31 0-29.454zm-203.26-293.494c66.032 0 119.773 53.741 119.773 119.772s-53.741 119.773-119.772 119.773c-66.032 0-119.773-53.742-119.773-119.773 0-66.03 53.741-119.772 119.773-119.772z" class="primary"/></g></g><g clip-path="url(#c)" style="display:none"><g class="primary design" style="display:none"><path fill="none" class="primary"/></g><g class="primary design" style="display:none"><path class="primary"/><path fill="none" class="primary"/></g><g class="primary design" style="display:none"><path class="primary"/></g></g></g></svg>
        </button>
    `;

  return `
          <div class="row">
              ${buttonValidar}${buttonEliminar}
          </div>
          `;
}

function showDetails(observaciones) {
  Swal.fire({
    title: "Observaciones",
    text: observaciones,
    icon: "info",
  });
}

function eliminar(id) {
  Swal.fire({
    title: "Eliminar comprobante",
    text: "¿Está seguro que desea eliminar este comprobante?",
    icon: "question",
    showCancelButton: true,
    confirmButtonColor: "#fca5a5",
    cancelButtonColor: "#adb5bd",
    confirmButtonText: "Eliminar",
  }).then((result) => {
    if (result.isConfirmed) {
      eliminarComprobante(id);
    }
  });
}

function eliminarComprobante(id) {
  loading.classList.add("loading");
  const url = `/api/delete_comprobante`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
    }),
  })
    .then(async (response) => {
      if (!response.ok) {
        // Si la respuesta no está en el rango de 200-299
        return response.json().then((errorData) => {
          const error = new Error("Respuesta no satisfactoria");
          error.data = errorData;
          throw error;
        });
      }
      response.json();
    })
    .then((data) => {
      console.log(data);
      Swal.fire("Eliminación completada", "", "success").then(() => {
        location.reload();
      });
    })
    .catch((error) => {
      let errorMessage;
      if (error.data) {
        // Error del servidor
        errorMessage = `Error del servidor: ${
          error.data.message || JSON.stringify(error.data)
        }`;
      } else {
        // Error de red u otro tipo de error
        errorMessage = `Error: ${error.message}`;
      }
      console.error(errorMessage);
      Swal.fire("Error en la eliminaicón", errorMessage, "error");
    })
    .finally(() => loading.classList.remove("loading"));
}

function validar(id) {
  Swal.fire({
    title: "Validar comprobante",
    text: "¿Está seguro que desea validar este comprobante?",
    icon: "question",
    showCancelButton: true,
    confirmButtonColor: "#34d399",
    cancelButtonColor: "#fca5a5",
    confirmButtonText: "Validar",
  }).then((result) => {
    if (result.isConfirmed) {
      validarComprobante(id);
    }
  });
}

function validarComprobante(id) {
  loading.classList.add("loading");
  const url = `/api/validar/comprobante`;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
    }),
  })
    .then(async (response) => {
      if (!response.ok) {
        // Si la respuesta no está en el rango de 200-299
        return response.json().then((errorData) => {
          const error = new Error("Respuesta no satisfactoria");
          error.data = errorData;
          throw error;
        });
      }
      return response.json();
    })
    .then((data) => {
      // console.log('data-', data);
      Swal.fire("Validacion completada", "", "success").then(() => {
        location.reload();
      });
    })
    .catch((error) => {
      let errorMessage;
      if (error.data) {
        // Error del servidor
        errorMessage = `Error del servidor: ${
          error.data.message || JSON.stringify(error.data)
        }`;
      } else {
        // Error de red u otro tipo de error
        errorMessage = `Error: ${error.message}`;
      }
      console.error(errorMessage);
      Swal.fire("Error en la validación", errorMessage, "error");
    })
    .finally(() => loading.classList.remove("loading"));
}

function validarMasivamenteDelDia() {
  Swal.fire({
    title: "¿Validar comprobantes registrados en el día?",
    icon: "question",
    showCancelButton: true,
    confirmButtonColor: "#34d399",
    cancelButtonColor: "#fca5a5",
    confirmButtonText: "Validar",
  }).then((result) => {
    if (result.isConfirmed) {
      validarComprobantesDelDia();
    }
  });
}

function validarComprobantesDelDia() {
  loading.classList.add("loading");
  const url = "/api/validar/comprobantes_del_dia";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(async (response) => {
      if (!response.ok) {
        // Si la respuesta no está en el rango de 200-299
        return response.json().then((errorData) => {
          const error = new Error("Respuesta no satisfactoria");
          error.data = errorData;
          error.status = response.status;
          throw error;
        });
      }
      return response.json();
    })
    .then((responseJson) => {
      Swal.fire(
        "Validaciones completadas",
        `${responseJson.info}`,
        "success"
      ).then(() => {
        location.reload();
      });
    })
    .catch((error) => {
      let errorMessage;
      if (error.data) {
        // Error del servidor
        errorMessage = `Error del servidor: ${
          error.data.message || JSON.stringify(error.data)
        }`;
      } else {
        // Error de red u otro tipo de error
        errorMessage = `Error: ${error.message}`;
      }
      if (error.status === 404) {
        Swal.fire("No se validaron", errorMessage, "info");
        return;
      }
      console.error(errorMessage);
      Swal.fire("Error en la validación", errorMessage, "error").then(() => {
        location.reload();
      });
    })
    .finally(() => loading.classList.remove("loading"));
}


function validarMasivamente() {
  Swal.fire({
    title: "¿Validar comprobantes no validados?",
    icon: "question",
    showCancelButton: true,
    confirmButtonColor: "#34d399",
    cancelButtonColor: "#fca5a5",
    confirmButtonText: "Validar",
  }).then((result) => {
    if (result.isConfirmed) {
      validarComprobantes();
    }
  });
}

function validarComprobantes() {
  loading.classList.add("loading");
  const url = "/api/validar/comprobantes";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(async (response) => {
      if (!response.ok) {
        // Si la respuesta no está en el rango de 200-299
        return response.json().then((errorData) => {
          const error = new Error("Respuesta no satisfactoria");
          error.data = errorData;
          error.status = response.status;
          throw error;
        });
      }
      return response.json();
    })
    .then((responseJson) => {
      Swal.fire(
        "Validaciones completadas",
        `${responseJson.info}`,
        "success"
      ).then(() => {
        location.reload();
      });
    })
    .catch((error) => {
      let errorMessage;
      if (error.data) {
        // Error del servidor
        errorMessage = `Error del servidor: ${
          error.data.message || JSON.stringify(error.data)
        }`;
      } else {
        // Error de red u otro tipo de error
        errorMessage = `Error: ${error.message}`;
      }
      if (error.status === 404) {
        Swal.fire("No se validaron", errorMessage, "info");
        return;
      }
      console.error(errorMessage);
      Swal.fire("Error en la validación", errorMessage, "error").then(() => {
        location.reload();
      });
    })
    .finally(() => loading.classList.remove("loading"));
}
