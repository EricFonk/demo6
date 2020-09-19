package yunhao.demo5.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import yunhao.demo5.entity.Job;
import yunhao.demo5.entity.Skill;
import yunhao.demo5.mapper.JobMapper;
import yunhao.demo5.service.JobService;

import java.io.*;
import java.util.*;

@Service("jobService")
public class JobServiceImpl implements JobService {

    @Autowired
    private JobMapper jobMapper;

    @Override
    public List<Job> findAll() {
        return jobMapper.findAll();
    }

    @Override
    public Job findOne(int id) {
        return jobMapper.findOne(id);
    }

    @Override
    public List<Job> findJobs(String string) {
//        System.out.println("模糊查询岗位 === "+string);
//        List<Job> jobs = jobMapper.findJobs(finalresult[0]);
//        for (int i = 1; i < finalresult.length; i++) {
//            System.out.println("单个 === "+finalresult[i]);
//            if(finalresult[i] == " "){
//
//            }
//            else{
//                jobs.addAll(jobMapper.findJobs(finalresult[i].replace(" ","")));
//            }
//        }
//        System.out.println(jobs.size());
        return jobMapper.findJobs(string);
    }

    /**
     * 根据前端传入的表单值字符串 通过决策树算法生产推荐岗位
     * @param string
     * @return 岗位
     */
    @Override
    public String[] getJob(String string) {
        System.out.println("old:"+string);
        string = string.replace("undefined","0");
        System.out.println("new:"+string);
        String result = "";
        String path = "";
        try{
            path = this.getClass().getClassLoader().getResource("algorithm/user_run.py").getPath();
            path = java.net.URLDecoder.decode(path, "utf-8");
        }catch(UnsupportedEncodingException e){
            e.printStackTrace();
        }
        path = path.replaceFirst("/", "").replace("\\","/");
        System.out.println("python " + path + " " + string);
//        string[] args = new String[] { "python", "D:\\demo2.py", String.valueOf(a), String.valueOf(b) };
        try {
            //调用python，其中字符串数组对应的是python，python文件路径，向python传递的参数
//            String[] strs=new String[] {"F:\\Tools\\anaconda3\\python.exe","F:\\算法\\user_run.py",string};
            //Runtime类封装了运行时的环境。每个 Java 应用程序都有一个 Runtime 类实例，使应用程序能够与其运行的环境相连接。
            //一般不能实例化一个Runtime对象，应用程序也不能创建自己的 Runtime 类实例，但可以通过 getRuntime 方法获取当前Runtime运行时对象的引用。
            // exec(String[] cmdarray) 在单独的进程中执行指定命令和变量。
            Process pr = Runtime.getRuntime().exec("python " + path + " " + string);
            //使用缓冲流接受程序返回的结果
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream(),"GBK"));//注意格式
            //定义一个接受python程序处理的返回结果
            String line=" ";
            while((line=in.readLine())!=null) {
                //循环打印出运行的结果
                result+=line+"\n";
            }
            //关闭in资源
            in.close();
            pr.waitFor();
        }catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("\npython传来的结果："+result);
        result = result.replace('"',' ');
        result = result.trim();
        String[] temp;
        temp = result.replace('[', ' ').replace(']', ' ' ).replace(",,",",").replaceAll("\\s+","").trim().split(",");
        List list = Arrays.asList(temp);
        Set set = new HashSet(list);
        String[] tempresult = (String[])set.toArray(new String[0]);
        List<String> strsToList=new ArrayList<>();
        Collections.addAll(strsToList,tempresult);
        strsToList.remove("");
        String[] finalresult=strsToList.toArray(new String[strsToList.size()]);
        for (int i = 0; i < finalresult.length; i++) {
            System.out.println("-----------"+finalresult[i]);
        }
        return finalresult;
    }

    @Override
    public List<Skill> getSkills() {
        return jobMapper.getSkills();
    }
}
