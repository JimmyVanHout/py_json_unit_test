# Python Unit Testing Using JSON Tests

A Python-based unit testing program for Python programs, with test parameters written in a JSON file. See the important note in the [About](#about) section *before* using.

## About

> **Important**: This program was mainly created as an academic project and should **not** typically be used over more established and comprehensive unit testing programs such as the built-in Python unit testing module [unittest](https://docs.python.org/3/library/unittest.html) or [pytest](https://docs.pytest.org/).

This program is useful for unit testing Python programs using a file with test specifications (file path, function names, inputs, and expected outputs) written in JSON. A resulting limitation of the program is that the inputs to the tests are also limited to [JSON data types (RFC 8259)](https://datatracker.ietf.org/doc/html/rfc8259#section-3).

This program offers the following benefits:

1. Test parameters can be easily specified in a JSON file (see the format below).

1. Because tests are written in JSON, they can be easily sent to a server to allow remote testing of functions in backend applications.

    For example, to test a function of a web application, the test specification JSON data can be submitted via an HTML form in the browser to a specific testing endpoint such as `https://www.example.com/app/test`. Upon receipt of the test data, the unit testing program can be executed on the server using the received test specifications to test a program in the same filesystem.

## Installation

Clone the repository from [GitHub](https://github.com/JimmyVanHout/py_json_unit_test):

```
git clone https://github.com/JimmyVanHout/py_json_unit_test
```

## Usage

### Create the Test Specifications File

First, if it is not already present, create the **test specifications file**, which is a JSON file (a file containing JSON with a `.json` extension) containing the test specifications. It must be formatted similarly to the following example:

```
{
    "file_path": "/home/username/py_json_unit_test/test/tested.py",
    "tests": [
        {
            "function_name": "f",
            "input": [
                "a",
                "b",
                "c"
            ],
            "expected_output": [
                1,
                2,
                3
            ]
        },
        {
            "function_name": "g",
            "input": [
                "a",
                "b",
                "c"
            ],
            "expected_output": [
                1,
                2,
                3
            ]
        }
    ]
}
```

This example specifies the following:

* The path of the file to test is named `/home/username/py_json_unit_test/test/tested.py`.

* Two functions in `tested.py` will be tested: `f` and `g`.

* The inputs and expected outputs are specified for each function (in both cases here, the expected outputs are `1`, `2`, and `3` for the inputs `"a"`, `"b"`, and `"c"`, respectively).

### Run the Program

Next, **run the program**:

```
python3 unit_test.py <path_to_spec_file>
```

where `<path_to_spec_file>` is the path to the JSON specifications file.

The program output will be printed to standard output. Example output for the test in the following section is given in `test/test_output.txt`. When the program is run, the status (`PASSED`, `FAILED`, `ERROR`) for each test is printed:

* For each passed test, the CPU time is given.

* For each failed test, the input, expected output, and received output is given.

* For each error, the input, expected output, and error is given.

## Testing the Unit Test Program

The files in `test` can be used to test the unit testing program. Run the command:

```
python3 unit_test.py test/tested_test_data.json
```

The expected output is in the file `test/test_output.txt`. To view only the differences between the program's output and the test output, you can run:

```
python3 unit_test.py test/tested_test_data.json | diff - test/test_output.txt
```

The only differences between the program's output to standard output and the test output file should be the execution times of the first tested function, `f`. For example, if the output of the previous command is similar to the following, the test of the unit test program has been successful:

```
5,7c5,7
< 	Test 1...PASSED in 1.55e-06s
< 	Test 2...PASSED in 6.78e-07s
< 	Test 3...PASSED in 5.89e-07s
---
> 	Test 1...PASSED in 1.53e-06s
> 	Test 2...PASSED in 6.89e-07s
> 	Test 3...PASSED in 5.91e-07s
```

## Support

You can file an issue on [GitHub](https://github.com/JimmyVanHout/py_json_unit_test/issues).
