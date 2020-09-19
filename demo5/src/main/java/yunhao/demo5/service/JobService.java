package yunhao.demo5.service;

import yunhao.demo5.entity.Job;
import yunhao.demo5.entity.Skill;

import java.util.List;

public interface JobService {
    List<Job> findAll();

    Job findOne(int id);

    List<Job> findJobs(String string);

    String[] getJob(String string);

    List<Skill> getSkills();
}
