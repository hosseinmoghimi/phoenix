// leonolan2020@gmail.com
// 2020-09-05
// 
// 

let to_price =function(x,currency) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' ' + currency
  }


  var showNotification = function (from, align, icon, bgcolor, html) {
    type = ['', 'info', 'danger', 'success', 'warning', 'rose', 'primary'];

    color = Math.floor((Math.random() * 6) + 1);
    color = 3;
    $.notify({
        icon: icon,
        message: html

    }, {
        type: bgcolor,
        timer: 3000,
        placement: {
            from: from,
            align: align
        }
    });
}