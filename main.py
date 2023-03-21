import sys, os, json, time
from random import randint
import argparse

import parsl
from parsl.app.app import bash_app
print(parsl.__version__, flush = True)

import parsl_utils
from parsl_utils.config import config, exec_conf
from parsl_utils.data_provider import PWFile

from workflow_apps import test_file_transfer

# tmp notes:
# gcloud auth activate-service-account --key-file=MY_KEY_FILE.json
# Running the above command on the controller also works for compute nodes

FILES_PER_POOL_TYPE: dict = {
    'gclusterv2': {
        'inputs': [
            PWFile(
                url = 'gs://bucket/demoworkflows/parsl_demo/hello.in',
                local_path = './hello.in'
            )
        ],
        'outputs': [
            PWFile(
                url = 'gs://bucket/demoworkflows/parsl_demo/hello.out',
                local_path = './hello.out'
            )
        ]
    },
    'pclusterv2': {
        'inputs': [
            PWFile(
                url = 's3://demoworkflows/data_transfer_test/hello.in',
                local_path = './hello.in'
            )
        ],
        'outputs': [
            PWFile(
                url = 's3://demoworkflows/data_transfer_test/hello.out',
                local_path = './hello.out'
            )
        ]
    }
}

print(FILES_PER_POOL_TYPE)

if __name__ == '__main__':

    print('Loading Parsl Config', flush = True)
    parsl.load(config)


    fut_list: list = []
    
    # Test the PWRSyncStaging on the first executor:
    first_executor_label = list(exec_conf.keys())[0]
    print(f'\n\nExecutor label: {first_executor_label}\nTesting PWRSyncStaging')
    fut = bash_app(test_file_transfer, executors=[first_executor_label])(
        inputs = [ 
            PWFile(
                url = 'file://usercontainer/{cwd}/PWRSyncStaging.in'.format(cwd = os.getcwd()),
                local_path = './inputs/PWRSyncStaging.in'
                )
            ],
            outputs = [
                PWFile(
                    url = 'file://usercontainer/{cwd}/outputs/PWRSyncStaging.out'.format(cwd = os.getcwd()),
                    local_path = './PWRSyncStaging.out'
                )
            ],
        stdout = 'log-PWRSyncStaging.out',
        stderr = 'log-PWRSyncStaging.err'
    )
    
    fut_list.append(fut)
    
    """
    Test data provider corresponding to POOL_TYPE. For example:
    - gclusterv2: PWGsutil
    - pclusterv2: PWAWSS3
    """
    for exec_label, exec_conf_i in exec_conf.items():
        pool_type = exec_conf_i['POOL_TYPE']
        print(f'\n\nExecutor label: {exec_label}\nTesting type {pool_type}')
        fut = bash_app(test_file_transfer, executors=[exec_label])(
            **FILES_PER_POOL_TYPE[pool_type],
            stdout = f'log-{pool_type}.out',
            stderr = f'log-{pool_type}.err'
        )
        
        fut_list.append(fut)
    
    for fut in fut_list:
        print(fut.result())