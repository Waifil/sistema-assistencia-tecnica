function alternarContraste() {
    document.body.classList.toggle("alto-contraste");

    const ativo = document.body.classList.contains("alto-contraste");

    localStorage.setItem("altoContraste", ativo ? "ativado" : "desativado");
}

document.addEventListener("DOMContentLoaded", function () {
    const contrasteSalvo = localStorage.getItem("altoContraste");

    if (contrasteSalvo === "ativado") {
        document.body.classList.add("alto-contraste");
    }
});