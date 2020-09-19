package yunhao.demo5.service;

import yunhao.demo5.entity.Feature;
import yunhao.demo5.entity.Job;

import java.util.List;

public interface BackService {

    List<Job> dataGet();

    List<Job> dataCut();

    List<Feature> dataPick();

    void update();
}
