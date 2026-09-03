"""
PDF Generator for McCulloch-Pitts Neuron & NAND Gate Project Report
Generates a highly detailed, professional PDF document using ReportLab.
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute total page numbers and render running headers/footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress header/footer on cover/title section
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header
        self.drawString(54, 11 * 72 - 36, "McCulloch-Pitts Neuron & NAND Gate — Comprehensive PBL Report")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Running Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 36, page_str)
        self.drawString(54, 36, "Neural Networks & Deep Learning • Antigravity AI Lab")
        self.line(54, 48, 8.5 * 72 - 54, 48)

        self.restoreState()


def create_pdf_report(filename="McCulloch_Pitts_NAND_Neuron_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0F172A")    # Deep Navy
    SECONDARY = colors.HexColor("#0284C7")  # Cerulean Blue
    ACCENT = colors.HexColor("#7C3AED")     # Violet
    TEXT_DARK = colors.HexColor("#1E293B")  # Charcoal
    TEXT_MUTED = colors.HexColor("#475569") # Slate Gray
    BG_LIGHT = colors.HexColor("#F8FAFC")   # Off-white
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceAfter=20
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_MUTED
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=TEXT_DARK,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
        leftIndent=15,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0F172A")
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=PRIMARY
    )

    story = []

    # =========================================================================
    # COVER / HEADER SECTION
    # =========================================================================
    story.append(Paragraph("McCulloch-Pitts Neuron Model & NAND Gate Universal Computation", title_style))
    story.append(Paragraph("A Comprehensive Project-Based Learning (PBL) Report for Neural Networks & Deep Learning", subtitle_style))

    # Metadata Box
    meta_text = """
    <b>Course:</b> Neural Networks & Deep Learning (7th Sem) &nbsp;|&nbsp; 
    <b>Topic:</b> McCulloch-Pitts Neuron, NAND Gate & Universal Computation<br/>
    <b>Author:</b> Antigravity AI Lab & Student &nbsp;|&nbsp; 
    <b>Files Included:</b> <code>mcculloch_pitts_nand.py</code>, <code>index.html</code>, <code>styles.css</code>, <code>app.js</code>
    """
    meta_table = Table([[Paragraph(meta_text, meta_style)]], colWidths=[504])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('PADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # Executive Callout Banner
    exec_text = """
    <b>Executive Summary:</b> This report presents a rigorous, end-to-end investigation of the <b>McCulloch-Pitts (MP) Neuron (1943)</b> applied to the <b>NAND Logic Gate</b>. It covers the historical context, mathematical threshold derivation, proof of universal computation (building NOT, AND, OR, XOR, XNOR solely from NAND MP neurons), Python software implementation, an interactive visual Web application, and a real-world <b>Industrial Power Press Emergency Safety Interlock System</b> case study.
    """
    callout_table = Table([[Paragraph(exec_text, callout_style)]], colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F9FF")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BAE6FD")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 1: WHAT IS THE MCCULLOCH-PITTS NEURON & NAND GATE?
    # =========================================================================
    story.append(Paragraph("1. Conceptual Foundations: What is a McCulloch-Pitts Neuron?", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=2, spaceAfter=10))

    p1 = """
    Proposed by neurophysiologist <b>Warren McCulloch</b> and logician <b>Walter Pitts</b> in their seminal 1943 paper <i>"A Logical Calculus of the Ideas Immanent in Nervous Activity"</i>, the <b>McCulloch-Pitts (MP) Neuron</b> is the foundational computational abstraction of a biological neuron. It established that biological neural circuits could perform complex logical operations and laid the groundwork for artificial intelligence, threshold logic units (TLUs), and modern deep learning perceptrons.
    """
    story.append(Paragraph(p1, body_style))

    story.append(Paragraph("Mathematical Architecture of the MP Neuron", h2_style))
    p2 = """
    An MP neuron processes a vector of binary inputs <b>x</b> = (x₁, x₂, ..., xₙ) where xᵢ ∈ {0, 1}. The inputs pass through synaptic connections with numerical weights <b>w</b> = (w₁, w₂, ..., wₙ). The neuron computes the net scalar weighted sum <b>z</b> and passes it through a step function governed by a firing threshold <b>θ</b>:
    """
    story.append(Paragraph(p2, body_style))

    # Formula Box
    formula_text = """
    <b>Net Weighted Sum:</b> &nbsp;&nbsp; <i>z = ∑ᵢ₌₁ⁿ wᵢ xᵢ = w₁ x₁ + w₂ x₂ + ... + wₙ xₙ</i><br/><br/>
    <b>Heaviside Step Activation:</b> &nbsp;&nbsp; <i>y = f(z) = <b>1</b> if z ≥ θ else <b>0</b></i>
    """
    f_table = Table([[Paragraph(formula_text, ParagraphStyle('FormulaStyle', parent=body_style, fontName='Helvetica-Bold', textColor=ACCENT))]], colWidths=[504])
    f_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F3E8FF")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#DDD6FE")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(f_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("What is a NAND Gate?", h2_style))
    p3 = """
    The <b>NAND (NOT-AND) Gate</b> is a fundamental binary logic gate that outputs <b>0</b> if and only if all of its inputs are <b>1</b>. For all other input combinations, the NAND gate outputs <b>1</b>.
    """
    story.append(Paragraph(p3, body_style))

    # NAND Truth Table
    tt_data = [
        [Paragraph("<b>Input x₁</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY)),
         Paragraph("<b>Input x₂</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY)),
         Paragraph("<b>x₁ AND x₂</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY)),
         Paragraph("<b>NAND Output y = NOT(x₁ AND x₂)</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY))]
    ]
    tt_rows = [
        ["0", "0", "0", "1"],
        ["0", "1", "0", "1"],
        ["1", "0", "0", "1"],
        ["1", "1", "1", "0"]
    ]
    for r in tt_rows:
        tt_data.append([
            Paragraph(r[0], body_style),
            Paragraph(r[1], body_style),
            Paragraph(r[2], body_style),
            Paragraph(f"<b>{r[3]}</b>", ParagraphStyle('Out', parent=body_style, textColor=SECONDARY if r[3]=="1" else colors.HexColor("#DC2626")))
        ])

    tt_table = Table(tt_data, colWidths=[100, 100, 120, 184])
    tt_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(tt_table)
    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 2: WHY ARE WE USING THIS?
    # =========================================================================
    story.append(Paragraph("2. Pedagogical Motivation & Significance: Why are we using this?", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("1. The Principle of Functional Completeness (Universality)", h2_style))
    p_why1 = """
    In computer science and digital logic design, a set of logical operations is defined as <b>functionally complete</b> (or universal) if any possible Boolean function can be constructed using only elements from that set. The NAND gate is a <b>universal logic gate</b>. By implementing the NAND gate with a single McCulloch-Pitts neuron, we prove that <i>a network of simple MP neurons can compute any computable Boolean function</i>, including arithmetic logic units (ALUs), memory latches, and complex decision networks.
    """
    story.append(Paragraph(p_why1, body_style))

    story.append(Paragraph("2. Understanding Linear Separability in Deep Learning", h2_style))
    p_why2 = """
    Single-layer threshold neurons (like MP neurons and perceptrons) act as <b>linear classifiers</b>. In a 2D binary input space (x₁, x₂), the decision boundary separating y=1 outputs from y=0 outputs is a straight line defined by:
    """
    story.append(Paragraph(p_why2, body_style))

    line_eq = "<b>Decision Boundary Line Equation:</b> &nbsp;&nbsp; <i>w₁ x₁ + w₂ x₂ = θ</i>"
    story.append(Paragraph(line_eq, ParagraphStyle('LineEq', parent=body_style, textColor=ACCENT, leftIndent=20)))
    story.append(Spacer(1, 6))

    p_why2_cont = """
    For the NAND gate, the points (0,0), (0,1), and (1,0) lie on one side of the line (y=1), while the point (1,1) lies on the other side (y=0). Because these two groups can be split by a straight line, NAND is <b>linearly separable</b>. Studying NAND with MP neurons teaches students how early neural networks solved linearly separable problems, while illustrating why multi-layer networks (MLPs) are required for non-linearly separable functions like XOR.
    """
    story.append(Paragraph(p_why2_cont, body_style))

    story.append(Paragraph("3. Bridging Abstract Math with Industrial Safety Engineering", h2_style))
    p_why3 = """
    Rather than stopping at theoretical logic gates, this PBL project applies MP NAND neurons to a high-consequence real-world engineering challenge: an <b>Industrial Stamping Press Safety System</b>. This demonstrates how binary neural interlocks guarantee zero-defect safety clearance in automated factories.
    """
    story.append(Paragraph(p_why3, body_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 3: HOW IT IS IMPLEMENTED - MATHEMATICAL DERIVATION
    # =========================================================================
    story.append(Paragraph("3. Step-by-Step Mathematical Derivation: How NAND is Formulated", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=2, spaceAfter=10))

    p_math1 = """
    To construct a McCulloch-Pitts neuron for the NAND gate, we must determine specific numerical values for weights <b>w₁</b>, <b>w₂</b> and threshold <b>θ</b> such that the neuron satisfies all four rows of the NAND truth table simultaneously.
    """
    story.append(Paragraph(p_math1, body_style))

    # System of Inequalities Table
    sys_data = [
        [Paragraph("<b>Input Vector (x₁, x₂)</b>", ParagraphStyle('TH2', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY)),
         Paragraph("<b>Target Output (y)</b>", ParagraphStyle('TH2', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY)),
         Paragraph("<b>Mathematical Condition (z vs θ)</b>", ParagraphStyle('TH2', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY)),
         Paragraph("<b>Resulting Inequality Equation</b>", ParagraphStyle('TH2', parent=body_style, fontName='Helvetica-Bold', textColor=PRIMARY))]
    ]
    ineqs = [
        ["(0, 0)", "1", "z ≥ θ", "w₁(0) + w₂(0) ≥ θ  ⟹  <b>0 ≥ θ</b>"],
        ["(0, 1)", "1", "z ≥ θ", "w₁(0) + w₂(1) ≥ θ  ⟹  <b>w₂ ≥ θ</b>"],
        ["(1, 0)", "1", "z ≥ θ", "w₁(1) + w₂(0) ≥ θ  ⟹  <b>w₁ ≥ θ</b>"],
        ["(1, 1)", "0", "z < θ", "w₁(1) + w₂(1) < θ  ⟹  <b>w₁ + w₂ < θ</b>"]
    ]
    for row in ineqs:
        sys_data.append([
            Paragraph(row[0], body_style),
            Paragraph(row[1], body_style),
            Paragraph(row[2], body_style),
            Paragraph(row[3], body_style)
        ])

    sys_table = Table(sys_data, colWidths=[110, 85, 120, 189])
    sys_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(sys_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Derivation Solution", h2_style))
    p_math2 = """
    From Inequality (1), we learn that threshold θ must be non-positive (θ ≤ 0).<br/>
    If we select symmetric negative weights <b>w₁ = -1.0</b> and <b>w₂ = -1.0</b> with threshold <b>θ = -1.0</b>:
    """
    story.append(Paragraph(p_math2, body_style))

    proof_list = [
        "<b>For (0, 0):</b> z = (-1.0)(0) + (-1.0)(0) = 0.0 &nbsp;⟹&nbsp; 0.0 ≥ -1.0 (TRUE) ⟹ <b>Output y = 1</b>",
        "<b>For (0, 1):</b> z = (-1.0)(0) + (-1.0)(1) = -1.0 &nbsp;⟹&nbsp; -1.0 ≥ -1.0 (TRUE) ⟹ <b>Output y = 1</b>",
        "<b>For (1, 0):</b> z = (-1.0)(1) + (-1.0)(0) = -1.0 &nbsp;⟹&nbsp; -1.0 ≥ -1.0 (TRUE) ⟹ <b>Output y = 1</b>",
        "<b>For (1, 1):</b> z = (-1.0)(1) + (-1.0)(1) = -2.0 &nbsp;⟹&nbsp; -2.0 < -1.0 (FALSE) ⟹ <b>Output y = 0</b>"
    ]
    for item in proof_list:
        story.append(Paragraph(f"• {item}", bullet_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Proof of Universal Gate Synthesizing via NAND MP Neurons", h2_style))
    p_univ = """
    By interconnecting multiple McCulloch-Pitts NAND neurons (w₁=-1, w₂=-1, θ=-1), we synthesize all basic logic gates:
    """
    story.append(Paragraph(p_univ, body_style))

    univ_gates = [
        "<b>NOT Gate (1 NAND):</b> NOT(x) = NAND(x, x)",
        "<b>AND Gate (2 NANDs):</b> AND(x₁, x₂) = NOT(NAND(x₁, x₂)) = NAND(NAND(x₁, x₂), NAND(x₁, x₂))",
        "<b>OR Gate (3 NANDs):</b> OR(x₁, x₂) = NAND(NOT(x₁), NOT(x₂)) = NAND(NAND(x₁, x₁), NAND(x₂, x₂))",
        "<b>XOR Gate (4 NANDs):</b> Stage 1: N₁ = NAND(x₁, x₂); Stage 2: N₂ = NAND(x₁, N₁), N₃ = NAND(x₂, N₁); Stage 3: Out = NAND(N₂, N₃)",
        "<b>XNOR Gate (5 NANDs):</b> XNOR(x₁, x₂) = NOT(XOR(x₁, x₂)) = NAND(XOR(x₁, x₂), XOR(x₁, x₂))"
    ]
    for ug in univ_gates:
        story.append(Paragraph(f"• {ug}", bullet_style))
    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 4: HOW IT IS IMPLEMENTED - SOFTWARE ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("4. Software Architecture & Implementation Details", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("Python Implementation (`mcculloch_pitts_nand.py`)", h2_style))
    p_py = """
    The project codebase is built using clean, object-oriented Python. Key classes include:
    """
    story.append(Paragraph(p_py, body_style))

    py_classes = [
        "<b>McCullochPittsNeuron:</b> Core mathematical class encapsulating weight vectors, threshold evaluation, and optional inhibitory inputs.",
        "<b>NANDNeuron Factory:</b> Instantiates a pre-calibrated MP neuron with w=[-1,-1] and threshold=-1.",
        "<b>NANDUniversalSynthesizer:</b> Provides static methods synthesizing NOT, AND, OR, XOR, and XNOR logic strictly from NAND neurons.",
        "<b>IndustrialPressSafetySystem:</b> Implements the real-world safety interlock logic.",
        "<b>Automated Test Suite:</b> Programmatically asserts truth table states and prints diagnostic execution trace."
    ]
    for pyc in py_classes:
        story.append(Paragraph(f"• {pyc}", bullet_style))
    story.append(Spacer(1, 8))

    # Code Snippet Box
    code_text = """
