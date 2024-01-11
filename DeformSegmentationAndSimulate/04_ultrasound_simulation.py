import argparse
import os
import subprocess
import time


def process(root_path_spine, txt_file):
    # Read the lines from the text file
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    # Process each line
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespaces
        # todo sub
        subfolder_path = os.path.join(root_path_spine, f"sub-{line}/")
        # subfolder_path = os.path.join(root_path_spine, line)

        # Find the nii.gz file without 'seg' in its name
        batch_files = [
            file_name
            for file_name in os.listdir(subfolder_path)
            if file_name.endswith('.txt') and 'spline' in file_name
        ]

        workspace_us_simulation = "./imfusion_workspaces/us_simulation.iws"
        for batch_file in batch_files:

            arguments_imfusion = f"batch={os.path.join(subfolder_path, batch_file)}"
            print('ARGUMENTS: ', arguments_imfusion)
            # p = subprocess.Popen("ImFusionConsole" + " " + workspace_us_simulation + " " + arguments_imfusion)
            # time.sleep(10)
            # p.kill()
            # todo os.sys
            os.system("ImFusionConsole" + " " + workspace_us_simulation + " " + arguments_imfusion)
            print('################################################### ')




if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="replace the labels with ultrasound simulation labels")

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