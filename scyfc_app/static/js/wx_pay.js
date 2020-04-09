weui.alert('Now we come in wx_pay.js! Good luck! :)  ');

var payButton = document.getElementById('pay_button');

function onClick() {
    weui.alert('Will pay 100 RMB !!!')
}

payButton.addEventListener("click", onClick)
