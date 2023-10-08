import os
import argparse
if __name__ == '__main__':
    """
    scripts for batch segmentations by TotalSegmentator.
    """
    arg_parser = argparse.ArgumentParser(description="Generate segmentations")

    arg_parser.add_argument(
            "--root_path_spines",
            required=True,
            dest="root_path_spines",
            help="Root path to the spine folders."
        )

    arg_parser.add_argument(
        "--list_file_names",
        required=True,
        dest="txt_file",
        help="Txt file that contains all spines that contain all lumbar vertebrae"
    )

    arg_parser.add_argument(
        "--segmentation_folder",
        required=True,
        help="folder containing the output of the total segmentator"
    )

    args =arg_parser.parse_args()

    root_path_spine = args.root_path_spines
    segmentation_folder = args.segmentation_folder
    txt_file = args.txt_file

    with open(txt_file, 'r') as file:
        lines = file.readlines()
    file.close()
    # Process each line
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespaces
        subfolder_path = os.path.join(root_path_spine, line)
        output_path = os.path.join(segmentation_folder, f"{line}_segmentation")

        # Find the nii.gz file without 'seg' in its name
        nii_files = [
            file_name
            for file_name in os.listdir(subfolder_path)
            if file_name.endswith('.nii.gz') and 'seg' not in file_name
        ]

        in_path = os.path.join(subfolder_path, nii_files[0])

        cmd = 'TotalSegmentator' + ' -i' + in_path + ' -o' + output_path + ' --fast --ml'
        print("cmd: ", cmd)
        os.system(cmd)