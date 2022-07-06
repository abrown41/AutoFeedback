"""
Check a students' function works as expected, and provide feedback
"""
import importlib


def _exists(funcname, modname=None):
    """Check that modname.funcname exists (modname and funcname are both
    strings)"""
    import inspect
    if not modname:
        mod = importlib.import_module('main')
    else:
        mod = modname
    funcstring = "mod."+funcname  # get variable from main code
    try:
        testfunc = eval(funcstring)
        return(inspect.isfunction(testfunc))
    except Exception:
        return (False)


def _get_func(funcname, modname=None):
    """import modname.funcname (modname and funcname are both strings)"""
    if not modname:
        mod = importlib.import_module('main')
    else:
        mod = modname
    funcstring = "mod."+funcname  # get function from main code
    return(eval(funcstring))


def _input_vars(func, ins):
    """check that func accepts input as expected
    Parameters
    ==========
    func : function handle for function to be checked
    ins : tuple containing sample inputs
    """
    from copy import deepcopy as dc
    inputs = dc(ins)
    try:
        if hasattr(inputs, "__len__"):
            func(*inputs)
        else:
            func(inputs)
        return True
    except TypeError as e:
        return ('positional' not in str(e))


def _returns(func, ins):
    """check that func returns a value
    Parameters
    ==========
    func : function handle for function to be checked
    ins : tuple containing sample inputs
    """
    from copy import deepcopy as dc
    inputs = dc(ins)
    try:
        if hasattr(inputs, "__len__"):
            res = func(*inputs)
        else:
            res = func(inputs)
        if hasattr(res, "__len__"):
            res = list(res)
        return (res is not None)
    except Exception as e:
        raise(e)


def _check_outputs(func, ins, expected):
    """check that func(ins) returns the expected value
    Parameters
    ==========
    func : function handle for function to be checked
    ins : tuple containing sample inputs
    expected : expected return value of func(ins)
    """
    from AutoFeedback.varchecks import check_value
    from copy import deepcopy as dc
    inputs = dc(ins)
    try:
        res = func(*inputs)
        if hasattr(expected, "check_value") and callable(expected.check_value):
            return expected.check_value(res)
        else:
            return (check_value(res, expected))
    except Exception:
        return False


def _check_calls(func, call):
    """check that func calls another function called 'call'
    Parameters
    ==========
    func : function handle for function to be checked
    call : str, name of other function to be called
    """
    import inspect
    import ast
    try:
        all_names = [c.func for c in ast.walk(
            ast.parse(inspect.getsource(func))) if isinstance(c, ast.Call)]
        call_names = [name.id for name in all_names if
                      isinstance(name, ast.Name)]
        return (call in call_names)
    except Exception:
        return False


def check_func(funcname, inputs, expected, calls=[],
               modname=None, output=True):
    """given information on a function which the student has been asked to
    define, check whether it has been defined correctly, and provide feedback

    Parameters
    ==========
    funcname : str
        name of function to be investigated
    inputs : list of tuples
        inputs with which to test funcname
    expected : list
        expected outputs of [funcname(inp) for inp in inputs]
    calls : list of strings
        names of any functions which funcname should call
    modname : str
        name of module from which funcname should be imported (mostly used for
        testing. If modname==None, then main.py will be used as the source
    output : bool
        if True, print output to screen. otherwise execute quietly

    Returns
    =======
    bool: True if function works as expected, False otherwise.
    """
    from AutoFeedback.function_error_messages import print_error_message
    from copy import deepcopy as copy
    call = []
    ins = inputs[0]
    outs = expected[0]
    res = -999
    try:
        assert(_exists(funcname, modname)), "existence"
        func = _get_func(funcname, modname)
        assert(_input_vars(func, inputs[0])), "inputs"

        assert(_returns(func, inputs[0])), "return"
        for ins, outs in zip(inputs, expected):
            res = func(*copy(ins))  # ensure the inputs are not overwritten
            assert(_check_outputs(func, ins, outs)), "outputs"
        for call in calls:
            assert(_check_calls(func, call)), "calls"
        if output:
            print_error_message("success", funcname)
    except AssertionError as error:
        if output:
            print_error_message(error, funcname, inp=ins,
                                exp=outs, result=res, callname=call)
        return(False)
    except Exception as e:
        if output:
            import traceback
            print_error_message("execution", funcname, inp=ins,
                                exp=outs, result=res, callname=call,
                                msg=traceback.format_exc().splitlines()[-3:])
        return(False)

    return(True)
