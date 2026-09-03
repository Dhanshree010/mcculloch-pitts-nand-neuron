"""
McCulloch-Pitts Neuron Implementation for NAND Gate & Universal Logic Systems
Project-Based Learning Module for Neural Networks & Deep Learning

Author: Antigravity AI & Student
Date: 2026
"""

import math
from typing import List, Tuple, Dict, Union

class McCullochPittsNeuron:
    """
    A mathematical implementation of the McCulloch-Pitts (MP) Neuron (1943).
    
    Mathematical Model:
    -------------------
    Given binary inputs x_i in {0, 1}, weights w_i, and a threshold theta:
    
    1. Weighted Sum:
       z = sum(w_i * x_i)  for i = 1 to n
       
    2. Activation Function (Heaviside Step Function):
       y = 1  if z >= theta
       y = 0  if z < theta
       
    Additionally supports classic MP inhibitory inputs:
    If any inhibitory input is active (1), the output is immediately suppressed (0).
    """

    def __init__(
        self,
        weights: List[float],
        threshold: float,
        name: str = "MP_Neuron",
        inhibitory_indices: List[int] = None
    ):
        """
        Initialize the McCulloch-Pitts Neuron.
        
        :param weights: List of numerical weights for each input.
        :param threshold: Numerical threshold theta for activation.
        :param name: Identifier name for the neuron node.
        :param inhibitory_indices: List of input indices that act as absolute inhibitory inputs.
        """
        self.weights = list(weights)
        self.threshold = float(threshold)
        self.name = name
        self.inhibitory_indices = set(inhibitory_indices) if inhibitory_indices else set()

    def activate(self, inputs: List[int]) -> int:
        """
        Compute the neuron output for given binary inputs.
        
        :param inputs: List of binary inputs (0 or 1).
        :return: Binary output (0 or 1).
        """
        if len(inputs) != len(self.weights):
            raise ValueError(
                f"Input length ({len(inputs)}) must match weight vector length ({len(self.weights)})"
            )

        # Check for absolute inhibitory inputs (Classic MP rule)
        for idx in self.inhibitory_indices:
            if inputs[idx] == 1:
                return 0

        # Calculate weighted sum z = sum(w_i * x_i)
        weighted_sum = sum(w * x for w, x in zip(self.weights, inputs))

        # Heaviside Step Activation Function
        return 1 if weighted_sum >= self.threshold else 0

    def inspect(self, inputs: List[int]) -> Dict[str, Union[int, float, bool, str]]:
        """
        Inspect detailed step-by-step evaluation for educational debugging.
        """
        if len(inputs) != len(self.weights):
            raise ValueError("Input dimensions mismatch.")

        inhibited = any(inputs[i] == 1 for i in self.inhibitory_indices)
        weighted_sum = sum(w * x for w, x in zip(self.weights, inputs))
        output = 0 if inhibited else (1 if weighted_sum >= self.threshold else 0)

        step_breakdown = []
        for i, (w, x) in enumerate(zip(self.weights, inputs)):
            is_inhib = i in self.inhibitory_indices
            step_breakdown.append(f"x_{i+1}={x} (w_{i+1}={w}{' [INHIB]' if is_inhib else ''})")

        return {
            "neuron": self.name,
            "inputs": inputs,
            "weights": self.weights,
            "threshold": self.threshold,
            "inhibited": inhibited,
            "weighted_sum": weighted_sum,
            "condition": f"{weighted_sum} >= {self.threshold}",
            "output": output,
            "breakdown": step_breakdown
        }


# =====================================================================
# Factory Functions for Standard Logic Gates using MP Neurons
# =====================================================================

def create_nand_neuron() -> McCullochPittsNeuron:
    """
    Creates a McCulloch-Pitts Neuron configured as a NAND Gate.
    
    Derivation:
    -----------
    Truth Table for NAND:
    x1 | x2 | NAND(x1, x2)
    -----------------------
     0 |  0 |      1
     0 |  1 |      1
     1 |  0 |      1
     1 |  1 |      0
     
    Using Weights w1 = -1, w2 = -1 and Threshold theta = -1:
    - (0, 0) => z = (-1)(0) + (-1)(0) =  0 >= -1 => Output 1
    - (0, 1) => z = (-1)(0) + (-1)(1) = -1 >= -1 => Output 1
    - (1, 0) => z = (-1)(1) + (-1)(0) = -1 >= -1 => Output 1
    - (1, 1) => z = (-1)(1) + (-1)(1) = -2 <  -1 => Output 0
    """
    return McCullochPittsNeuron(weights=[-1.0, -1.0], threshold=-1.0, name="NAND_Neuron")


def create_and_neuron() -> McCullochPittsNeuron:
    """
    Creates a direct MP Neuron for AND Gate.
    w1 = 1, w2 = 1, theta = 2
    """
    return McCullochPittsNeuron(weights=[1.0, 1.0], threshold=2.0, name="AND_Neuron")


def create_or_neuron() -> McCullochPittsNeuron:
    """
    Creates a direct MP Neuron for OR Gate.
    w1 = 1, w2 = 1, theta = 1
    """
    return McCullochPittsNeuron(weights=[1.0, 1.0], threshold=1.0, name="OR_Neuron")


