# Verification Assignment

This assignment will help you get familiar with how to model simple network functionality in first-order logic and use the [Z3 theoram prover](https://github.com/Z3Prover/z3) to automatically reason about it.

**This assignment is optional and can count as 5% extra credit towards your final grade. Due date is April 17.**

## Obtaining required software

### Python3

You need Python3 to be able to run this exericse.

### Z3 Theorem Prover

Install Z3 and its python wrapper by following the instructions on its [github repository](https://github.com/Z3Prover/z3):

- You will need to provide a special flag when building Z3 to be able to use the python wrapper.
- The python wrapper itself can be installed using `pip`.


## Warmup

The file `warmup.py` contains three examples, increasing in complexity, to help familiarize you with how to express what you want to analyze in logic and use Z3's python API to reason about it. 

## Reasoning about forwarding behavior

In this exercise, we will use Z3 to reason about a simple forwarding information base (FIB). Our FIB is a table with rules that match on the destination IP prefix and assign an output port to the packet accordingly:

| IP         | Prefix Length | Output Port |
| -----------|-------------- | ------------| 
| 10.0.0.1   | 24            | 2           |
| 128.1.10.2 | 31            | 10          |
| 7.6.5.3    | 20            | 3           |
| 128.1.0.0  | 16            | 1           |

For modeling purposes, we assume that **if the output port is set to 10, the packet will be dropped**. The packet will also be dropped if it's destination IP address does not match any of the prefixes specified by the rules in the table. 

Note that the rules are **prioritized** by their order. The rules that appear earlier have higher priorities. If a packet matches more than one rule, it will be assigned an output port based on the rule that appears earlier than the others. 

We would like to model the forwarding behavior that results from this table in logic, and given a IP prefix $p$, we would like to be able to ask the following query:

*Would any packets whose destination IP address belongs to p be dropped by this table?*

The starter code can be found in `fib.py`:

- Similar to the example we saw in lecture 7 from the Anteater paper, our forwarding table only cares about destination IP addresses. As such, we will only model the destination IP address in the packet header.
- IP addresses have 32 bits. So, we model the destination IP address of a packet as 32 boolean variables (`dstip_vars`), where the $i$th variable corresponds to the $i$th bit in the destination IP address. 
- We model the output port assigned to an incoming packet as an integer variable called `output_port`. 
- There is a helper function, `dstip_matches_prefix`, that takes the above variables (`dstip_vars`) and an IP prefix as input and returns a formula that evaluates to true if the relevant variables in `dstip_vars` are equal to that of the prefix.
- The `create_fib_model` function takes the name of the file containing the rules (in our case, `rules.txt`) and returns a formula that captures the behavior of the forwarding table. Here, as marked by TODOs in the file, you will need to create the sub-formulas needed to do so.
- The `check_property` function takes `dstip_vars`, `output_port`, and `fib_model`, as well as the prefix whose packets we would like to make sure are not dropped. In this function, you need to construct the formula we will hand to Z3 to help us do that analysis. 

### Running the exercise

The file `run.py` calls `create_fib_model` to get the necessary logical variables, and then calls `check_property` a few times with different prefixes. So, to run the exercise, you can simply run ```python3 run.py```.
