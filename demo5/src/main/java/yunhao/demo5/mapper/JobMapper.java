package yunhao.demo5.mapper;

import org.apache.ibatis.annotations.Mapper;
import yunhao.demo5.entity.Job;
import yunhao.demo5.entity.Skill;

import java.util.List;
@Mapper
public interface JobMapper {

    List<Job> findAll();

    Job findOne(int id);

    List<Job> findJobs(String string);

    List<Skill> getSkills();
}
