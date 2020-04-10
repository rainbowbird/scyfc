
var mydata = JSON.parse(document.getElementById("mydiv").dataset.mydata)
var payButton = document.getElementById('pay_button');

function onClick() {
    weui.alert('APPID: ' + mydata.appId + ' timestamp: ' + mydata.timestamp + ' nonceStr:' + mydata.nonceStr + ' signature: ' + mydata.signature)
}
payButton.addEventListener("click", onClick)


wx.config({
    debug: true,
    appId: mydata.appId,
    timestamp: mydata.timestamp,
    nonceStr: mydata.nonceStr,
    signature: mydata.signature,
    jsApiList: ['chooseWXPay']
});

wx.ready(function(){
    wx.checkJsApi({
        jsApiList: ['chooseWXPay'],
        success:function(res){
            weui.alert("WXPay is ready");
        },
        fail:function(res){
            weui.alert("WXPay is not ready")
        }
    })
});
wx.error(function() {
    weui.alert("WX config is wrong!!!")
});

/*
wx.chooseWXPay({
    timestamp: 0, // 支付签名时间戳，注意微信jssdk中的所有使用timestamp字段均为小写。但最新版的支付后台生成签名使用的timeStamp字段名需大写其中的S字符
    nonceStr: '', // 支付签名随机串，不长于 32 位
    package: '',  // 统一支付接口返回的prepay_id参数值，提交格式如：prepay_id=\*\*\*）
    signType: '', // 签名方式，默认为'SHA1'，使用新版支付需传入'MD5'
    paySign: '',  // 支付签名
    success: function (res) {
      // 支付成功后的回调函数
    }
  });
*/

// prepay_id 通过微信支付统一下单接口拿到，
// paySign 采用统一的微信支付 Sign 签名生成方法，注意这里 appId 也要参与签名，
//   appId 与 config 中传入的 appId 一致，即最后参与签名的参数有appId, timeStamp, nonceStr, package, signType。