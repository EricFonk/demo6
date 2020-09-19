package yunhao.demo5.service;

import yunhao.demo5.entity.User;

public interface UserService {
    String login(String username,String password);
    String register(User user);
    String getbyUsername(String username);
}
