# McCulloch-Pitts Neuron for NAND Gate & Universal Computation

[![GitHub Pages Deployment](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen?style=for-the-badge&logo=github)](https://dhanshree010.github.io/mcculloch-pitts-nand-neuron/)
[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://python.org)
[![HTML5 / CSS3 / JS](https://img.shields.io/badge/Web%20Lab-HTML5%20%7C%20CSS3%20%7C%20JS-orange?style=for-the-badge)](https://dhanshree010.github.io/mcculloch-pitts-nand-neuron/)

> **Course:** Neural Networks and Deep Learning  
> **Topic:** Project-Based Learning (PBL)  
> **Live Demo:** [https://dhanshree010.github.io/mcculloch-pitts-nand-neuron/](https://dhanshree010.github.io/mcculloch-pitts-nand-neuron/)  
> **Author:** Antigravity AI & Student  
> **Repository Scope:** Python Implementation, Mathematical Derivations, Interactive Visual Web Lab, and Real-World Safety System Project.


---

## 📌 Executive Summary

The **McCulloch-Pitts (MP) Neuron** (1943) is the fundamental building block of artificial neural network theory. This project implements a computational McCulloch-Pitts neuron specifically calibrated for the **NAND Gate**, demonstrates the **functional universality** of NAND MP neurons (building NOT, AND, OR, XOR, XNOR logic gates exclusively from NAND neurons), and applies this logic to an **Industrial Stamping Press Emergency Safety Interlock System**.

---

## 🧮 1. Theoretical Foundation & Mathematical Proof

### McCulloch-Pitts Neuron Model
Given binary inputs $x_i \in \{0, 1\}$, real-valued weights $w_i$, and activation threshold $\theta$:

$$z = \sum_{i=1}^{n} w_i x_i$$

$$y = f(z) = \begin{cases} 1 & \text{if } z \ge \theta \\ 0 & \text{if } z < \theta \end{cases}$$

### NAND Gate Truth Table
| $x_1$ | $x_2$ | Target Output $y = \text{NAND}(x_1, x_2)$ |
|:---:|:---:|:---:|
| 0 | 0 | **1** |
| 0 | 1 | **1** |
| 1 | 0 | **1** |
| 1 | 1 | **0** |

### Derivation of System Inequalities
To satisfy the truth table, the weights $w_1, w_2$ and threshold $\theta$ must fulfill:
1. $x=(0,0): w_1(0) + w_2(0) \ge \theta \implies 0 \ge \theta$
2. $x=(0,1): w_1(0) + w_2(1) \ge \theta \implies w_2 \ge \theta$
3. $x=(1,0): w_1(1) + w_2(0) \ge \theta \implies w_1 \ge \theta$
4. $x=(1,1): w_1(1) + w_2(1) < \theta \implies w_1 + w_2 < \theta$

### Canonical Parameter Solution
Setting **$w_1 = -1.0, w_2 = -1.0, \theta = -1.0$**:
- **(0,0):** $z = (-1)(0) + (-1)(0) = 0.0 \ge -1.0 \implies y = 1$ ✅
- **(0,1):** $z = (-1)(0) + (-1)(1) = -1.0 \ge -1.0 \implies y = 1$ ✅
- **(1,0):** $z = (-1)(1) + (-1)(0) = -1.0 \ge -1.0 \implies y = 1$ ✅
- **(1,1):** $z = (-1)(1) + (-1)(1) = -2.0 < -1.0 \implies y = 0$ ✅

---

## 🌐 2. Universal Gate Synthesis using MP NAND Neurons

Because the NAND gate is functionally complete, any digital logic gate can be synthesized strictly out of McCulloch-Pitts NAND neurons:

- **NOT Gate:** $y = \text{NAND}(x, x)$ *(1 NAND)*
- **AND Gate:** $y = \text{NAND}(\text{NAND}(x_1, x_2), \text{NAND}(x_1, x_2))$ *(2 NANDs)*
- **OR Gate:** $y = \text{NAND}(\text{NAND}(x_1, x_1), \text{NAND}(x_2, x_2))$ *(3 NANDs)*
- **XOR Gate:** $y = \text{NAND}(\text{NAND}(x_1, N_1), \text{NAND}(x_2, N_1))$ where $N_1 = \text{NAND}(x_1, x_2)$ *(4 NANDs)*
- **XNOR Gate:** $y = \text{NOT}(\text{XOR}(x_1, x_2))$ *(5 NANDs)*

---

## 🏭 3. Real-World Project: Industrial Stamping Press Safety System

### Operational Requirements
An automated industrial stamping press must operate (Clearance = 1) ONLY when:
1. **Safety Enclosure Guard** is closed ($x_1 = 1$).
2. **Two-Hand Operator Buttons** are pressed simultaneously ($x_2 = 1$).
3. **Emergency Stop (E-Stop)** is NOT engaged ($E = 0$).

### Neural Implementation
1. **Stage 1 (Clearance Check):** $\text{AND}(\text{Guard}, \text{Buttons})$ implemented via 2 MP NAND neurons.
2. **Stage 2 (Inhibitory Interlock):** An MP Neuron with threshold $\theta = 1.0$ taking Stage 1 output as input and Emergency Stop as an **absolute inhibitory connection**.

---

## 🚀 4. How to Run the Project

### Running the Python Engine & Test Suite
Execute the pure Python script to run automated unit tests, truth table evaluations, and safety project simulations:

```bash
python mcculloch_pitts_nand.py
```

### Opening the Interactive Web Visualizer Lab
Simply open `index.html` in any web browser:
- **Chrome / Edge / Firefox / Safari:** Double-click `index.html` or open via browser.
- Features real-time SVG neural connection pulse animations, threshold sliders, interactive truth tables, step-activation function chart, universal synthesizer playground, and animated power press safety simulator.

---

## 📂 5. Project Directory Structure

```
TAE1_PR/
├── mcculloch_pitts_nand.py   # Pure Python MP Neuron engine, NAND gate & safety project
├── index.html                # Main Interactive Lab Web Application
├── styles.css                # Sleek Glassmorphism Dark-Mode CSS Design System
├── app.js                    # Interactive JS simulation engine & SVG visualizer
└── README.md                 # Comprehensive project documentation & proofs
```

---
*Developed for Neural Networks & Deep Learning Coursework.*