class McCullochPittsNeuron:
    def __init__(self, weights: List[float], threshold: float, inhibitory_indices: List[int] = None):
        self.weights = list(weights)
        self.threshold = float(threshold)
        self.inhibitory_indices = set(inhibitory_indices) if inhibitory_indices else set()

    def activate(self, inputs: List[int]) -> int:
        # Check absolute inhibitory inputs
        for idx in self.inhibitory_indices:
            if inputs[idx] == 1:
                return 0
        # Compute weighted sum z = sum(w_i * x_i)
        weighted_sum = sum(w * x for w, x in zip(self.weights, inputs))
        return 1 if weighted_sum >= self.threshold else 0
    """
    code_table = Table([[Paragraph(code_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
    ]))
    story.append(code_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Interactive Web Visualizer Dashboard (`index.html`, `styles.css`, `app.js`)", h2_style))
    p_web = """
    To provide an intuitive visual interface, a modern web dashboard was constructed:
    """
    story.append(Paragraph(p_web, body_style))

    web_features = [
        "<b>Neuron Diagram Canvas:</b> SVG-rendered neural graph displaying active input pulses, weight badges, soma activation, and axon glow.",
        "<b>Real-Time Hyperparameter Sliders:</b> Dynamic sliders allowing users to adjust w₁, w₂, and threshold θ to see instantaneous decision boundary changes.",
        "<b>Interactive Truth Table:</b> Automatically highlights the active row corresponding to selected binary inputs (x₁, x₂).",
        "<b>Universal Synthesizer Playground:</b> Visualizes stage-by-stage evaluation of complex logic gates built out of NAND neurons.",
        "<b>Safety Interlock Simulator:</b> Animated power press machine reacting in real-time to guard sensors, dual buttons, and emergency stop."
    ]
    for wf in web_features:
        story.append(Paragraph(f"• {wf}", bullet_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Real-World Industrial Safety Case Study", h2_style))
    p_case = """
    In heavy manufacturing, power stamping presses exert thousands of tons of force. The press is permitted to cycle (Permission = 1) ONLY IF:
    <br/>1. <b>Safety Guard Enclosure</b> is closed (Sensor A = 1).
    <br/>2. <b>Two-Hand Palm Buttons</b> are pressed simultaneously (Sensor B = 1).
    <br/>3. <b>Emergency Stop (E-Stop)</b> is NOT pressed (E = 0).
    <br/><br/>
    This is realized using 2 NAND MP Neurons (forming an AND clearance gate) followed by an <b>Inhibitory MP Neuron</b> where the E-Stop acts as an absolute inhibitor.
    """
    story.append(Paragraph(p_case, body_style))
    story.append(Spacer(1, 15))

    # =========================================================================
    # SECTION 5: CONCLUSION & SUMMARY
    # =========================================================================
    story.append(Paragraph("5. Summary & Key Learning Outcomes", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=2, spaceAfter=10))

    p_conc = """
    Through this Project-Based Learning endeavor, we have demonstrated:
    <br/>1. The complete mathematical calibration of a <b>McCulloch-Pitts Neuron for the NAND Gate</b> (w₁=-1, w₂=-1, θ=-1).
    <br/>2. The theoretical and empirical validation of <b>functional universality</b>, showing how all computer logic stems from NAND MP neurons.
    <br/>3. A robust software architecture comprising pure Python algorithms and an interactive web visualizer.
    <br/>4. Practical deployment in an industrial press machine safety interlock controller.
    """
    story.append(Paragraph(p_conc, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF document successfully created at: {os.path.abspath(filename)}")

if __name__ == "__main__":
    create_pdf_report()
