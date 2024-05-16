console.log("comprobantes");
const dataTablesOptions = {
  responsive: true,
  order: [[0, "desc"]],
  autoWidth: false,
  language: {
    entries: {
      _: "Entradas",
      1: "Entrada",
    },
    search: "Buscar: ",
  },
  // language: {
  //   "url": "https://cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json"
  // },
  layout: {
    topStart: {
      search: {
        placeholder: "Ingresa busqueda",
      },
    },
    topEnd: "pageLength",
    bottomStart: {
      paging: {
        numbers: 5,
      },
    },
    bottomEnd: "info",
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
};

const tablaComprobantes = new DataTable(
  "#tablaComprobantes ",
  dataTablesOptions
).columns
  .adjust()
  .responsive.recalc();

/** Agregar filas */
comprobantes.forEach(function (comprobante) {
  tablaComprobantes.row
    .add([
      `<span style="font-size: 0.7rem"}>${comprobante.id}</span>`,
      comprobante.ruc,
      comprobante.fecha_emision,
      comprobante.serie,
      comprobante.numero,
      comprobante.monto,
      comprobante.tipo_comprobante,
      renderRowStatus(comprobante.estado_comprobante),
      renderRowStatus(comprobante.estado_ruc),
      renderRowStatus(comprobante.cod_domiciliaria_ruc),
      renderRowOptions(comprobante.id),
    ])
    .draw();
});

function renderRowStatus(status) {
  const colorStatus = {
    "NO EXISTE": "badge text-bg-secondary",
    ACEPTADO: "badge text-bg-success",
    ANULADO: "badge text-bg-danger",
    // EstadoRuc
    ACTIVO: "badge text-bg-success",
    // ConDomRuc
    HABIDO: "badge text-bg-success",
    default: "badge text-bg-secondary",
  };
  return `<span class='px-2 py-1 ${
    colorStatus[status] || colorStatus["default"]
  }'>${status}</span>`;
}

function renderRowOptions(id) {
  const buttonValidar = `
        <button onclick="aceptar(${id})" class="btn btn-light col-3 col-sm-4"">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        </button>
    `;
  const buttonEliminar = `
        <button onclick="eliminar(${id})" class="btn btn-light col-3 col-sm-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fca5a5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
        </button>
    `;
  const buttonDetails = `
        <button onclick="showDetails(${id})" class="btn btn-light col-3 col-sm-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" style="width:100%;height:100%;transform:translate3d(0,0,0);content-visibility:visible" viewBox="0 0 500 500"><defs><clipPath id="a"><path d="M0 0h500v500H0z"/></clipPath><clipPath id="c"><path d="M0 0h500v500H0z"/></clipPath><clipPath id="b"><path d="M0 0h500v500H0z"/></clipPath></defs><g clip-path="url(#a)"><g clip-path="url(#b)" style="display:block"><g class="primary design" style="display:none"><path fill="none" class="primary"/></g><g class="primary design" style="display:none"><path class="primary"/><path fill="none" class="primary"/></g><g class="primary design" style="display:none"><path fill="#4a90e2" d="m427.222 397.726-75.488-75.488c21.017-27.245 33.661-61.281 33.661-98.234 0-89.152-72.488-161.432-161.432-161.432-88.945 0-161.433 72.28-161.433 161.432 0 88.944 72.488 161.433 161.433 161.433 37.014 0 71.071-12.686 98.338-33.745l75.467 75.488a20.773 20.773 0 0 0 14.727 6.103 20.773 20.773 0 0 0 14.727-6.103c8.144-8.145 8.144-21.31 0-29.454zm-203.26-293.494c66.032 0 119.773 53.741 119.773 119.772s-53.741 119.773-119.772 119.773c-66.032 0-119.773-53.742-119.773-119.773 0-66.03 53.741-119.772 119.773-119.772z" class="primary"/></g><g class="primary design" style="display:block"><path fill="#4a90e2" d="m427.222 397.726-75.488-75.488c21.017-27.245 33.661-61.281 33.661-98.234 0-89.152-72.488-161.432-161.432-161.432-88.945 0-161.433 72.28-161.433 161.432 0 88.944 72.488 161.433 161.433 161.433 37.014 0 71.071-12.686 98.338-33.745l75.467 75.488a20.773 20.773 0 0 0 14.727 6.103 20.773 20.773 0 0 0 14.727-6.103c8.144-8.145 8.144-21.31 0-29.454zm-203.26-293.494c66.032 0 119.773 53.741 119.773 119.772s-53.741 119.773-119.772 119.773c-66.032 0-119.773-53.742-119.773-119.773 0-66.03 53.741-119.772 119.773-119.772z" class="primary"/></g></g><g clip-path="url(#c)" style="display:none"><g class="primary design" style="display:none"><path fill="none" class="primary"/></g><g class="primary design" style="display:none"><path class="primary"/><path fill="none" class="primary"/></g><g class="primary design" style="display:none"><path class="primary"/></g></g></g></svg>
        </button>
    `;

  return `
          <div class="row">
              ${buttonDetails} ${buttonValidar} ${buttonEliminar}
          </div>
          `;
}

function validarComprobantes() {
  let timerInterval;
  // Agregar un spinner
  Swal.fire({
    title: "Auto close alert!",
    html: "Validando <b></b> segundos.",
    timer: 10000,
    timerProgressBar: true,
    didOpen: () => {
      Swal.showLoading();
      const timer = Swal.getPopup().querySelector("b");
      timerInterval = setInterval(() => {
        timer.textContent = `${Swal.getTimerLeft()}`;
      }, 100);
    },
    willClose: () => {
      clearInterval(timerInterval);
      location.reload()
    }
  }).then((result) => {
    /* Read more about handling dismissals below */
    if (result.dismiss === Swal.DismissReason.timer) {
      console.log("I was closed by the timer");
    }
  });
  const url = '/api/validar/comprobantes'
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(data => {
    console.log(data)
  })
}
