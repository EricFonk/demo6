package yunhao.demo5.mapper;

import org.apache.ibatis.annotations.Mapper;
import yunhao.demo5.entity.Feature;
import yunhao.demo5.entity.Job;

import java.util.List;
@Mapper
public interface BackMapper {

    List<Job> dataGet();

    List<Job> dataCut();

    List<Feature> dataPick();
}
