package yunhao.demo5.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import yunhao.demo5.entity.User;
import yunhao.demo5.mapper.UserMapper;
import yunhao.demo5.service.UserService;

@Service
public class UserServiceImpl implements UserService{
    @Autowired(required = false)
    private UserMapper userMapper;
    @Override
    public String login(String username,String password){
        return userMapper.login(username,password);
    }
    @Override
    public String register(User user){
        int flag = userMapper.add(user);
        if (flag > 0)
            return "success";
        else
            return "failed";
    }
    @Override
    public String getbyUsername(String username){
        return userMapper.getbyUsername(username);
    }
}
