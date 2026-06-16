// script.js

// Exemplo: alerta quando clicar em botão de salvar
document.addEventListener("DOMContentLoaded", function() {
    const salvarBtn = document.querySelector("button[type='submit']");
    if (salvarBtn) {
        salvarBtn.addEventListener("click", function() {
            alert("Dados enviados com sucesso!");
        });
    }
});

// Exemplo: destacar linha da tabela ao passar o mouse
document.querySelectorAll("table tr").forEach(function(row) {
    row.addEventListener("mouseover", function() {
        this.style.backgroundColor = "#ecf0f1";
    });
    row.addEventListener("mouseout", function() {
        this.style.backgroundColor = "";
    });
});
