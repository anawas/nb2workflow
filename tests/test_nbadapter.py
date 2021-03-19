import os
import logging


# this can be also set in pytest call
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("nb2workflow")
logger.setLevel(level=logging.DEBUG)


def test_nbadapter(test_notebook):
    from nb2workflow.nbadapter import NotebookAdapter

    nba = NotebookAdapter(test_notebook)
    parameters = nba.extract_parameters()

    print(parameters)
    assert len(parameters) == 4

    assert 'comment' in parameters['scwid']
    assert parameters['scwid']['owl_type'] == "http://odahub.io/ontology/integral#ScWID"

    outputs = nba.extract_output_declarations()
    print("outputs", outputs)

    assert len(outputs) == 3

    if os.path.exists(nba.output_notebook_fn):
        os.remove(nba.output_notebook_fn)

    if os.path.exists(nba.preproc_notebook_fn):
        os.remove(nba.preproc_notebook_fn)

    nba.execute(dict())

    output = nba.extract_output()

    print(output)
    assert len(output) == 4

    assert 'spectrum' in output


def test_nbadapter_repo(test_notebook_repo):
    from nb2workflow.nbadapter import NotebookAdapter, find_notebooks

    nbas = find_notebooks(test_notebook_repo)

    assert len(nbas) == 1

    for nba_name, nba in nbas.items():
        print("notebook", nba_name)

        parameters = nba.extract_parameters()

        print(parameters)
        assert len(parameters) == 4

        if os.path.exists(nba.output_notebook_fn):
            os.remove(nba.output_notebook_fn)

        if os.path.exists(nba.preproc_notebook_fn):
            os.remove(nba.preproc_notebook_fn)

        nba.execute(dict())

        output = nba.extract_output()

        print(output)

        assert len(output) == 4
        assert 'spectrum' in output


def test_nbreduce(test_notebook):
    from nb2workflow.nbadapter import NotebookAdapter, nbreduce, setup_logging

    setup_logging()

    nba = NotebookAdapter(test_notebook)

    if os.path.exists(nba.output_notebook_fn):
        os.remove(nba.output_notebook_fn)

    if os.path.exists(nba.preproc_notebook_fn):
        os.remove(nba.preproc_notebook_fn)

    nba.execute(dict())

    output = nba.extract_output()

    assert len(output) == 4

    assert 'spectrum' in output

    print("will reduce", nba.output_notebook_fn)

    nbsize_b = os.path.getsize(nba.output_notebook_fn)

    assert isinstance(nbsize_b, int)

    assert nbsize_b > 0

    nbreduce(nba.output_notebook_fn, nbsize_b/1024./1024 + 1.)

    nbreduce(nba.output_notebook_fn, nbsize_b/1024./1024*0.5)


def test_denumpyfy():
    import numpy as np
    import json
    from nb2workflow.nbadapter import denumpyfy

    data = {"d": np.bool_(True), "k": np.array([1, 2, 3]), "dd": [
        1, 2, np.float32(33), {'a': np.int64(10)}]}

    try:
        r = json.dumps(data)
        print(r)
    except TypeError as e:
        print("failed as expected", e)
    else:
        raise Exception("did not fail")

    r = json.dumps(denumpyfy(data))
    print(r)