def create_not_neuron() -> McCullochPittsNeuron:
    """
    Creates a direct MP Neuron for NOT Gate.
    w = -1, theta = 0
    """
    return McCullochPittsNeuron(weights=[-1.0], threshold=0.0, name="NOT_Neuron")


# =====================================================================
# Universal Gate Synthesizer: Building All Gates using ONLY NAND Neurons
# =====================================================================

class NANDUniversalSynthesizer:
    """
    Demonstrates the functional universality of the NAND McCulloch-Pitts Neuron.
    Every basic logic gate (NOT, AND, OR, XOR, XNOR) is constructed exclusively
    from interconnected NAND MP neurons.
    """

    @staticmethod
    def NOT(x: int) -> int:
        """
        NOT(x) = NAND(x, x)
        """
        nand = create_nand_neuron()
        return nand.activate([x, x])

    @staticmethod
    def AND(x1: int, x2: int) -> int:
        """
        AND(x1, x2) = NOT(NAND(x1, x2)) = NAND(NAND(x1, x2), NAND(x1, x2))
        """
        nand1 = create_nand_neuron()
        nand2 = create_nand_neuron()
        
        stage1 = nand1.activate([x1, x2])
        stage2 = nand2.activate([stage1, stage1])
        return stage2

    @staticmethod
    def OR(x1: int, x2: int) -> int:
        """
        OR(x1, x2) = NAND(NOT(x1), NOT(x2)) = NAND(NAND(x1, x1), NAND(x2, x2))
        """
        nand_not1 = create_nand_neuron()
        nand_not2 = create_nand_neuron()
        nand_out = create_nand_neuron()

        not_x1 = nand_not1.activate([x1, x1])
        not_x2 = nand_not2.activate([x2, x2])
        return nand_out.activate([not_x1, not_x2])

    @staticmethod
    def XOR(x1: int, x2: int) -> int:
        """
        XOR(x1, x2) implemented using 4 NAND MP Neurons.
        Stage 1: N1 = NAND(x1, x2)
        Stage 2: N2 = NAND(x1, N1), N3 = NAND(x2, N1)
        Stage 3: Output = NAND(N2, N3)
        """
        n1 = create_nand_neuron().activate([x1, x2])
        n2 = create_nand_neuron().activate([x1, n1])
        n3 = create_nand_neuron().activate([x2, n1])
        out = create_nand_neuron().activate([n2, n3])
        return out

    @staticmethod
    def XNOR(x1: int, x2: int) -> int:
        """
        XNOR(x1, x2) = NOT(XOR(x1, x2)) using 5 NAND MP Neurons.
        """
        xor_val = NANDUniversalSynthesizer.XOR(x1, x2)
        return NANDUniversalSynthesizer.NOT(xor_val)


# =====================================================================
# Real-World Project: Industrial Automated Press Safety Interlock System
# =====================================================================

class IndustrialPressSafetySystem:
    """
    Project Application: Industrial Power Press Emergency Interlock Controller.
    
    Real-World Problem:
    In a heavy manufacturing facility, a heavy stamping press must operate safely.
    The machine should run (Output = 1) ONLY when safety conditions are met.
    
    Sensors:
    - Sensor A (Safety Guard In Place): 1 if guard closed, 0 if open.
    - Sensor B (Operator Two-Hand Buttons Active): 1 if dual buttons pressed, 0 otherwise.
    - Emergency Override Stop (E-Stop): 1 if pressed (danger!), 0 if normal.
    
    Safety Requirement:
    The press is ALLOWED TO RUN if Safety Guard IS closed AND Dual Buttons ARE pressed,
    UNLESS E-Stop is engaged.
    
    Using NAND MP Neuron logic:
    We can construct the safety interlock using McCulloch-Pitts NAND neurons!
    """

    def __init__(self):
        self.nand = create_nand_neuron()

    def evaluate_system(self, guard_closed: int, buttons_pressed: int, emergency_stop: int) -> Dict[str, Union[int, str]]:
        """
        Evaluates the industrial press operation state using McCulloch-Pitts NAND network.
        
        Logic:
        1. Normal Operation Signal: AND(guard_closed, buttons_pressed)
           = NAND( NAND(guard_closed, buttons_pressed), NAND(guard_closed, buttons_pressed) )
        2. Emergency Inhibition Signal:
           If Emergency Stop = 1, force state to 0.
        """
        # Step 1: Compute NAND(guard_closed, buttons_pressed)
        stage1_nand = self.nand.activate([guard_closed, buttons_pressed])
        
        # Step 2: Invert to get AND result (normal operational clearance)
        normal_clearance = self.nand.activate([stage1_nand, stage1_nand])
        
        # Step 3: Emergency Override - using MP Inhibitory Neuron rule
        # Inhibitory neuron: clearance signal is input, e-stop is inhibitory input
        safety_interlock_neuron = McCullochPittsNeuron(
            weights=[1.0, 0.0],
            threshold=1.0,
            name="Safety_Interlock_Final",
            inhibitory_indices=[1]  # Index 1 (emergency_stop) is absolute inhibitor
        )
        
        press_permission = safety_interlock_neuron.activate([normal_clearance, emergency_stop])
        
        status_msg = (
            "PRESS AUTHORIZED & OPERATING SAFELY" if press_permission == 1
            else ("EMERGENCY STOP SHUTDOWN IN EFFECT!" if emergency_stop == 1
                  else "SAFETY HAZARD: Guard open or buttons released!")
        )

        return {
            "guard_closed": guard_closed,
            "buttons_pressed": buttons_pressed,
            "emergency_stop": emergency_stop,
            "normal_clearance_signal": normal_clearance,
            "press_permission": press_permission,
            "status_message": status_msg
        }


