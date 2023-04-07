# PARSL DATA TRANSFER TEST
Workflow to test the custom data providers for PW clusters. The function `test_file_transfer` in `workflow_apps.py` is executed on every executor listed on the `executors.json` file. This function transfers files from their global path to their worker path (stage in) and viceversa (stage out). 

**Directory paths must end with `/`.** 

## Data Providers
### Rsync
The PWRsync data provider is tested on the first executor. This provider is used if the prefix of the global path starts with `file` (e.g.: `file://<host-name>/path/to/file`). 

### GCP Bucket: gsutil
The PWGsutil data provider is tested on every GCP executor. This provider is used if the prefix of the global path starts with `gs` (e.g.: `gs://<bucket-name>/path/to/file`).

### AWS Bucket: aws s3
The PWS3 data provider is tested on every AWS executor. This provider is used if the prefix of the global path starts with `s3` (e.g.: `s3://<bucket-name>/path/to/file`).

## Authentication
The workflow and data providers assume the resources have been authenticate and have the correct permission to launch the corresponding `rsync`, `gsutil` and `aws s3` commands. Follow this [link](https://github.com/parallelworks/parsl_utils/blob/main/data_provider/README.md) to authenticate the resources. 
