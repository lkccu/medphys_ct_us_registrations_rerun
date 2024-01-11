import argparse
import os

# convert_segmentation_into_mesh
"""
python thesis\convert_segmentation_into_mesh.py;"
--root_path_vertebrae {dataset}\\vertebrae 
--list_file_names dataset\\list.txt
--workspace_file_segm_to_mesh {thesis}\\imfusion_workspaces\\segmentation_to_mesh.iws
 """

# separate spine into vertebrae
""" 
python thesis\\separate_spine_into_vertebrae.py
--list_file_names dataset\\list.txt
--root_path_vertebrae dataset\\vertebrae
--root_path_spines dataset\\rawdata
"""

# total segmentation script
"""
python thesis/generate_totalseg_cmd.py 
--root_path_spines dataset\\rawdata 
--list_file_names dataset\\list.txt
--segmentation_folder dataset\\segs
"""

# Deform Segmentation And Simulate Pipeline
"""
python DeformSegmentationAndSimulate\\00_segment_and_simulate_pipeline.py
--root_path_spines dataset\\rawdata 
--root_path_vertebrae dataset-xyx\\vertebrae 
--list_file_names dataset\\spine.txt 
--nr_deform_per_spine 10 
--pipeline all
"""


# dataset/thesis/srcDeform是需要定义的参数
def generate_seg_to_mesh_cmd(root_thesis: str, root_dataset: str):
    path_script = os.path.join(root_thesis, 'convert_segmentation_into_mesh.py')
    root_path_vert = os.path.join(root_dataset, '../dataset-xyx/auto-test/vertebrae')
    list_file_name = os.path.join(root_dataset, '../dataset-xyx/auto-test/list.txt')
    workspace_file_segm_to_mesh = os.path.join(root_thesis, 'imfusion_workspaces', 'segmentation_to_mesh.iws')

    cmd = (f'python {path_script} '
           f'--root_path_vertebrae {root_path_vert} '
           f'--list_file_names {list_file_name} '
           f'--workspace_file_segm_to_mesh {workspace_file_segm_to_mesh}')

    return cmd


def generate_spine_to_vert_cmd(root_thesis: str, root_dataset: str):
    path_script = os.path.join(root_thesis, 'separate_spine_into_vertebrae.py')
    root_path_vert = os.path.join(root_dataset, '../dataset-xyx/auto-test/vertebrae')
    list_file_name = os.path.join(root_dataset, '../dataset-xyx/auto-test/list.txt')
    root_path_spines = os.path.join(root_dataset, '../dataset-xyx/auto-test/rawdata')

    cmd = (f'python {path_script} '
           f'--root_path_vertebrae {root_path_vert} '
           f'--list_file_names {list_file_name} '
           f'--root_path_spines {root_path_spines}')

    return cmd


def generate_totalseg_cmd(root_thesis: str, root_dataset: str):
    path_script = os.path.join(root_thesis, 'generate_totalseg_cmd.py')
    segmentation_folder = os.path.join(root_dataset, '../dataset-xyx/auto-test/segs')
    list_file_name = os.path.join(root_dataset, '../dataset-xyx/auto-test/list.txt')
    root_path_spines = os.path.join(root_dataset, '../dataset-xyx/auto-test/rawdata')

    cmd = (f'python {path_script} '
           f'--segmentation_folder {segmentation_folder} '
           f'--list_file_names {list_file_name} '
           f'--root_path_spines {root_path_spines}')

    return cmd


def generate_main_pipe_cmd(root_src_deform:str, root_dataset:str):
    path_script = os.path.join(root_src_deform, '00_segment_and_simulate_pipeline.py')
    root_path_vert = os.path.join(root_dataset, '../dataset-xyx/auto-test/vertebrae')
    list_file_name = os.path.join(root_dataset, '../dataset-xyx/auto-test/list.txt')
    root_path_spines = os.path.join(root_dataset, '../dataset-xyx/auto-test/rawdata')

    cmd = (f'python {path_script} '
           f'--root_path_vertebrae {root_path_vert} '
           f'--list_file_names {list_file_name} '
           f'--root_path_spines {root_path_spines} '
           f'--nr_deform_per_spine 10')

    return cmd


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description="Generate segmentations")

    arg_parser.add_argument(
        "--root_thesis",
        required=True,
        help="Root path to the spine folders."
    )

    arg_parser.add_argument(
        "--root_dataset",
        required=True,
        help="folder containing all dataset including raw/segs/cropped_spine/vertebrae"
    )

    arg_parser.add_argument(
        "--root_src_deform",
        required=True,
        help="folder containing the source code of Deform Segmentation and Simulation"
    )

    args = arg_parser.parse_args()
    # init params
    root_thesis = args.root_thesis
    root_dataset = args.root_dataset
    root_src_deform = args.root_src_deform

    # generate commands
    totalseg_cmd = generate_totalseg_cmd(root_thesis,root_dataset)
    spine_to_vert_cmd = generate_spine_to_vert_cmd(root_thesis,root_dataset)
    seg_to_mesh_cmd = generate_seg_to_mesh_cmd(root_thesis,root_dataset)
    main_pipe_cmd = generate_main_pipe_cmd(root_src_deform,root_dataset)

    print(f'totalseg_cmd = {totalseg_cmd} \n'
          f'spine_to_vert_cmd = {spine_to_vert_cmd} \n'
          f'seg_to_mesh_cmd = {seg_to_mesh_cmd} \n'
          f'main_pipe_cmd ={main_pipe_cmd} \n')

