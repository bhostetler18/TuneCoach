#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <iostream>
#include <stdio.h>
#include "TunerStream.h"
/*
code adapted from: https://docs.python.org/3/extending/newtypes_tutorial.html
*/

typedef struct {
    PyObject_HEAD
    TunerStream *stream;
} TunerStream_py;
extern "C" {
static void TunerStream_py_dealloc(TunerStream_py *self)
{
    delete self->stream;
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject * TunerStream_py_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    TunerStream_py *self;
    self = (TunerStream_py *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->stream = nullptr;
    }
    return (PyObject *) self;
}

static int TunerStream_py_init(TunerStream_py *self, PyObject *args, PyObject *kwds) {
    int sample_rate;
    if (!PyArg_ParseTuple(args, "i", &sample_rate))
    {
        return -1;
    }
    self->stream = new TunerStream(sample_rate);
    return 0;
}

static PyObject *TunerStream_py_mainloop(TunerStream_py *self, PyObject *Py_UNUSED(ignored))
{
    Py_BEGIN_ALLOW_THREADS
    if (self->stream) {
        self->stream->mainloop();
    }
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}

static PyObject *TunerStream_py_pause(TunerStream_py *self, PyObject *Py_UNUSED(ignored))
{
    if (self->stream) self->stream->pause();
    Py_RETURN_NONE;
}

static PyObject *TunerStream_py_resume(TunerStream_py *self, PyObject *Py_UNUSED(ignored))
{
    if (self->stream) self->stream->resume();
    Py_RETURN_NONE;
}

static PyObject *TunerStream_py_kill(TunerStream_py *self, PyObject *Py_UNUSED(ignored))
{
    if (self->stream) self->stream->kill();
    while (!self->stream->isSafeToDelete());
    delete self->stream;
    self->stream = nullptr;

    Py_RETURN_NONE;
}

static PyObject *TunerStream_py_is_alive(TunerStream_py *self, PyObject *Py_UNUSED(ignored))
{
    if (self->stream && self->stream->isAlive()) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

static PyObject *TunerStream_py_is_paused(TunerStream_py *self, PyObject *Py_UNUSED(ignored))
{
    if (self->stream && self->stream->isPaused()) {
        Py_RETURN_TRUE;
    } else {
        Py_RETURN_FALSE;
    }
}

static PyObject *TunerStream_py_read(TunerStream_py *self, PyObject *Py_UNUSED(ignored))
{
    double ret = 0;
    PyObject *success = Py_False;
    Py_BEGIN_ALLOW_THREADS
    if (self->stream && self->stream->fetch_freq(ret)) {
        success = Py_True;
    }
    Py_END_ALLOW_THREADS
    Py_INCREF(success);
    return PyTuple_Pack(2, PyFloat_FromDouble(ret), success);
}

static PyObject *TunerStream_py_peek(TunerStream_py *self, PyObject *Py_UNUSED(ignored))
{
    double ret = 0;
    Py_BEGIN_ALLOW_THREADS
    if (self->stream) {
        ret = self->stream->peek();
    }
    Py_END_ALLOW_THREADS
    return PyFloat_FromDouble(ret);
}

static PyMethodDef TunerStream_py_methods[] = {
    {   "mainloop", (PyCFunction) TunerStream_py_mainloop, METH_NOARGS,
        "Start the mainloop" },
    {   "pause", (PyCFunction) TunerStream_py_pause, METH_NOARGS,
        "Pause the TunerStream" },
    {   "resume", (PyCFunction) TunerStream_py_resume, METH_NOARGS,
        "Resume the TunerStream" },
    {   "kill", (PyCFunction) TunerStream_py_kill, METH_NOARGS,
        "Kill the TunerStream" },
    {   "is_alive", (PyCFunction) TunerStream_py_is_alive, METH_NOARGS,
        "Check if the TunerStream is alive" },
    {   "is_paused", (PyCFunction) TunerStream_py_is_paused, METH_NOARGS,
        "Check if the TunerStream is paused" },
    {   "read", (PyCFunction) TunerStream_py_read, METH_NOARGS,
        "Reads from the TunerStream, returning a 2-tuple (double result, bool success)" },
    {   "peek", (PyCFunction) TunerStream_py_peek, METH_NOARGS,
        "Takes a peek at the TunerStream, returning None if no data is availible" },
    {NULL}
};

/* 
the order here isn't supposed to matter BUT IT DOES, because of inconsistencies between C/C++.
You can look up the correct order of fields here:
https://docs.python.org/3/extending/newtypes.html
*/
static PyTypeObject TunerStream_py_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "pitch_detection.TunerStream",
    .tp_basicsize = sizeof(TunerStream_py),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) TunerStream_py_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "Tuner Stream object",
    .tp_methods = TunerStream_py_methods,
    .tp_init = (initproc) TunerStream_py_init,
    .tp_new = TunerStream_py_new,
};

static struct PyModuleDef pitch_detection_module {
    PyModuleDef_HEAD_INIT,
    .m_name = "pitch_detection",
    .m_doc = "A module which exposes the C++ TunerStream class to python",
    .m_size = -1,
};


PyMODINIT_FUNC
PyInit_pitch_detection(void) {
    PyObject* m;
    if (PyType_Ready(&TunerStream_py_type) < 0)
        return NULL;
    m = PyModule_Create(&pitch_detection_module);
    if (m == NULL)
        return NULL;
        
    Py_INCREF(&TunerStream_py_type);
    if (PyModule_AddObject(m, "TunerStream", (PyObject *) &TunerStream_py_type) < 0)
    {
        Py_DECREF(&TunerStream_py_type);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
}