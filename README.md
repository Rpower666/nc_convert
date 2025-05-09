### 需求与计划

最近在处理NetCDF(.nc)数据，发现多年数据在arcmap处理很麻烦，再者虽然有build，但我对图形模式操作并不感冒，而且还有其他需求需要处理。

故选择使用module-->*`arcpy`*实现批量操作。

<p align="center"><img src="https://cdn.jsdelivr.net/gh/Rpower666/pic@main/20250509%2F1638_%E5%A4%84%E7%90%86%E6%B5%81%E7%A8%8B%E5%9B%BE.png" style="zoom:10%;" /><br /><strong>处理NetCDF流程图</strong></p>

#### 以下为代码的部分解释（请务必先看完）：

注意：arcpy只支持`python2.7`，请务必确保你是安装了`arcgis10.X`。

建议直接使用arcgis里的Python2.7，里面包含了arcpy包，且arcpy不开源，用conda安装也需要认证。



1. 先定位到代码最后，在def main()修改`extent_path` 和`root_path`。

   | env_variance | description       |
   | ------------ | ----------------- |
   | extent_path  | 矢量边界.shp      |
   | root_path    | 需要处理的.nc文件 |

   

1. 在读取NetCDF时，通常需要设置`variable`，根据`Arctoolbox` --> `Multidimension Tools`--> `Make NetCDF Raster Layer`查看文件变量是什么，这里的`ept_layer_{}`为文件名称，可自行修改。
<p align="center"><img src="https://cdn.jsdelivr.net/gh/Rpower666/pic@main/20250509%2F1410_20250509141025375.png" style="zoom:100%;" /><br /><strong>读取NetCDF</strong></p>

3. 在转为tiff格式的时候，请注意`pixel_type`，具体看`Properties` -->`Source`。投影看个人需要，可以是空间参考为地理坐标如`WGS 1984`这里的`4326`也就是WGS1984，也可以是投影坐标如`WGS1984 UTM Zone 39N`。

<p align="center"><img src="https://cdn.jsdelivr.net/gh/Rpower666/pic@main/20250509%2F1419_20250509141905928.png" style="zoom:50%;" /><br /><strong>转为TIFF</strong>
最后进行运行，运行时间取决于文件数量，由于本人未熟悉synr，所以时间可能还是需要一些，等待跑完即可。

在Evaporation文件生成文件目录如下：

```python
Evaporation
├── pet_2014
│   ├── clip
│   │   ├── etp_2014_month_01_clip.tfw
│   │   ├── ...
│   ├── data
│   │   ├── etp_201401_stats.csv
│   │   ├── etp_201401.dbf
│   │   ├── ...
│   ├── tiff
│   │   ├── etp_2014_month_01.tif
│   │   ├── ...
│   ├── pet_2014.nc
├── pet_2015
│   ├── clip
│   │   ├── etp_2015_month_01_clip.tfw
│   │   ├── ...
│   ├── data
│   │   ├── etp_201501_stats.csv
│   │   ├── etp_201501.dbf
│   │   ├── ...
│   ├── tiff
│   │   ├── etp_2015_month_01.tif
│   │   ├── ...
│   ├── pet_2015.nc
```



如果你有什么好的意见或问题欢迎提交issue。
=======
# nc_convert
>>>>>>> b8ab7460355436d0b224ba923586ab950c8d2512
