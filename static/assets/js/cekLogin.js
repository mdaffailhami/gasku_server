async function getPage() {
    let email = localStorage.getItem('email')
    let pass = localStorage.getItem('pass')


    if (email == null || pass == null) {
        window.location.pathname = '/form-login'
    }

    try {
        let getEmail = await fetch('/pangkalan/' + email)
        let getJson = await getEmail.json();

        if (getJson.status == 'failed' || pass != getJson.pangkalan.kata_sandi) {
            return window.location.pathname = '/form-login'
        }

        document.body.classList.remove('d-none')

    } catch (error) {
        console.log(error)
    }
}

getPage();