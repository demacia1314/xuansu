class FrontBase{
    constructor() {
        var self = this
        self.listenAuthBoxHover()
    }

    listenAuthBoxHover =()=>{
        var authBox = $('.auth-box')
        var userMoreBox = $('.user-more-box')
        authBox.hover(function (){
            userMoreBox.show()
        },function (){
            userMoreBox.hide()
        })
    }
}