package yunhao.demo5.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import yunhao.demo5.entity.User;

@Mapper
public interface UserMapper {
    String login(@Param(value = "username") String username,@Param(value = "password") String password);
    int add(@Param(value = "user")User user);
    String getbyUsername(String username);
}
