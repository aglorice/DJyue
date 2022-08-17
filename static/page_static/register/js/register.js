setTimeout(function(){
    $("#repassword ,#password").blur(function (){
        var passwordMsg = document.getElementById("passwordMsg");
        var password_msg = document.getElementById("password_msg");
        const password_val = document.getElementById("password");
        const repassword_val = document.getElementById("repassword");
        if (password_val.value != repassword_val.value){
            password_msg.className="glyphicon glyphicon-remove-sign";
            password_msg.innerHTML="两次输入的密码不一致";
            password_msg.style.color='#ff1244';
    }
        else {
            password_msg.className="glyphicon glyphicon-ok-sign";
            password_msg.innerHTML="两次密码输入一致";
            password_msg.style.color='#8cc540';
            passwordMsg.className="glyphicon glyphicon-ok-sign";
            passwordMsg.style.color='#8cc540';
        }
    });
    $("#username").blur(function () {
        var username=document.getElementById("username");
        var is_user=document.getElementById("is_username");
        let url1;
        url1="/index/is_user?username="+username.value;
        $.ajax({
            url: url1,
            type: "get",
            success: function (reg) {
                if (reg["code"] === 300){
                    is_user.className="glyphicon glyphicon-ok-sign";
                    is_user.style.color='#8cc540';
                    is_user.innerHTML="";
                }
                else if (reg["code"] === 200){
                    is_user.className="glyphicon glyphicon-remove-sign";
                    is_user.innerHTML="用户名已存在";
                    is_user.style.color='#ff1244';
                }
            }
        });
    });
    $("#is_check_code").click(function () {
        var email_value=document.getElementById("email");
        var check_code_msg = document.getElementById("check-code-msg");
        let url;
        if (!email_value.value) {
            check_code_msg.className = "glyphicon glyphicon-question-sign";
            check_code_msg.innerHTML = "请先输入邮箱号";
        } else {
            url = "/index/send_check_code?email=" + email_value.value;
            console.log(url)
            $.ajax({
                url:url,
                type: "get",
                success: function (reg) {
                    // 短信发送失败

                    if (reg["code"] === 200) {
                        check_code_msg.className = "glyphicon glyphicon-question-sign";
                        check_code_msg.innerHTML = "验证码发送成功，验证码十分钟内有效";
                    } else if (reg["code"] === 300) {
                        check_code_msg.className = "glyphicon glyphicon-question-sign";
                        check_code_msg.innerHTML = "验证码已发送，请注意查收";
                    } else {
                        check_code_msg.className = "glyphicon glyphicon-question-sign";
                        check_code_msg.innerHTML = "发送失败，请检查邮箱号是否正确";
                    }
                }
            });

        }

    });
},100);