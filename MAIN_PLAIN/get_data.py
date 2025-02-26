from colorama import init, Fore, Back, Style
init()
from datasets import load_dataset
import subprocess
import os
import sys

if __name__ == "__main__":

    if not os.path.exists("bitcode"):
        os.mkdir("bitcode")

    if not os.path.exists("stats"):
        os.mkdir("stats")
    
    ds = load_dataset('llvm-ml/ComPile', split='train', streaming=True)

    iteration = 0
    index = 0

    dataset_iterator = iter(ds)

    for i in range(1000):
        iteration = iteration + 1
        bitcode_module = next(dataset_iterator)['content']
        IR_module = None
        dis_command_vector = [
            './build/bin/llvm-dis', '-']
        with subprocess.Popen(
                dis_command_vector,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE) as dis_process:
            IR_module = dis_process.communicate(
                input=bitcode_module)[0].decode('utf-8')

        as_command_vector = ['./build/bin/llvm-as',
                            '-', '--o', f'./bitcode/test.bc']
        with subprocess.Popen(
                as_command_vector,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE) as as_process:
            as_process.communicate(
                input=IR_module.encode('utf-8'))

        opt_command_vector = [
            './build/bin/opt',  '-stats', f'./bitcode/test.bc']
        opt_O1_command_vector = [
            './build/bin/opt', '-O1', '-stats', f'./bitcode/test.bc']
        opt_O2_command_vector = [
            './build/bin/opt', '-O2', '-stats', f'./bitcode/test.bc']
        opt_O3_command_vector = [
            './build/bin/opt', '-O3', '-stats', f'./bitcode/test.bc']
        opt_Os_command_vector = [
            './build/bin/opt', '-Os', '-stats', f'./bitcode/test.bc']
        opt_Oz_command_vector = [
            './build/bin/opt', '-Oz', '-stats', f'./bitcode/test.bc']

        output_string = ""
        output_string += "PLAIN STATS> \n"
        with subprocess.Popen(opt_command_vector, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as opt_process:
            stdout_data, stderr_data = opt_process.communicate()
            stderr_str = stderr_data.decode('utf-8')
            output_string += str(stderr_data)[222:-1]

        output_string += "O1 STATS> \n"
        with subprocess.Popen(opt_O1_command_vector, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as opt_O1_process:
            stdout_data, stderr_data = opt_O1_process.communicate()
            stderr_str = stderr_data.decode('utf-8')
            output_string += str(stderr_data)[222:-1]

        output_string += "O2 STATS> \n"
        with subprocess.Popen(opt_O2_command_vector, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as opt_O2_process:
            stdout_data, stderr_data = opt_O2_process.communicate()
            stderr_str = stderr_data.decode('utf-8')
            output_string += str(stderr_data)[222:-1]

        output_string += "O3 STATS> \n"
        with subprocess.Popen(opt_O3_command_vector, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as opt_O3_process:
            stdout_data, stderr_data = opt_O3_process.communicate()
            stderr_str = stderr_data.decode('utf-8')
            output_string += str(stderr_data)[222:-1]

        output_string += "Os STATS> \n"
        with subprocess.Popen(opt_Os_command_vector, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as opt_Os_process:
            stdout_data, stderr_data = opt_Os_process.communicate()
            stderr_str = stderr_data.decode('utf-8')
            output_string += str(stderr_data)[222:-1]

        output_string += "Oz STATS> \n"
        with subprocess.Popen(opt_Oz_command_vector, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as opt_Oz_process:
            stdout_data, stderr_data = opt_Oz_process.communicate()
            stderr_str = stderr_data.decode('utf-8')
            output_string += str(stderr_data)[222:-1]

        output_string = output_string.replace('\\n', '\n')

        if (iteration % 10 == 0):
            index += 1

        with open(f'./stats/stats_{index}.txt', 'a') as f:
            f.write(f"====================================  STATS FOR FILE : {i} ====================================\n")
            f.write(output_string)

        print(Fore.CYAN + "Wrote Stats for Iteration: ", i)
        print(Fore.RESET)
