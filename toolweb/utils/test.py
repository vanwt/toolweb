import subprocess


def run_code(code):
    try:
        output = subprocess.check_output(["python", "-c", code],
                                         universal_newlines=True,
                                         stderr=subprocess.STDOUT,
                                         timeout=30)
    except subprocess.CalledProcessError as e:
        return e.output
    except subprocess.TimeoutExpired as e:
        return '\r\n'.join(['Time Out!!!', e.output])
    return output


code = "print('print')"

print(run_code(code))
