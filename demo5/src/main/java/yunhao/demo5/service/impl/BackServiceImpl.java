package yunhao.demo5.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import yunhao.demo5.entity.Feature;
import yunhao.demo5.entity.Job;
import yunhao.demo5.mapper.BackMapper;
import yunhao.demo5.service.BackService;

import java.io.*;
import java.util.List;

@Service
public class BackServiceImpl implements BackService {

   @Autowired
    private BackMapper backMapper;

    /**
     * 爬虫
     * @return
     */
    @Override
    public List<Job> dataGet() {
        /*try {
            String path = "F:\\Code\\爬虫\\Lagou\\Lagou";
            //python脚本的路径
            String executePath = path + "\\main.py";
            //执行命令Arr
            String[] cmdArr = new String[]{"python",executePath};
            //参数分别为： 执行命令；执行此脚本的路径
            Process process = Runtime.getRuntime().exec(cmdArr,null,new File(path));
            InputStream inputStream = process.getInputStream();
            int statusNum = process.waitFor();
            inputStream.close();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }*/

        return backMapper.dataGet();
    }

    /**
     * 分词
     * @return
     */
    @Override
    public List<Job> dataCut() {
        /*try {
            String result = "";
            String path = this.getClass().getClassLoader().getResource("algorithm/dataPreprocessing.py").getPath().replaceFirst("/", "");
            //调用python，其中字符串数组对应的是python，python文件路径
            //Runtime类封装了运行时的环境。每个 Java 应用程序都有一个 Runtime 类实例，使应用程序能够与其运行的环境相连接。
            //一般不能实例化一个Runtime对象，应用程序也不能创建自己的 Runtime 类实例，但可以通过 getRuntime 方法获取当前Runtime运行时对象的引用。
            // exec(String[] cmdarray) 在单独的进程中执行指定命令和变量。
            Process pr = Runtime.getRuntime().exec("python " + path);
            //使用缓冲流接受程序返回的结果
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream(), "GBK"));//注意格式
            //定义一个接受python程序处理的返回结果
            String line = " ";
            while ((line = in.readLine()) != null) {
                //循环打印出运行的结果
                System.out.println(line);
            }
            //关闭in资源
            in.close();
            pr.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            String result = "";
            String path = this.getClass().getClassLoader().getResource("algorithm/dataSegmentation.py").getPath().replaceFirst("/", "");
            //调用python，其中字符串数组对应的是python，python文件路径
            //Runtime类封装了运行时的环境。每个 Java 应用程序都有一个 Runtime 类实例，使应用程序能够与其运行的环境相连接。
            //一般不能实例化一个Runtime对象，应用程序也不能创建自己的 Runtime 类实例，但可以通过 getRuntime 方法获取当前Runtime运行时对象的引用。
            // exec(String[] cmdarray) 在单独的进程中执行指定命令和变量。
            Process process = Runtime.getRuntime().exec("python "+path);
            //使用缓冲流接受程序返回的结果
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), "GBK"));//注意格式
            //定义一个接受python程序处理的返回结果
            String line = " ";
            while ((line = reader.readLine()) != null) {
                //循环打印出运行的结果
                System.out.println(line);
            }
            //关闭in资源
            reader.close();
            process.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
*/
        return backMapper.dataCut();
    }

    @Override
    public List<Feature> dataPick() {
       /* System.out.println("特征提取");
        try {
            String path = Thread.currentThread().getContextClassLoader().getResource("algorithm/Test6.py").getPath().replaceFirst("/", "");
            System.out.println(path);
            //调用python，其中字符串数组对应的是python，python文件路径
//            String[] strs=new String[] {"F:\\Tools\\anaconda3\\python.exe","F:\\大创\\算法\\Test6.py"};
            //Runtime类封装了运行时的环境。每个 Java 应用程序都有一个 Runtime 类实例，使应用程序能够与其运行的环境相连接。
            //一般不能实例化一个Runtime对象，应用程序也不能创建自己的 Runtime 类实例，但可以通过 getRuntime 方法获取当前Runtime运行时对象的引用。
            // exec(String[] cmdarray) 在单独的进程中执行指定命令和变量。
            Process pr = Runtime.getRuntime().exec("python " + path);
            //使用缓冲流接受程序返回的结果
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream(), "GBK"));//注意格式
            //定义一个接受python程序处理的返回结果
            String line = " ";
            while ((line = in.readLine()) != null) {
                //循环打印出运行的结果
                System.out.println(line);
            }
            //关闭in资源
            in.close();
            pr.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }*/
        return backMapper.dataPick();
    }

    @Override
    public void update() {
        String path = this.getClass().getClassLoader().getResource("algorithm/Lagou/Lagou/main.py").getPath();
        path = path.replaceFirst("/", "");
        try {
            Process pr = Runtime.getRuntime().exec("python " + path);
            pr.waitFor();
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
