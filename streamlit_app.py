import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os
from mcculloch_pitts_nand import (
    McCullochPittsNeuron,
    NANDNeuron,
    mp_not_gate,
    mp_and_gate,
    mp_or_gate,
    mp_xor_gate,
    mp_xnor_gate,
    IndustrialSafetySystem
)

# Page configuration
st.set_page_config(
    page_title="McCulloch-Pitts NAND Neuron & Universal AI Lab",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #9d4edd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-box {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 18px;
        backdrop-filter: blur(10px);
        text-align: center;
    }
    .highlight-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/artificial-intelligence.png", width=70)
    st.title("MP Neuron Lab")
    st.caption("Neural Networks & Deep Learning • TAE-1 PBL")
    st.markdown("---")
    
    st.markdown("### 📌 Navigation")
    tab_choice = st.radio(
        "Select Module:",
        [
            "🧠 1. NAND Neuron Visualizer",
            "🧮 2. Mathematical Foundations",
            "🌐 3. Universal Logic Synthesizer",
            "🏭 4. Industrial Safety Project",
            "📄 5. Project Report & Download"
        ]
    )
    st.markdown("---")
    st.info("💡 **McCulloch-Pitts Neuron (1943):** Binary threshold device capable of universal computation when calibrated as a NAND gate.")

