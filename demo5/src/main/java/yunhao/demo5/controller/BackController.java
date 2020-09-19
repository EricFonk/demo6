package yunhao.demo5.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import yunhao.demo5.entity.Feature;
import yunhao.demo5.entity.Job;
import yunhao.demo5.service.BackService;

import java.util.List;

@Controller
@RequestMapping("/career/admin")
public class BackController {

    @Autowired
    private BackService backService;

    @ResponseBody
    @RequestMapping("dataGet")
    public List<Job> dataGet(){

        List<Job> jobs = backService.dataGet();
        return jobs;
    }

    @ResponseBody
    @RequestMapping("dataCut")
    public List<Job> dataCut(){
        List<Job> jobs = backService.dataCut();
        return jobs;
    }

    @ResponseBody
    @RequestMapping("dataPick")
    public List<Feature> dataPick(){
        List<Feature> features = backService.dataPick();
        return features;
    }

    @RequestMapping("/update")
    @ResponseBody
    public String update(){
        backService.update();
        return "ok";
    }
}
