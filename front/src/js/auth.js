class Auth{
    constructor(){
        var self = this
        self.maskWrapper = $('.mask-wrapper')
        self.scrollWrapper = $(".scroll-wrapper")

        self.listenShowHideEvent()
        self.listenSwitchEvent()
        self.listenSigninEvent()
        self.listenImageCaptcha()
        self.listenEmailCaptcha()
        self.listenSignupEvent()
    }

    listenSwitchEvent =()=>{
        var self = this
        var authInnerWrapper = $('.auth-inner-wrapper')
        $('.switch').click(function (){
        var title = authInnerWrapper.find("span[class='title']")
        var switchBtn = authInnerWrapper.find("a[class='switch']")
        var currentLeft = self.scrollWrapper.css('left')
        currentLeft = parseInt(currentLeft)
        if(currentLeft<0){
            self.scrollWrapper.animate({'left':'0'})
            title.css({'float':'left'})
            switchBtn.css({'float':'right'})
        }else{
            self.scrollWrapper.animate({'left':'-400px'})
            title.css({'float':'right'})
            switchBtn.css({'float':'left'})
        }
    })
    }

    showEvent =()=>{
        var self = this
        self.maskWrapper.show()
        self.maskWrapper.animate({'opacity':'1'},500)
    }

    closeEvent =()=>{
        var self = this
        self.maskWrapper.animate({'opacity':'0'},500,function (){
            self.maskWrapper.hide()
        })
    }

    listenShowHideEvent =()=>{
        var self = this
        $('#sign-in-up').click(function (){
            self.showEvent()
        })
        $('.close-btn').click(function (){
            self.closeEvent()
        })
    }

    listenImageCaptcha =()=>{
        var imageCaptcha = $('.image-captcha')
        imageCaptcha.click(function (){
            imageCaptcha.attr("src","/xuansu_auth/image_captcha/"+"?random="+Math.random())
        })
    }

    listenEmailCaptcha =()=>{
        var signupGroup = $('.signup-group')
        var emailInput = signupGroup.find("input[name='email']")
        var emailCaptchaBtn = $('.email-captcha-btn')

        emailCaptchaBtn.click(function (event){
            event.preventDefault()
            var email = emailInput.val()

            if(email){
                window.messageBox.showInfo('验证码发送成功')
                xuansu_ajax.get({
                'url':'/xuansu_auth/email_captcha/',
                'data':{
                    'email':email
                },
                'success':function (result){
                    if(result['code']==200){
                    }else{
                        var messageObject = result['message']
                        if(typeof messageObject == 'string' || messageObject.constructor==String){
                            window.messageBox.showError(messageObject)
                        }else{
                            for(var key in messageObject){
                                var messages = messageObject[key]
                                var message = messages[0]
                                window.messageBox.showError(message)
                            }
                        }
                    }
                },
            })
            }else{
                window.messageBox.showError('请输入邮箱')
            }
        })

    }

    listenSigninEvent =()=>{
        var signinGroup = $('.signin-group')
        var accountInput = signinGroup.find("input[name='account']")
        var passwordInput = signinGroup.find("input[name='password']")
        var rememberInput = signinGroup.find("input[name='remember']")
        var submitBtn = signinGroup.find(".submit-btn")

        submitBtn.click(function (){
            var account = accountInput.val()
            var password = passwordInput.val()
            var remember = rememberInput.prop('checked')

            xuansu_ajax.post({
                'url':'/xuansu_auth/login/',
                'data':{
                    'account':account,
                    'password':password,
                    'remember':remember
                },
                'success':function (result){
                    if(result['code']==200){
                        window.location.reload()
                    }else{
                        var messageObject = result['message']
                        if(typeof messageObject == 'string' || messageObject.constructor==String){
                            window.messageBox.showError(messageObject)
                        }else{
                            for(var key in messageObject){
                                var messages = messageObject[key]
                                var message = messages[0]
                                window.messageBox.showError(message)
                            }
                        }
                    }
                },
            })
        })
    }

    listenSignupEvent =()=>{
        var signupGroup = $('.signup-group')
        var submitBtn = signupGroup.find('.submit-btn')

        submitBtn.click(function (event){
            event.preventDefault()  //阻止默认行为
            var usernameInput = signupGroup.find("input[name='username']")
            var accountInput = signupGroup.find("input[name='account']")
            var passwordInput = signupGroup.find("input[name='password']")
            var emailInput = signupGroup.find("input[name='email']")
            var imageCaptchaInput = signupGroup.find("input[name='image-captcha']")
            var emailCaptchaInput = signupGroup.find("input[name='email-captcha']")

            var username = usernameInput.val()
            var account = accountInput.val()
            var password = passwordInput.val()
            var email = emailInput.val()
            var imageCaptcha = imageCaptchaInput.val()
            var emailCaptcha = emailCaptchaInput.val()

            xuansu_ajax.post({
                'url':'/xuansu_auth/register/',
                'data':{
                    'username':username,
                    'account':account,
                    'password':password,
                    'email':email,
                    'imageCaptcha':imageCaptcha,
                    'emailCaptcha':emailCaptcha,
                },
                'success':function (result){
                    if(result['code']==200){
                        window.location.reload()
                    }else{
                        var messageObject = result['message']
                        if(typeof messageObject == 'string' || messageObject.constructor==String){
                            window.messageBox.showError(messageObject)
                        }else{
                            for(var key in messageObject){
                                var messages = messageObject[key]
                                var message = messages[0]
                                window.messageBox.showError(message)
                            }
                        }
                    }
                },
            })
        })
    }
}

$(function (){
    var auth = new Auth()
})

$(function (){
    var frontBase = new FrontBase()
})