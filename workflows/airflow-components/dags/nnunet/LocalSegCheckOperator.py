import os
import glob
import numpy as np
import nibabel as nib
import pydicom
import json

from kaapana.operators.KaapanaPythonBaseOperator import KaapanaPythonBaseOperator
from kaapana.blueprints.kaapana_global_variables import BATCH_NAME, WORKFLOW_DIR


class LocalSegCheckOperator(KaapanaPythonBaseOperator):

    def get_nifti_dimensions(self, nifti_path, check_labels=True):
        img = nib.load(nifti_path)
        x, y, z = img.shape

        if check_labels and np.max(img.get_fdata()) == 0:
            print("Could not find any label in {}!".format(nifti_path))
            print("ABORT")
            exit(1)

        return [x, y, z]

    def get_dicom_dimensions(self, dcm_path, check_labels=True):
        data = pydicom.dcmread(dcm_path).pixel_array
        if len(data.shape) == 3:
            z, x, y = data.shape
        elif len(data.shape) == 2:
            x, y = data.shape
            z = len(next(os.walk(os.path.dirname(dcm_path)))[2])
        else:
            print("")
            print("")
            print("Could not extract DICOM dimensions!")
            print(f"File: {dcm_path}")
            print(f"Dimensions: {data.shape}")
            print("")
            print("")
            exit(1)

        if check_labels and data.max() == 0:
            print("Could not find any label in {}!".format(dcm_path))
            print("ABORT")
            exit(1)

        return [x, y, z]

    def start(self, ds, **kwargs):
        print("Split-Labels started..")

        run_dir = os.path.join(WORKFLOW_DIR, kwargs['dag_run'].run_id)
        batch_folders = [f for f in glob.glob(os.path.join(run_dir, BATCH_NAME, '*'))]

        print("Found {} batches".format(len(batch_folders)))

        for batch_element_dir in batch_folders:
            nifti_input_dir = os.path.join(batch_element_dir, self.operator_in_dir)
            dcm_input_dir = os.path.join(batch_element_dir, self.dicom_input_operator.operator_out_dir)

            batch_input_files = sorted(glob.glob(os.path.join(nifti_input_dir, "**", "*.nii*"), recursive=True))
            print("Found {} NIFTI files at {}.".format(len(batch_input_files), nifti_input_dir))
            if len(batch_input_files) == 0:
                print("No NIFTI file was found -> checking for DICOM SEG...")
                batch_input_files = sorted(glob.glob(os.path.join(nifti_input_dir, "**", "*.dcm*"), recursive=True))
                if len(batch_input_files) == 0:
                    print("")
                    print("No DICOM SEG file was found -> abort!")
                    print("")
                    exit(1)

            batch_dcm_files = sorted(glob.glob(os.path.join(dcm_input_dir, "**", "*.dcm*"), recursive=True))
            print("Found {} DICOM files at {}.".format(len(batch_dcm_files), dcm_input_dir))

            if len(batch_dcm_files) == 0:
                print("No DICOM file was found!")
                print("abort!")
                exit(1)

            print("Loading DICOM...")
            dicom_dimensions = self.get_dicom_dimensions(dcm_path=batch_dcm_files[0])

            print("Loading Input files...")
            for input in batch_input_files:
                if ".dcm" in input:
                    input_dimensions = self.get_nifti_dimensions(nifti_path=input)
                elif ".nii" in input:
                    input_dimensions = self.get_dicom_dimensions(dcm_path=input)
                else:
                    print(f"Unexpected file: {input} !")
                    print("abort.")
                    print("")
                    exit(1)

                if dicom_dimensions != input_dimensions:
                    print("")
                    print("Dimensions are different!!!")
                    print(f"Dimensions INPUT: {input_dimensions}")
                    print(f"Dimensions DICOM: {dicom_dimensions}")
                    print("")
                    exit(1)
                else:
                    print(f"{input}: Dimensions ok!")

    def __init__(self,
                 dag,
                 dicom_input_operator,
                 *args,
                 **kwargs):

        self.dicom_input_operator = dicom_input_operator

        super().__init__(
            dag,
            name="check-seg-data",
            python_callable=self.start,
            *args,
            **kwargs
        )
