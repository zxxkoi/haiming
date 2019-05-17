var log = console.log.bind(console)

var e = function (sel) {
    return document.querySelector(sel)
}

var es = function (sel) {
    return document.querySelectorAll(sel)
}

var bindEventLogin = function() {
    var login = e('.change-login')
    // 事件响应函数会传入一个参数 就是事件本身
    login.addEventListener('click', function(event) {
        var self = event.target
        var register = e('.change-register')
        var loginForm = e('.login-form')
        var registerForm = e('.register-form')
        var slideBar = e('.slide-bar')
        if (register.classList.contains('active')) {
            register.classList.remove('active')
            self.classList.add('active')
            slideBar.classList.remove('slide-bar1')
            registerForm.setAttribute('style', "display: none;")
            loginForm.setAttribute('style', '')
        }

})}


var bindEventRegister = function() {
    var register = e('.change-register')
    register.addEventListener('click', function(event) {
        var self = event.target
        var login = e('.change-login')
        var loginForm = e('.login-form')
        var registerForm = e('.register-form')
        var slideBar = e('.slide-bar')
        if (login.classList.contains('active')) {
            login.classList.remove('active')
            self.classList.add('active')
            slideBar.classList.add('slide-bar1')
            loginForm.setAttribute('style', "display: none;")
            registerForm.setAttribute('style', '')
        }

    // if (self.classList.contains('todo-edit')) {
    //     log('点到了编辑按钮')
    //     todoCell = self.closest('.todo-cell')
    //     todoId = todoCell.dataset['id']
    //     var todoSpan = e('.todo-title', todoCell)
    //     var title = todoSpan.innerText
    //     // 插入编辑输入框
    //     insertUpdateForm(title, todoCell)
    // } else {
    //     log('点到了 todo cell')
    // }
})}


var __main = function() {
     bindEventLogin()
    bindEventRegister()
}

__main()