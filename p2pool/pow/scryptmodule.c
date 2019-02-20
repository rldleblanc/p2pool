#include <Python.h>

//#include "scrypt.h"

static PyObject *scrypt_getpowhash(PyObject *self, PyObject *args)
{
    char *output;
    PyObject *value;
    PyBytesObject *input;
    if (!PyArg_ParseTuple(args, "S", &input))
        return NULL;
    Py_INCREF(input);
    output = PyMem_Malloc(32);

    scrypt_1024_1_1_256((char *)PyBytes_AsString((PyObject*) input), output);
    Py_DECREF(input);
    value = Py_BuildValue("y#", output, 32);
    PyMem_Free(output);
    return value;
}

static PyMethodDef ScryptMethods[] = {
    { "getPoWHash", scrypt_getpowhash, METH_VARARGS, "Returns the proof of work hash using scrypt" },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef cModPyScrypt =
{
    PyModuleDef_HEAD_INIT,
    "ltc_scrypt",	/* name of module */
    "Scrypt functions",	/* module documentatain */
    -1,			/* size of per-interpreter state of the module,
			   or -1 if the module keeps state in global variables. */
    ScryptMethods
};

PyMODINIT_FUNC PyInit_ltc_scrypt(void) {
    return PyModule_Create(&cModPyScrypt);
}