# =====================================================================
# Verification & Test Suite
# =====================================================================

def run_tests_and_demonstration():
    """
    Executes automated tests verifying NAND MP Neuron truth tables,
    Universal Gate Synthesizer correctness, and Industrial Safety System simulation.
    """
    print("=" * 70)
    print(" MCCULLOCH-PITTS NEURON - NAND GATE & PROJECT IMPLEMENTATION")
    print("=" * 70)
    
    # 1. Verify NAND Gate Truth Table
    nand_neuron = create_nand_neuron()
    print("\n1. Testing McCulloch-Pitts NAND Neuron (w1=-1, w2=-1, theta=-1):")
    print("-" * 55)
    print(" x1 | x2 | Weighted Sum z | Condition z >= -1 | Output")
    print("-" * 55)
    
    expected_nand = [(0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
    for x1, x2, expected in expected_nand:
        info = nand_neuron.inspect([x1, x2])
        out = info["output"]
        assert out == expected, f"Failed NAND for ({x1}, {x2}): got {out}, expected {expected}"
        z = info["weighted_sum"]
        cond = "TRUE (>= -1)" if z >= -1 else "FALSE (< -1)"
        print(f"  {x1} |  {x2} |      {z:2.1f}       |   {cond:15s} |   {out}")
    print("=> All NAND MP Neuron tests PASSED successfully!\n")

    # 2. Verify Universal Gates Synthesized from NAND Neurons
    print("2. Testing Universal Logic Gates Synthesized EXCLUSIVELY from MP NAND Neurons:")
    print("-" * 65)
    
    # NOT Test
    not_results = [(0, 1), (1, 0)]
    for x, exp in not_results:
        res = NANDUniversalSynthesizer.NOT(x)
        assert res == exp, f"NOT({x}) failed: got {res}"
    print("  [OK] NOT Gate via NAND:  PASSED")

    # AND Test
    and_results = [((0, 0), 0), ((0, 1), 0), ((1, 0), 0), ((1, 1), 1)]
    for (x1, x2), exp in and_results:
        res = NANDUniversalSynthesizer.AND(x1, x2)
        assert res == exp, f"AND({x1},{x2}) failed: got {res}"
    print("  [OK] AND Gate via NAND:  PASSED")

    # OR Test
    or_results = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)]
    for (x1, x2), exp in or_results:
        res = NANDUniversalSynthesizer.OR(x1, x2)
        assert res == exp, f"OR({x1},{x2}) failed: got {res}"
    print("  [OK] OR Gate via NAND:   PASSED")

    # XOR Test
    xor_results = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]
    for (x1, x2), exp in xor_results:
        res = NANDUniversalSynthesizer.XOR(x1, x2)
        assert res == exp, f"XOR({x1},{x2}) failed: got {res}"
    print("  [OK] XOR Gate via NAND:  PASSED")

    # XNOR Test
    xnor_results = [((0, 0), 1), ((0, 1), 0), ((1, 0), 0), ((1, 1), 1)]
    for (x1, x2), exp in xnor_results:
        res = NANDUniversalSynthesizer.XNOR(x1, x2)
        assert res == exp, f"XNOR({x1},{x2}) failed: got {res}"
    print("  [OK] XNOR Gate via NAND: PASSED")

    # 3. Real-World Project Simulation
    print("\n3. Real-World Project: Industrial Stamping Press Safety System:")
    print("-" * 75)
    safety_sys = IndustrialPressSafetySystem()
    scenarios = [
        (1, 1, 0, "Guard closed, Dual buttons pressed, No E-Stop"),
        (1, 0, 0, "Guard closed, Buttons released, No E-Stop"),
        (0, 1, 0, "Guard OPEN, Dual buttons pressed, No E-Stop"),
        (1, 1, 1, "Guard closed, Buttons pressed BUT E-STOP PRESSED!"),
    ]
    
    for guard, buttons, estop, desc in scenarios:
        res = safety_sys.evaluate_system(guard, buttons, estop)
        print(f" Scenario: {desc}")
        print(f"   [Inputs] Guard={guard}, Buttons={buttons}, E-Stop={estop}")
        print(f"   [Output] Press Clearance={res['press_permission']} -> {res['status_message']}\n")

    print("=" * 70)
    print(" ALL TESTS AND DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests_and_demonstration()
