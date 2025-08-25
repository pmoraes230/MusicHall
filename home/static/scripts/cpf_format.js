function maskCPF(value) {
    let valor = value.this.replace(/\D/g, "")
    if (valor.length <=3) {
        value = valor.value
    } else if (valor.length <=6) {
        value = valor.value.replace(/(\d{3})(\d+)/, '$1.$2')
    } else if (valor.length <=9) {
        value = valor.value.replace(/(\d{3})(\d{3})(\d+)/, '$1.$2.$3')
    } else {
        value = valor.value.replace(/(\d{3})(\d{3})(\d{3})(\d{3})/, '$1.$2.$3-$4')
    }
}