# Header
st.markdown('<div class="main-title">McCulloch-Pitts Neuron: NAND Gate & Universal AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive Laboratory for Project-Based Learning in Neural Networks</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 1: NAND NEURON VISUALIZER
# -------------------------------------------------------------
if "1. NAND Neuron" in tab_choice:
    st.header("🧠 1. McCulloch-Pitts NAND Neuron Visualizer")
    st.markdown("Explore how input signals, synaptic weights, and threshold determine neuron firing behavior.")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("⚙️ Neuron Parameters")
        
        c_in1, c_in2 = st.columns(2)
        with c_in1:
            x1 = st.selectbox("Input $x_1$", [0, 1], index=0)
        with c_in2:
            x2 = st.selectbox("Input $x_2$", [0, 1], index=0)
            
        c_w1, c_w2 = st.columns(2)
        with c_w1:
            w1 = st.slider("Weight $w_1$", min_value=-3.0, max_value=3.0, value=-1.0, step=0.5)
        with c_w2:
            w2 = st.slider("Weight $w_2$", min_value=-3.0, max_value=3.0, value=-1.0, step=0.5)
            
        theta = st.slider("Threshold $\\theta$", min_value=-3.0, max_value=3.0, value=-1.0, step=0.5)
        
        # Calculations
        z = w1 * x1 + w2 * x2
        fired = 1 if z >= theta else 0
        
        st.markdown("---")
        st.subheader("📊 Live Computation Breakdown")
        st.latex(rf"z = ({w1} \times {x1}) + ({w2} \times {x2}) = {z:.1f}")
        st.latex(rf"\text{{Condition: }} z \ge \theta \implies {z:.1f} \ge {theta:.1f} \implies \mathbf{{{bool(z >= theta)}}}")
        
        if fired == 1:
            st.success(f"🔥 **Neuron FIRED (Output y = 1)**")
        else:
            st.error(f"❄️ **Neuron INACTIVE (Output y = 0)**")
            
    with col2:
        st.subheader("📈 Heaviside Step Activation Function")
        
        # Plotly Step Function Chart
        z_vals = np.linspace(-3.5, 3.5, 300)
        y_vals = np.where(z_vals >= theta, 1, 0)
        
        fig = go.Figure()
        
        # Background step curve
        fig.add_trace(go.Scatter(
            x=z_vals, y=y_vals,
            mode='lines',
            name='Step Activation f(z)',
            line=dict(color='#00f2fe', width=3)
        ))
        
        # Threshold line
        fig.add_vline(x=theta, line_dash="dash", line_color="#f59e0b", annotation_text=f"Threshold θ={theta:.1f}")
        
        # Current Operating Point
        fig.add_trace(go.Scatter(
            x=[z], y=[fired],
            mode='markers+text',
            name='Current State',
            text=[f"z={z:.1f}, y={fired}"],
            textposition="top right",
            marker=dict(size=14, color='#ef4444' if fired==0 else '#10b981', symbol='diamond')
        ))
        
        fig.update_layout(
            title="Activation Curve: y = f(z - θ)",
            xaxis_title="Weighted Sum (z)",
            yaxis_title="Output (y)",
            yaxis=dict(range=[-0.2, 1.3], tickvals=[0, 1]),
            template="plotly_dark",
            margin=dict(l=40, r=40, t=40, b=40),
            height=340
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Truth Table Evaluation
        st.subheader("📋 Truth Table Verification (All 4 states)")
        tt_data = []
        for inp1, inp2 in [(0,0), (0,1), (1,0), (1,1)]:
            calc_z = w1 * inp1 + w2 * inp2
            calc_out = 1 if calc_z >= theta else 0
            nand_target = 1 if not (inp1 == 1 and inp2 == 1) else 0
            match = "✅" if calc_out == nand_target else "❌"
            tt_data.append({
                "x1": inp1,
                "x2": inp2,
                "z = w1*x1 + w2*x2": f"{calc_z:.1f}",
                "z >= θ": f"{calc_z:.1f} >= {theta:.1f}",
                "Output y": calc_out,
                "Target NAND": nand_target,
                "Status": match
            })
        st.dataframe(pd.DataFrame(tt_data), use_container_width=True, hide_index=True)

# -------------------------------------------------------------
# TAB 2: MATHEMATICAL FOUNDATIONS
# -------------------------------------------------------------
elif "2. Mathematical Foundations" in tab_choice:
    st.header("🧮 2. Theoretical Derivation & Mathematical Proof")
    
    st.markdown(r"""
    ### 1. McCulloch-Pitts Mathematical Model (1943)
    For binary inputs $x_i \in \{0, 1\}$, real weights $w_i$, and threshold $\theta$:
    """)
    st.latex(r"z = \sum_{i=1}^{n} w_i x_i")
    st.latex(r"y = f(z) = \begin{cases} 1 & \text{if } z \ge \theta \\ 0 & \text{if } z < \theta \end{cases}")
    
    st.markdown(r"""
    ### 2. NAND Gate Constraint System
    A 2-input NAND gate must satisfy the following 4 simultaneous linear inequalities:
    """)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(r"""
        1. **Input (0, 0) $\implies y = 1$:**
           $$w_1(0) + w_2(0) \ge \theta \implies \mathbf{0 \ge \theta}$$
        2. **Input (0, 1) $\implies y = 1$:**
           $$w_1(0) + w_2(1) \ge \theta \implies \mathbf{w_2 \ge \theta}$$
        """)
    with c2:
        st.markdown(r"""
        3. **Input (1, 0) $\implies y = 1$:**
           $$w_1(1) + w_2(0) \ge \theta \implies \mathbf{w_1 \ge \theta}$$
        4. **Input (1, 1) $\implies y = 0$:**
           $$w_1(1) + w_2(1) < \theta \implies \mathbf{w_1 + w_2 < \theta}$$
        """)
        
    st.markdown(r"""
    ### 3. Canonical Parameter Solution
    Choosing symmetric inhibitory synaptic weights **$w_1 = -1.0, w_2 = -1.0$** and activation threshold **$\theta = -1.0$**:
    """)
    
    proof_df = pd.DataFrame([
        {"Input (x1, x2)": "(0, 0)", "Calculation z": "(-1)(0) + (-1)(0) = 0.0", "Inequality Check": "0.0 >= -1.0 (TRUE)", "Output y": 1, "NAND Spec": 1, "Status": "PASS ✅"},
        {"Input (x1, x2)": "(0, 1)", "Calculation z": "(-1)(0) + (-1)(1) = -1.0", "Inequality Check": "-1.0 >= -1.0 (TRUE)", "Output y": 1, "NAND Spec": 1, "Status": "PASS ✅"},
        {"Input (x1, x2)": "(1, 0)", "Calculation z": "(-1)(1) + (-1)(0) = -1.0", "Inequality Check": "-1.0 >= -1.0 (TRUE)", "Output y": 1, "NAND Spec": 1, "Status": "PASS ✅"},
        {"Input (x1, x2)": "(1, 1)", "Calculation z": "(-1)(1) + (-1)(1) = -2.0", "Inequality Check": "-2.0 >= -1.0 (FALSE)", "Output y": 0, "NAND Spec": 0, "Status": "PASS ✅"}
    ])
    st.table(proof_df)

# -------------------------------------------------------------
# TAB 3: UNIVERSAL LOGIC SYNTHESIZER
# -------------------------------------------------------------
elif "3. Universal Logic Synthesizer" in tab_choice:
    st.header("🌐 3. Universal Gate Synthesis (All from MP NAND Neurons)")
    st.markdown("NAND is a **functionally complete** universal gate. Any logic circuit can be synthesized exclusively using MP NAND neurons.")
    
    gate_choice = st.selectbox("Select Synthesized Gate:", ["NOT Gate (1 NAND)", "AND Gate (2 NANDs)", "OR Gate (3 NANDs)", "XOR Gate (4 NANDs)", "XNOR Gate (5 NANDs)"])
    
    col_in, col_res = st.columns([1, 1.5])
    
    with col_in:
        st.subheader("Input Values")
        if "NOT" in gate_choice:
            in_a = st.radio("Input X", [0, 1], horizontal=True)
            in_b = in_a
            out = mp_not_gate(in_a)
        else:
            in_a = st.radio("Input X1", [0, 1], horizontal=True)
            in_b = st.radio("Input X2", [0, 1], horizontal=True)
            
            if "AND" in gate_choice:
                out = mp_and_gate(in_a, in_b)
            elif "OR" in gate_choice:
                out = mp_or_gate(in_a, in_b)
            elif "XOR" in gate_choice:
                out = mp_xor_gate(in_a, in_b)
            else:
                out = mp_xnor_gate(in_a, in_b)
                
        st.markdown("---")
        st.metric(label=f"Synthesized Output", value=f"y = {out}")
        
    with col_res:
        st.subheader("Circuit Architecture & Mathematical Formulation")
        if "NOT" in gate_choice:
            st.info("💡 **Formula:** $y = \\text{NAND}(x, x)$")
            st.markdown("- **Neuron Count:** 1 MP NAND Neuron")
        elif "AND" in gate_choice:
            st.info("💡 **Formula:** $y = \\text{NAND}(\\text{NAND}(x_1, x_2), \\text{NAND}(x_1, x_2))$")
            st.markdown("- **Neuron Count:** 2 MP NAND Neurons (Layer 1 + Inverter)")
        elif "OR" in gate_choice:
            st.info("💡 **Formula:** $y = \\text{NAND}(\\text{NAND}(x_1, x_1), \\text{NAND}(x_2, x_2))$")
            st.markdown("- **Neuron Count:** 3 MP NAND Neurons (De Morgan's Theorem)")
        elif "XOR" in gate_choice:
            st.info("💡 **Formula:** $y = \\text{NAND}(\\text{NAND}(x_1, N_1), \\text{NAND}(x_2, N_1))$ where $N_1 = \\text{NAND}(x_1, x_2)$")
            st.markdown("- **Neuron Count:** 4 MP NAND Neurons (Solves Non-Linear Separability!)")
        else:
            st.info("💡 **Formula:** $y = \\text{NOT}(\\text{XOR}(x_1, x_2))$")
            st.markdown("- **Neuron Count:** 5 MP NAND Neurons")
            
        # Full truth table for selected gate
        st.markdown("**Complete Gate Truth Table:**")
        if "NOT" in gate_choice:
            table_records = [{"X": i, "Synthesized Output y": mp_not_gate(i)} for i in [0, 1]]
        elif "AND" in gate_choice:
            table_records = [{"X1": i, "X2": j, "Output y": mp_and_gate(i, j)} for i, j in [(0,0), (0,1), (1,0), (1,1)]]
        elif "OR" in gate_choice:
            table_records = [{"X1": i, "X2": j, "Output y": mp_or_gate(i, j)} for i, j in [(0,0), (0,1), (1,0), (1,1)]]
        elif "XOR" in gate_choice:
            table_records = [{"X1": i, "X2": j, "Output y": mp_xor_gate(i, j)} for i, j in [(0,0), (0,1), (1,0), (1,1)]]
        else:
            table_records = [{"X1": i, "X2": j, "Output y": mp_xnor_gate(i, j)} for i, j in [(0,0), (0,1), (1,0), (1,1)]]
            
        st.dataframe(pd.DataFrame(table_records), use_container_width=True, hide_index=True)

# -------------------------------------------------------------
# TAB 4: INDUSTRIAL SAFETY PROJECT
# -------------------------------------------------------------
elif "4. Industrial Safety Project" in tab_choice:
    st.header("🏭 4. Real-World Project: Industrial Stamping Press Safety System")
    st.markdown("""
    **Problem Statement:** An automated high-tonnage sheet metal stamping press presents high amputation risks. 
    It requires a fail-safe neural interlock controller built using McCulloch-Pitts neurons.
    """)
    
    col_sim1, col_sim2 = st.columns([1, 1.2])
    
    with col_sim1:
        st.subheader("🎛️ Safety Sensors Control Panel")
        
        guard = st.toggle("🛡️ Safety Enclosure Guard (1 = Closed, 0 = Open)", value=True)
        buttons = st.toggle("✋ Two-Hand Operator Buttons (1 = Both Pressed)", value=True)
        estop = st.toggle("🚨 Emergency Stop Button (1 = Active / Pressed)", value=False)
        
        guard_val = 1 if guard else 0
        btn_val = 1 if buttons else 0
        estop_val = 1 if estop else 0
        
        system = IndustrialSafetySystem()
        result = system.evaluate(guard_val, btn_val, estop_val)
        
    with col_sim2:
        st.subheader("⚙️ Real-time Neural Interlock Status")
        
        st.markdown(f"**Stage 1 (Operational Clearance AND Gate):** `Output = {result['stage1_clearance']}`")
        st.markdown(f"**Stage 2 (Inhibitory Interlock with E-Stop):** `Output = {result['press_clearance']}`")
        
        if result['safe_to_operate']:
            st.success("🟢 **PRESS AUTHORIZED & OPERATING SAFELY**\n\nAll safety interlocks satisfied. Ram cycle cleared.")
        elif estop_val == 1:
            st.error("🛑 **EMERGENCY STOP SHUTDOWN IN EFFECT!**\n\nInhibitory synapse instantly clamped motor drive to 0.")
        else:
            st.warning("⚠️ **SAFETY HAZARD: Press Inhibited!**\n\nEnsure guard door is closed and both operator buttons are pressed.")
            
        st.markdown("---")
        st.caption("Neural Architecture: 2 MP NAND Neurons forming AND gate + 1 MP Inhibitory Interlock Neuron.")

# -------------------------------------------------------------
# TAB 5: REPORT & DOWNLOAD
# -------------------------------------------------------------
elif "5. Project Report" in tab_choice:
    st.header("📄 5. Project Report & Academic Deliverables")
    st.markdown("Download the comprehensive project documentation and academic report PDF.")
    
    pdf_path = "McCulloch_Pitts_NAND_Neuron_Project_Report.pdf"
    
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
            
        st.download_button(
            label="📥 Download Full Project Report (PDF)",
            data=pdf_bytes,
            file_name="McCulloch_Pitts_NAND_Neuron_Project_Report.pdf",
            mime="application/pdf"
        )
        st.success(f"✅ Academic Report ready: `{pdf_path}` ({len(pdf_bytes) // 1024} KB)")
    else:
        st.warning("PDF report not found. Run `python generate_pdf_report.py` to generate it.")
        
    st.markdown("""
    ### 📚 Summary of Project Deliverables:
    1. **Mathematical Proofs:** System of linear inequalities for NAND parameter solutions.
    2. **Universal Computation:** Verification of NOT, AND, OR, XOR, and XNOR synthesized purely from MP NAND neurons.
    3. **Industrial Interlock Simulation:** Implementation of 2-stage neural safety controller.
    4. **Interactive Streamlit Lab:** Live educational and testing platform.
    """)
