from solution import *

if __name__ == "__main__":
    dstip_vars, output_port, fib_model = create_fib_model("rules.txt")
 
    check_property(dstip_vars, output_port, fib_model,
                   IPPrefix("127.0.0.0", 8))

    check_property(dstip_vars, output_port, fib_model,
                   IPPrefix("7.6.5.3", 16))

    check_property(dstip_vars, output_port, fib_model,
                   IPPrefix("10.0.127.0", 17))
