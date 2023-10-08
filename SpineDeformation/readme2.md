# readme2

### windows环境配置

1.ImfusionSuite:下载
[ImfusionSuite Base](https://www.imfusion.com/downloads/Webshop/index.html)，并配置环境变量。   

2.Sofa Framework:下载教程[Sofa3Python tutorial](https://sofapython3.readthedocs.io/en/latest/content/Installation.html)，注意版本对应关系，推荐用Conda进行环境分离。否则会出现
**分段错误**
**(sig11 seg fault)**
SpineDeformation所需Sofa env的环境配置已经在**sofa.yml**中展示。    

3 ImfusionConsole命令经常出现阻塞现象，可使用start ImfusionConsole进行并行处理。但可能出现内存卡死现象。

### 目录结构

```
│  00_deformation_pipeline.py   
│  01_scale_mesh_down.py   
│  02_generate_springs_spine_deformation.py   
│  03_deform_lumbar_spines.py    (sofa framework needed)
│  04_convert_vtu_to_obj.py   
│  05_scale_mesh_up.py   
│  06_merge_vertebrae_into_spine_mesh.py   
│  07_center_mesh.py
│  README.md   
│  sofa.yml   
│   
└─imfusion_workspaces    
        merge_lumbar_vertebrae.iws   
        scale_down_mesh.iws    
        scale_up_mesh.iws   
```


**Start scripts**   
`python SpineDeformation\00_deformation_pipeline.py;--root_path_spines 01_training --root_path_vertebrae dataset\vertebrae --list_file_names DeformSegmentationAndSimulate\test_spines.txt --nr_deform_per_spine 10`



