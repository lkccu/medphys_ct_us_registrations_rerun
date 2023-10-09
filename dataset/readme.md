# dataset #
-- 
dataset目录中包括

- 存放spine的**training**文件夹
- *\DataGeneration_CT-US-Registration\DeformSegmentationAndSimulate\01_crop_ROI.py*处理得到的**cropped_spine**文件夹
- 使用**TotalSegmentator**对原始Spine分割的segmentations文件夹
- 使用*spine deformation*工具得到的椎体以及中间处理结果

其目录树形图如下：
```    │  readme.txt
    │
    ├─01_training
    │  ├─sub-verse*xxx*
    │  │  │  extract_pcd_from_labelmaps.txt
    │  │  │  verse*xxx*forcefield*n*_lumbar_deformed.obj
    │  │  │  verse*xxx*forcefield*n*_lumbar_deformed_ct_img.nii.gz
    │  │  │  verse*xxx*forcefield*n*_lumbar_deformed_field.mha
    │  │  │  verse*xxx*forcefield*n*_lumbar_deformed_seg.nii.gz
    │  │  │  verse*xxx*forcefield*n*_lumbar_deformed_seg_sim.nii.gz
    │  │  │  verse*xxx*_cropped.nii.gz
    │  │  │  verse*xxx*_lumbar_msh.obj
    │  │  │  verse*xxx*_segmentation_cropped.nii.gz
    │  │  │  verse*xxx*_spline_position.txt
    │  │  ├─verse*xxx*forcefield*n*_us_set
    │  ├─verse*xxx*
    │  │  verse*xxx*-w.png
    │  │  verse*xxx*.nii.gz
    │  │  verse*xxx*forcefield*n*_lumbar_deformed.obj
    │  │  verse*xxx*_iso-ctd.json
    │  │  verse*xxx*_lumbar_msh.obj
    │  │  verse*xxx*_seg.nii.gz
    ├─cropped_spine
    │  ├─sub-verse*xxx*
    │  │  verse*xxx*_cropped.nii.gz
    │  │  verse*xxx*_segmentation_cropped.nii.gz
    ├─segs
    │  totalsegcmd.py
    │  verse*xxx*_segmentation.nii
    │  verse005_segmentation.nii
    │  verse008_segmentation.nii    
    │   
    └─vertebrae	   
    ├─forces_folder    
    │  verse*xxx*_*n*.txt    
    ├─spring_files    
    │  verse*xxx*.json   
    │    
    ├─verse*xxx*_verlev*i*    
    │  verse*xxx*_seg_verlev*i*.nii.gz   
    │  verse*xxx*_seg_verlev*i*_msh.obj    
    │  verse*xxx*_seg_verlev*i*_scaled_msh.obj    
    │  verse*xxx*_verlev*i*_forces*n*scaled_deformed_20_0.obj   
    │  verse*xxx*_verlev*i*_forces*n*scaled_deformed_20_0.vtu   
    │  verse*xxx*_verlev*i*_forces*n*_deformed_20_0.obj`
```
*xxx*:  spine序列号   
*i*：   第i个椎体   
*n*：   第n个旋转   



## need to expand.
