package yunhao.demo5.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import yunhao.demo5.entity.Job;
import yunhao.demo5.entity.Skill;
import yunhao.demo5.service.JobService;

import java.util.List;

@Controller
@RequestMapping("/career")
public class JobController {
    @Autowired
    private JobService jobService;

    @ResponseBody
    @RequestMapping("/getJobs")
    public List<Job> getJobs(){
        List<Job> jobs = jobService.findAll();
        return jobs;
    }


    @ResponseBody
    @RequestMapping("findOne")
    public Job findOne(@RequestParam("id") int id){
        Job job = jobService.findOne(id);
        return job;
    }

    @ResponseBody
    @RequestMapping("/getJob")
    public String[] getJob(@RequestParam("str") String string){
        String[] result = jobService.getJob(string);
//        List<Job> jobs = jobService.findJobs(result);
        return result;
    }
    @ResponseBody
    @RequestMapping("/getSingleJobs")
    public List<Job> getSingleJobs(@RequestParam("str") String string) {
    return jobService.findJobs(string);
    }

    @GetMapping("/labels")
    @ResponseBody
    public List<Skill> getLabels(){
        return jobService.getSkills();
    }
}
