import argparse
import os
import shutil

import numpy as np
import SimpleITK as sitk
import torchio
import torchio as tio


def process(root_path_spine, txt_file):
    # Read the lines from the text file
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    # Process each line
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespaces
        subfolder_path = os.path.join(root_path_spine, f"sub-{line}/")

        # Find the nii.gz file with 'seg' in its name
        nii_files = [
            file_name
            for file_name in os.listdir(subfolder_path)
            if file_name.endswith('.nii.gz') and 'seg' in file_name and "deformed" in file_name and 'sim' not in file_name
        ]

        batch_file_path = os.path.join(subfolder_path, f"{line}_spline_position.txt")
        if os.path.exists(batch_file_path):
            os.remove(batch_file_path)
        with open(batch_file_path, 'w') as file:
            file.write('OUTFILE; OUT2DSET; TRASSPLINE; DIRECTIONSPLINE; INFILE\n')

        for nii_file in nii_files:

            prepare_us_simulation(batch_file_path, line, nii_file, subfolder_path)


def prepare_us_simulation(batch_file_path, line, nii_file, subfolder_path):
    # Open the nii.gz file found using torchio
    nii_path = os.path.join(subfolder_path, nii_file)
    image = tio.ScalarImage(nii_path)
    print(f"Loaded image: {nii_path}")
    save_path = os.path.join(subfolder_path, nii_file.replace("_seg.nii.gz", "_seg_sim.nii.gz"))
    # create the txt input for ultrasound simulation
    sim_output_path = os.path.join(subfolder_path, nii_file.replace("_seg.nii.gz", "_us_sim.imf"))
    sim_output_folder = os.path.join(subfolder_path, nii_file.replace("_lumbar_deformed_seg.nii.gz", "_us_set"))
    if os.path.exists(sim_output_folder):
        shutil.rmtree(sim_output_folder)
    os.makedirs(sim_output_folder)
    argument = calculate_splines(segmentation=image, output_path=sim_output_path, output_folder=sim_output_folder, file_path=save_path)
    # Open the file in write mode
    with open(batch_file_path, 'a') as file:
        file.write(f'{argument}\n')
    replace_labels(image, save_path)


def replace_labels(image, save_path):
    seg_data = image.data
    seg_data[(seg_data == 80) | (seg_data == 81) | (seg_data == 82) |
             (seg_data == 83) | (seg_data == 84) | (seg_data == 85) |
             (seg_data == 86) | (seg_data == 87) | (seg_data == 88) |
             (seg_data == 89)  ] = 8  # muscle
    seg_data[(seg_data == 25) | (seg_data == 26) | (seg_data == 27) |
             (seg_data == 28) | (seg_data == 29) | (seg_data == 30) |
             (seg_data == 31) | (seg_data == 32) | (seg_data == 33) |
             (seg_data == 34) | (seg_data == 77) | (seg_data == 78)] = 13  # bone
    seg_data[seg_data == 3] = 3  # fat
    seg_data[seg_data == 0] = 3  # background
    seg_data[(seg_data != 8) & (seg_data != 13) & (seg_data != 3) & (seg_data != 1)] = 12  # soft tissue
    image.set_data(seg_data)
    image.save(save_path)


def calculate_splines(segmentation: torchio.Image, output_path, output_folder, file_path):

    segmentation_data = segmentation.data.squeeze()
    # find sacrum lowest point
    lowest_sacrum_index = 0
    for i in range(segmentation_data.shape[2]):
        slice_ = segmentation_data[:, :, i]
        # if (slice_ == 92).sum() > 0 and (slice_ == 18).sum() == 0:
        if (slice_ == 25).sum() > 0 :
            lowest_sacrum_index = i
            break
    lowest_t11_index = 0
    for i in range(segmentation_data.shape[2]):
        slice_ = segmentation_data[:, :, i]
        # if (slice_ == 23).sum() > 0:
        if (slice_ == 33).sum() > 0:
            lowest_t11_index = i
            break
    # find the lateral lowest point
    lowest_lateral_index = 0
    for i in range(segmentation_data.shape[1]):
        slice_ = segmentation_data[:, i, :]
        # if ((slice_ < 24) & (slice_ >= 18)).sum() > 0:
        if ((slice_ >= 25) & (slice_ < 33)).sum() > 0:
            lowest_lateral_index = i
            break

    margin = 20  # 20 mm spline margin


    x = segmentation_data.shape[0] // 2
    y1 = np.max([lowest_lateral_index - margin // segmentation.spacing[1], 0])
    y2 = y1 + 100 // segmentation.spacing[1]  # for the direction spline
    z2 = lowest_t11_index #segmentation_data.shape[2]
    z1 = lowest_sacrum_index
    print(f"shape of segs:{segmentation_data.shape}")
    print(x,y1,y2,z1,z2)
    # fixing_vector = np.array([1, -1, 1])

    sitk_image = sitk.ReadImage(segmentation.path)

    point1 = sitk_image.TransformContinuousIndexToPhysicalPoint(np.array([x, y1, z1])) # fixing_vector * (segmentation.affine @ np.array([x, y1, z1, 1]))[:3]
    point2 = sitk_image.TransformContinuousIndexToPhysicalPoint(np.array([x, y1, z2])) # fixing_vector * (segmentation.affine @ np.array([x, y1, z2, 1]))[:3]
    trans_spline = np.concatenate([point1, point2], axis=0)

    point3 = sitk_image.TransformContinuousIndexToPhysicalPoint(np.array([x, y2, z1])) # fixing_vector * (segmentation.affine @ np.array([x, y2, z1, 1]))[:3]
    point4 = sitk_image.TransformContinuousIndexToPhysicalPoint(np.array([x, y2, z2])) # fixing_vector * (segmentation.affine @ np.array([x, y2, z2, 1]))[:3]
    dir_spline = np.concatenate([point3, point4], axis=0)

    print(trans_spline)
    print(dir_spline)
    arguments = f"{output_path}; {output_folder}; {' '.join(map(str, trans_spline.tolist()))}; {' '.join(map(str, dir_spline.tolist()))}; {file_path}"

    return arguments


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="replace the labels with ultrasound simuation labels")

    arg_parser.add_argument(
        "--root_path_spine",
        required=True,
        dest="root_path_spine",
        help="Root path of the spine folders with cropped spines"
    )

    arg_parser.add_argument(
        "--list_file_names",
        required=True,
        dest="txt_file",
        help="Txt file that contains all spines that contain all lumbar vertebrae"
    )

    args = arg_parser.parse_args()
    process(args.root_path_spine, args.txt_file)