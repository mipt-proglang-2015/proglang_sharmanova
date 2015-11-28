#include <vector>

extern "C" {
#include <Python.h>
}

namespace electro {
	typedef std::vector<double>  row_t;
	typedef std::vector<row_t>   matrix_t;

	static matrix_t electro_count(matrix_t &a)
	{
		for (size_t k = 0; k < a.size(); ++k)
			for (size_t i = 0; i < a.size(); ++i)
				for (size_t j = 0; j < a.size(); ++j)
					if (a[i][j] != 0 && a[i][k] + a[k][j] != 0)
						a[i][j] = a[i][j] * (a[i][k] + a[k][j]) / (a[i][j] + a[i][k] + a[k][j]);

		return a;
	}
}

static electro::matrix_t pyobject_to_cxx(PyObject * py_matrix)
{
	electro::matrix_t result;
	result.resize(PyObject_Length(py_matrix));
	for (size_t i = 0; i<result.size(); ++i) {
		PyObject * py_row = PyList_GetItem(py_matrix, i);
		electro::row_t & row = result[i];
		row.resize(PyObject_Length(py_row));
		for (size_t j = 0; j<row.size(); ++j) {
			PyObject * py_elem = PyList_GetItem(py_row, j);
			const double elem = PyFloat_AsDouble(py_elem);
			row[j] = elem;
		}
	}
	return result;
}

static PyObject * cxx_to_pyobject(const electro::matrix_t &matrix)
{
	PyObject * result = PyList_New(matrix.size());
	for (size_t i = 0; i<matrix.size(); ++i) {
		const electro::row_t & row = matrix[i];
		PyObject * py_row = PyList_New(row.size());
		PyList_SetItem(result, i, py_row);
		for (size_t j = 0; j<row.size(); ++j) {
			const double elem = row[j];
			PyObject * py_elem = PyFloat_FromDouble(elem);
			PyList_SetItem(py_row, j, py_elem);
		}
	}
	return result;
}

static PyObject * electro_count(PyObject * module, PyObject * args)
{
	PyObject * py_a = PyTuple_GetItem(args, 0);
	electro::matrix_t a = pyobject_to_cxx(py_a);
	electro::matrix_t result = electro::electro_count(a);
	PyObject * py_result = cxx_to_pyobject(result);
	return py_result;
}


PyMODINIT_FUNC PyInit_matrixops()
{
	static PyMethodDef ModuleMethods[] = {
		{ "electro_count", electro_count, METH_VARARGS, "Count all Rs" },
		{ NULL, NULL, 0, NULL }
	};
	static PyModuleDef ModuleDef = {
		PyModuleDef_HEAD_INIT,
		"electro",
		"Count all Rs",
		-1, ModuleMethods,
		NULL, NULL, NULL, NULL
	};
	PyObject * module = PyModule_Create(&ModuleDef);
	return module;
}
