
from gen_oplist import print_title, print_hline


def print_file(file):

    print('.. _typelist:\n\n', file=file)

    print_title(file, "Type List", "~", "~")

    print("*THIS PAGE IS A PLACEHOLDER: WRITEME*", file=file)
    print("", file=file)
    print_hline(file)

    print("", file=file)
    print(".. contents::", file=file)
    print("", file=file)

    print_title(file, "Type Classes", '=')

    print("- scalar.Scalar\n", file=file)
    print("- tensor.Tensor\n", file=file)
    print("- sparse.Sparse\n", file=file)

    print_title(file, "Type Instances", '=')

    print("- scalar.int8\n", file=file)
    print("- tensor.lvector\n", file=file)
    print("- sparse.??\n", file=file)

    print("", file=file)


if __name__ == '__main__':

    if len(sys.argv) >= 2:
        file = open(sys.argv[1], 'w')
    else:
        file = sys.stdout

    print_file(file)
