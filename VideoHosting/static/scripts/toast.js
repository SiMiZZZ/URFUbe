const alerts = document.querySelectorAll('.alert')
console.log(alerts)
setTimeout(() => {
    for (const alert of alerts){
        alert.classList.add('invisible')
    }
}, 3000)