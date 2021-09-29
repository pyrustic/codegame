import ast
import codeval


class Section:
    META = "[META]"
    INPUT = "[INPUT]"
    OUTPUT = "[OUTPUT]"


def parse_test(test_spec):
    """test_spec is a string"""
    cache = _extract_sections(test_spec)
    meta_section, input_section, output_section = cache
    return (_formalize_meta_section(meta_section),
           _formalize_input_section(input_section),
           _formalize_output_section(output_section))


def eval_user_code(code, test):
    meta_section, input_section, output_section = test
    fname = meta_section.get("function")
    max_time = meta_section.get("max_time", 0)
    codeval.process(code, fname, kwargs=input_section,
                    output=output_section, max_time=max_time)



def _extract_sections(data):
    lines = data.splitlines()
    meta_section = []
    input_section = []
    output_section = []
    current_section = None
    for line in lines:
        if line == "" or line.isspace():
            continue
        if line in (Section.META, Section.INPUT, Section.OUTPUT):
            current_section = line
            continue
        if current_section == Section.META:
            meta_section.append(line)
        elif current_section == Section.INPUT:
            input_section.append(line)
        elif current_section == Section.OUTPUT:
            output_section.append(line)
    return meta_section, input_section, output_section


def _formalize_meta_section(meta_section):
    data = {}
    for line in meta_section:
        cache = line.split("=", maxsplit=1)
        if len(cache) != 2:
            continue
        left = cache[0].strip("\" '")
        right = cache[1].strip("\" '")
        if left in ("name", "function", "max_time"):
            if left == "max_time":
                try:
                    data[left] = float(right)
                except Exception as e:
                    raise InvalidTest("max_time must be a float or an integer")
            else:
                data[left] = right
    return data


def _formalize_input_section(input_section):
    data = {}
    for line in input_section:
        cache = line.split("=", maxsplit=1)
        if len(cache) != 2:
            continue
        left = cache[0].strip("\" '")
        right = cache[1].strip(" ")
        try:
            data[left] = ast.literal_eval(right)
        except Exception as e:
            raise InvalidTest("Invalid input section")
    return data


def _formalize_output_section(output_section):
    for line in output_section:
        try:
            data = ast.literal_eval(line)
        except Exception as e:
            break
        else:
            return data
    raise InvalidTest("Invalid output section")


class Error(Exception):
    pass


class InvalidTest(Error):
    pass
