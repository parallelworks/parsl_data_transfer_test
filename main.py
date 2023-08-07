import os

import parsl
from parsl.app.app import bash_app
print(parsl.__version__, flush = True)

import parsl_utils
from parsl_utils.config import config, exec_conf
from parsl_utils.config import config, resource_labels, executor_dict
from parsl_utils.data_provider import PWFile

from workflow_apps import test_file_transfer

# tmp notes:
# gcloud auth activate-service-account --key-file=MY_KEY_FILE.json
# Running the above command on the controller also works for compute nodes

FILES_PER_POOL_TYPE: dict = {
    'gclusterv2': {
        'inputs': [
            PWFile(
                url = 'gs://demoworkflows/parsl_demo/hello.in',
                local_path = './hello.in'
            )
        ],
        'outputs': [
            PWFile(
                url = 'gs://demoworkflows/parsl_demo/hello.out',
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

print(FILES_PER_POOL_TYPE, flush = True)

if __name__ == '__main__':

    print('Loading Parsl Config', flush = True)
    parsl.load(config)


    fut_list: list = []
    
    # Test the PWRSyncStaging on the first executor:
    first_executor_label = resource_labels[0]
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
    for executor_label in resource_labels:
        resource_type = executor_dict[executor_label]['resource']['type']
        print(f'\n\nExecutor label: {executor_label}\nTesting type {resource_type}')
        fut = bash_app(test_file_transfer, executors=[executor_label])(
            **FILES_PER_POOL_TYPE[resource_type],
            stdout = f'log-{resource_type}.out',
            stderr = f'log-{resource_type}.err'
        )
        
        fut_list.append(fut)
    
    for fut in fut_list:
        print(fut.result())