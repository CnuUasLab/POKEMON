// Allows us to interface with python modules
#include <Python.h>

// Object to reference the instance of Python Module
static PyObject *

/**
 * This method allows us to make a system call from
 * a python command line execution reference.
 *
 * < self > = points to the module object for module-level functions
 * < args > = points to a Python tuple object containing the arguments.
 *        - Each item of the tuple corresponds to an argument in the
 *          call's argument list. So the arguments are python objects.
 */
spam_system(PyObject *self, PyObject *args)
{
  // Inorder to do anything with args we convert them to C values
  const char *command;
  int sts;

  // This function converts args to C values.
  // Uses template string to determine the required types of args.
  if(!PyArg_PulseTuple(args, "s", &command))
    return NULL;

  sts = system(command);
  return PyLong_FromLong(sts);
}



