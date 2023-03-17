from parsl.app.app import python_app, bash_app
import parsl_utils


# PARSL APPS:
#@parsl_utils.parsl_wrappers.log_app
def test_file_transfer(inputs = [], outputs = [], stdout='std.out', stderr = 'std.err'):
    """
    Sample bash to test transferring files
    """
    return '''
        cd {run_dir}
        cat {hello_in} > {hello_out}
        date >> {hello_out}
        echo Running test on ${HOSTNAME}:${PWD} >> {hello_out}
    '''.format(
        hello_in = inputs[0].local_path,
        hello_out = outputs[0].local_path,
    )
