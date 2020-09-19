package yunhao.demo5.controller;

import org.apache.ibatis.annotations.Param;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import yunhao.demo5.entity.User;
import yunhao.demo5.service.UserService;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import javax.websocket.Session;

@Controller
@RequestMapping("career/user")
public class UserController {
    @Autowired
    private UserService userService;

    @ResponseBody
    @RequestMapping(value = "/login",method = RequestMethod.POST)
    public String login(String username,String password,HttpServletRequest request){
        String result = userService.login(username,password);
        if(result=="")
            return result;
        else {
            HttpSession session =request.getSession();
            session.setAttribute("username",result);
            return result;
        }
    }
    @ResponseBody
    @RequestMapping(value = "/register",method = RequestMethod.POST)
    public String register(User user){
        String result = userService.register(user);
        return result;
    }
    @ResponseBody
    @RequestMapping(value = "/nameexist",method = RequestMethod.POST)
    public String nameexist(String username){

        String result = userService.getbyUsername(username);
        System.out.println("nameexist:"+result);
        if(result != null)
            return "已经存在此用户名";
        else
            return "可使用";
    }
}
