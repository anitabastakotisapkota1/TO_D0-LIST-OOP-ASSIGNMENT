var pass1 = document.getElementById("pass1")
var pass2 = document.getElementById("pass2")
function clicked1() {

    if (pass1.type === 'password') {
        pass1.type = 'type'
    }
    else {
        pass1.type = 'password'

    }
}
function clicked2() {
    if (pass2.type === 'password') {
        pass2.type = 'text'
    }
    else {
        pass2.type = "password"

    }
}
