import importlib
import json
import os
import pathlib
import sys
import time

def run_test(func, input, expected_output):
    results = []
    for i in range(len(input)):
        received_output = None
        result = {
            "input": input[i],
        }
        start_time = None
        end_time = None
        try:
            start_time = time.process_time()
            received_output = func(input[i])
            end_time = time.process_time()
        except Exception as e:
            result["status"] = False
            result["expected_output"] = expected_output[i]
            result["error"] = e
        else:
            total_time = end_time - start_time
            result["time"] = total_time
            if expected_output[i] == received_output:
                result["status"] = True
            else:
                result["status"] = False
                result["expected_output"] = expected_output[i]
                result["received_output"] = received_output
        results.append(result)
    return results

def test_file(file_name, module, tests):
    print("Testing " + file_name + ":")
    passed_all = True
    for test in tests:
        function_name = test["function_name"]
        func = None
        try:
            func = getattr(module, function_name)
        except AttributeError:
            print("\nError: Could not locate function " + function_name + " in file " + file_name)
            passed_all = False
        else:
            input = test["input"]
            expected_output = test["expected_output"]
            print("\nTesting " + function_name + ":\n")
            results = run_test(func, input, expected_output)
            count = 1
            num_passed = 0
            did_not_pass = []
            for result in results:
                print("\tTest " + str(count) + "...", end="")
                if "error" in result:
                    print("ERROR")
                    did_not_pass.append((count, result))
                    passed_all = False
                else:
                    if result["status"]:
                        time = result["time"]
                        print("PASSED in {time:.2e}s".format(time=time))
                        num_passed += 1
                    else:
                        print("FAILED")
                        did_not_pass.append((count, result))
                        passed_all = False
                count += 1
            print("\n\tPassed " + str(num_passed) + "/" + str(len(results)) + " tests\n")
            if passed_all:
                print("\tPassed all tests for " + function_name)
            else:
                for test_num, result in did_not_pass:
                    if "error" in result:
                        print("\tTest {test_num}: Error while testing {function_name}: From input {input}, expected {expected_output} but received the following error: {error}".format(test_num=test_num, function_name=function_name, input=result["input"], expected_output=result["expected_output"], error=result["error"]))
                    else:
                        print("\tTest {test_num}: Failure while testing {function_name}: From input {input}, expected {expected_output} but received {received_output}".format(test_num=test_num, function_name=function_name, input=result["input"], expected_output=result["expected_output"], received_output=result["received_output"]))
    if passed_all:
        print("\nPASSED ALL TESTS")
    print("\nFinished testing " + file_name)

def import_module(file_path):
    file_name = os.path.basename(file_path)
    if not os.path.isfile(file_path):
        raise FileNotFoundError("Could not locate file " + str(file_name) + "\n")
    module_name = file_name.rstrip(".py")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

if __name__ == "__main__":
    test_data_file_path = pathlib.Path(sys.argv[1])
    test_data = None
    with open(test_data_file_path) as test_data_file:
        test_data = json.load(test_data_file)
    tested_file_path = test_data["file_path"]
    module_name = os.path.basename(tested_file_path).rstrip(".py")
    module = None
    try:
        module = import_module(tested_file_path)
    except FileNotFoundError as e:
        raise ModuleNotFoundError("Error: Could not locate module " + module_name + "\n") from e
    tests = test_data["tests"]
    tested_file_name = os.path.basename(tested_file_path)
    test_file(tested_file_name, module, tests)
    sys.exit(0)
