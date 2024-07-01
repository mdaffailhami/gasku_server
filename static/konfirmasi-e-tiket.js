const email = localStorage.getItem('email');
const pass = localStorage.getItem('pass');

const params = new Proxy(new URLSearchParams(window.location.search), {
  get: (searchParams, prop) => searchParams.get(prop),
});

const nik = window.location.pathname.split('/').at(-2);
const key = window.location.pathname.split('/').at(-1);

if (email == null || pass == null) {
  window.location.pathname = `/form-login/konfirmasi-e-tiket/${nik}/${key}`;
}

const modal = new bootstrap.Modal(document.getElementById('modal'), {});
const konten = document.getElementById('konten');
const tombolKonfirmasi = document.getElementById('tombol-konfirmasi');
const loading = document.getElementById('loading');

async function konfirmasiETiket() {
  // Start loading
  loading.classList.remove('d-none');

  const url = `/konfirmasi-e-tiket/${nik}/${key}`;

  try {
    let response = await fetch(url, {
      headers: { Accept: 'application/json' },
      method: 'POST',
    });

    response = await response.json();

    if (response.status == 'failed') {
      alert(response.message);
      console.log(response);
    } else {
      alert('E-Tiket Berhasil Dikonfirmasi');
    }
  } catch (error) {
    alert('Error:', error);
  } finally {
    // Stop loading
    loading.classList.add('d-none');
  }
}

async function initial() {
  modal.toggle();
  tombolKonfirmasi.addEventListener('click', () => konfirmasiETiket());

  const url = `/pengguna/${nik}`;

  try {
    const response = await fetch(url);

    const data = await response.json();

    if (data.status == 'failed') throw JSON.stringify(data);

    tombolKonfirmasi.classList.remove('disabled');
    const pengguna = data.pengguna;

    konten.innerHTML = `
      <table class="table">
        <tbody>
          <tr>
            <th scope="row">●</th>
            <td>Nama</td>
            <td>:</td>
            <td>${pengguna.nama}</td>
          </tr>
          <tr>
            <th scope="row">●</th>
            <td>NIK</td>
            <td>:</td>
            <td>${pengguna.nik}</td>
          </tr>
          <tr>
            <th scope="row">●</th>
            <td>KK</td>
            <td>:</td>
            <td>${pengguna.kk}</td>
          </tr>
          <tr>
            <th scope="row">●</th>
            <td>Email</td>
            <td>:</td>
            <td>${pengguna.email}</td>
          </tr>
        </tbody>
      </table>
    `;
  } catch (error) {
    konten.innerHTML = '<h5>Data tidak ditemukan</h5>';
    console.log('Error:', error);
  }
}

initial();
