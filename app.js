/**
 * McCulloch-Pitts Neuron Engine & Lab Controller
 * Vanilla JS Application for Neural Networks & Deep Learning
 */

document.addEventListener('DOMContentLoaded', () => {
    // State Management
    const state = {
        inputs: { x1: 0, x2: 0 },
        weights: { w1: -1.0, w2: -1.0 },
        theta: -1.0,
        currentPreset: 'nand',
        universal: {
            gate: 'NOT',
            inputs: { x1: 1, x2: 0 }
        },
        safety: {
            guard: true,
            buttons: true,
            estop: false
        }
    };

    // DOM Elements Cache
    const el = {
        tabs: document.querySelectorAll('.tab-btn'),
        panels: document.querySelectorAll('.tab-panel'),
        
        // Tab 1: Neuron Visualizer
        btnToggleX1: document.getElementById('btn-toggle-x1'),
        btnToggleX2: document.getElementById('btn-toggle-x2'),
        stateX1: document.getElementById('state-x1'),
        stateX2: document.getElementById('state-x2'),
        
        sliderW1: document.getElementById('slider-w1'),
        sliderW2: document.getElementById('slider-w2'),
        sliderTheta: document.getElementById('slider-theta'),
        
        valW1: document.getElementById('val-w1'),
        valW2: document.getElementById('val-w2'),
        valTheta: document.getElementById('val-theta'),
        
        presetBtns: document.querySelectorAll('.btn-preset'),
        btnResetParams: document.getElementById('btn-reset-params'),
        
        // SVG Elements
        nodeX1: document.getElementById('node-x1'),
        nodeX2: document.getElementById('node-x2'),
        svgValX1: document.getElementById('svg-val-x1'),
        svgValX2: document.getElementById('svg-val-x2'),
        svgW1Text: document.getElementById('svg-w1-text'),
        svgW2Text: document.getElementById('svg-w2-text'),
        synapse1: document.getElementById('synapse-1'),
        synapse2: document.getElementById('synapse-2'),
        axonLine: document.getElementById('axon-line'),
        somaGroup: document.getElementById('node-soma'),
        svgSumVal: document.getElementById('svg-sum-val'),
        svgThetaVal: document.getElementById('svg-theta-val'),
        nodeOutput: document.getElementById('node-output'),
        svgValOut: document.getElementById('svg-val-out'),
        
        // Calc Banner
        bannerZ: document.getElementById('banner-z'),
        bannerCond: document.getElementById('banner-cond'),
        bannerOut: document.getElementById('banner-out'),
        
        // Tab 2: Truth Table & Chart
        rows: {
            '00': document.getElementById('row-00'),
            '01': document.getElementById('row-01'),
            '10': document.getElementById('row-10'),
            '11': document.getElementById('row-11')
        },
        chartPoint: document.getElementById('chart-current-point'),
        chartThetaLabel: document.getElementById('chart-theta-label'),
        
        // Tab 3: Universal Synthesizer
        gateBtns: document.querySelectorAll('.btn-gate'),
        univTitle: document.getElementById('univ-title'),
        univToggleX1: document.getElementById('univ-toggle-x1'),
        univToggleX2: document.getElementById('univ-toggle-x2'),
        univX2Wrapper: document.getElementById('univ-x2-wrapper'),
        univSvg: document.getElementById('univ-svg'),
        univStagesBox: document.getElementById('univ-stages-box'),
        
        // Tab 4: Safety Project
        swGuard: document.getElementById('sw-guard'),
        swButtons: document.getElementById('sw-buttons'),
        swEstop: document.getElementById('sw-estop'),
        beaconLight: document.getElementById('beacon-light'),
        machineStatusTitle: document.getElementById('machine-status-title'),
        machineStatusSub: document.getElementById('machine-status-sub'),
        pressRam: document.getElementById('press-ram'),
        traceN1: document.getElementById('trace-n1'),
        traceClearance: document.getElementById('trace-clearance'),
        tracePermission: document.getElementById('trace-permission')
    };

    // Initialize Event Listeners
    initTabs();
    initNeuronControls();
    initUniversalSynthesizer();
    initSafetyProject();

    // Initial render
    updateNeuronLab();

    // =================================================================
    // Tab Navigation Logic
    // =================================================================
    function initTabs() {
        el.tabs.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetTab = btn.getAttribute('data-tab');

                el.tabs.forEach(t => t.classList.remove('active'));
                el.panels.forEach(p => p.classList.remove('active'));

                btn.classList.add('active');
                document.getElementById(targetTab).classList.add('active');

                // Trigger MathJax re-render if available
                if (window.MathJax && window.MathJax.typesetPromise) {
                    window.MathJax.typesetPromise();
                }
            });
        });
    }

    // =================================================================
    // Tab 1: McCulloch-Pitts Neuron Engine & Controls
    // =================================================================
    function initNeuronControls() {
        // Input Toggles
        el.btnToggleX1.addEventListener('click', () => {
            state.inputs.x1 = state.inputs.x1 === 0 ? 1 : 0;
            updateNeuronLab();
        });

        el.btnToggleX2.addEventListener('click', () => {
            state.inputs.x2 = state.inputs.x2 === 0 ? 1 : 0;
            updateNeuronLab();
        });

        // Hyperparameter Sliders
        el.sliderW1.addEventListener('input', (e) => {
            state.weights.w1 = parseFloat(e.target.value);
            state.currentPreset = 'custom';
            updateNeuronLab();
        });

        el.sliderW2.addEventListener('input', (e) => {
            state.weights.w2 = parseFloat(e.target.value);
            state.currentPreset = 'custom';
            updateNeuronLab();
        });

        el.sliderTheta.addEventListener('input', (e) => {
            state.theta = parseFloat(e.target.value);
            state.currentPreset = 'custom';
            updateNeuronLab();
        });

        // Presets
        el.presetBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const preset = btn.getAttribute('data-preset');
                applyPreset(preset);
            });
        });

        el.btnResetParams.addEventListener('click', () => {
            applyPreset('nand');
        });
    }

    function applyPreset(preset) {
        state.currentPreset = preset;
        if (preset === 'nand') {
            state.weights.w1 = -1.0;
            state.weights.w2 = -1.0;
            state.theta = -1.0;
        } else if (preset === 'and') {
            state.weights.w1 = 1.0;
            state.weights.w2 = 1.0;
            state.theta = 2.0;
        } else if (preset === 'or') {
            state.weights.w1 = 1.0;
            state.weights.w2 = 1.0;
            state.theta = 1.0;
        } else if (preset === 'nor') {
            state.weights.w1 = -1.0;
            state.weights.w2 = -1.0;
            state.theta = 0.0;
        }

        // Update Slider UI
        el.sliderW1.value = state.weights.w1;
        el.sliderW2.value = state.weights.w2;
        el.sliderTheta.value = state.theta;

        updateNeuronLab();
    }

    // =================================================================
    // McCulloch-Pitts Computational Evaluator
    // =================================================================
    function evaluateMPNeuron(x1, x2, w1, w2, theta) {
        const z = (w1 * x1) + (w2 * x2);
        const fired = z >= theta;
        return {
            z,
            theta,
            fired,
            y: fired ? 1 : 0
        };
    }

    function updateNeuronLab() {
        const { x1, x2 } = state.inputs;
        const { w1, w2 } = state.weights;
        const theta = state.theta;

        const res = evaluateMPNeuron(x1, x2, w1, w2, theta);

        // 1. Update Input Toggle UI
        el.stateX1.textContent = `${x1} (${x1 ? 'ON' : 'OFF'})`;
        el.stateX2.textContent = `${x2} (${x2 ? 'ON' : 'OFF'})`;
        el.btnToggleX1.classList.toggle('active', x1 === 1);
        el.btnToggleX2.classList.toggle('active', x2 === 1);

        // 2. Update Slider Text Labels
        el.valW1.textContent = w1.toFixed(1);
        el.valW2.textContent = w2.toFixed(1);
        el.valTheta.textContent = theta.toFixed(1);

        // Update Preset Buttons Active State
        el.presetBtns.forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-preset') === state.currentPreset);
        });

        // 3. Update SVG Canvas Elements
        el.svgValX1.textContent = x1;
        el.svgValX2.textContent = x2;
        el.svgW1Text.textContent = `w₁ = ${w1.toFixed(1)}`;
        el.svgW2Text.textContent = `w₂ = ${w2.toFixed(1)}`;
        el.svgSumVal.textContent = `z = ${res.z.toFixed(1)}`;
        el.svgThetaVal.textContent = `θ = ${theta.toFixed(1)}`;
        el.svgValOut.textContent = res.y;

        // Node Glow Classes
        el.nodeX1.classList.toggle('active', x1 === 1);
        el.nodeX2.classList.toggle('active', x2 === 1);

        el.synapse1.className.baseVal = `synapse-line ${x1 ? 'active' : 'inactive'}`;
        el.synapse2.className.baseVal = `synapse-line ${x2 ? 'active' : 'inactive'}`;

        el.somaGroup.className.baseVal = `soma-group ${res.fired ? 'firing' : 'quiescent'}`;
        el.axonLine.className.baseVal = `synapse-line ${res.fired ? 'axon-active' : 'axon-inactive'}`;
        el.nodeOutput.className.baseVal = `output-node-group ${res.fired ? 'active' : 'inactive'}`;

        // 4. Update Calculation Inspector Banner
        const w1Term = `(${w1.toFixed(1)} × ${x1})`;
        const w2Term = `(${w2.toFixed(1)} × ${x2})`;
        el.bannerZ.textContent = `z = ${w1Term} + ${w2Term} = ${res.z.toFixed(1)}`;

        const condStr = res.fired ? `${res.z.toFixed(1)} ≥ ${theta.toFixed(1)} (TRUE)` : `${res.z.toFixed(1)} < ${theta.toFixed(1)} (FALSE)`;
        el.bannerCond.textContent = condStr;
        el.bannerCond.style.color = res.fired ? 'var(--accent-emerald)' : 'var(--accent-pink)';

        el.bannerOut.textContent = `y = ${res.y}`;
        el.bannerOut.className = `calc-result ${res.fired ? 'active-1' : 'active-0'}`;

        // 5. Update Truth Table Active Row Highlighting
        const activeKey = `${x1}${x2}`;
        Object.keys(el.rows).forEach(key => {
            if (el.rows[key]) {
                el.rows[key].classList.toggle('active-row', key === activeKey);
            }
        });

        // 6. Update Step Chart Operating Point
        // Chart coordinates mapping: x-range [40, 360], z range [-3, 3] -> center z=0 is at x=200
        // threshold theta is mapped to x_theta.
        const thetaX = 200 + (theta / 3.0) * 160;
        const currentZ = res.z;
        const pointX = Math.max(40, Math.min(360, 200 + (currentZ / 3.0) * 160));
        const pointY = res.fired ? 40 : 160;

        el.chartPoint.setAttribute('cx', pointX);
        el.chartPoint.setAttribute('cy', pointY);
        el.chartThetaLabel.textContent = `θ = ${theta.toFixed(1)}`;
        el.chartThetaLabel.setAttribute('x', Math.max(50, Math.min(340, thetaX - 10)));
    }

    // =================================================================
    // Tab 3: Universal Logic Synthesizer
    // =================================================================
    function initUniversalSynthesizer() {
        el.gateBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                state.universal.gate = btn.getAttribute('data-gate');
                el.gateBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderUniversalCircuit();
            });
        });

        el.univToggleX1.addEventListener('click', () => {
            state.universal.inputs.x1 = state.universal.inputs.x1 === 0 ? 1 : 0;
            el.univToggleX1.textContent = state.universal.inputs.x1;
            el.univToggleX1.classList.toggle('active', state.universal.inputs.x1 === 1);
            renderUniversalCircuit();
        });

        el.univToggleX2.addEventListener('click', () => {
            state.universal.inputs.x2 = state.universal.inputs.x2 === 0 ? 1 : 0;
            el.univToggleX2.textContent = state.universal.inputs.x2;
            el.univToggleX2.classList.toggle('active', state.universal.inputs.x2 === 1);
            renderUniversalCircuit();
        });

        renderUniversalCircuit();
    }

    function nand(a, b) {
        return (a === 1 && b === 1) ? 0 : 1;
    }

    function renderUniversalCircuit() {
        const { gate, inputs } = state.universal;
        const { x1, x2 } = inputs;

        // Show/hide x2 toggle based on single or dual input gate
        el.univX2Wrapper.style.display = (gate === 'NOT') ? 'none' : 'flex';

        let stagesHtml = '';
        let svgContent = '';
        let titleText = '';

        if (gate === 'NOT') {
            const out = nand(x1, x1);
            titleText = `Synthesizing NOT(${x1}) = NAND(${x1}, ${x1}) = ${out}`;

            stagesHtml = `
                <div class="stage-card">
                    <div class="stage-title">Single NAND Stage</div>
                    <div class="stage-calc">N1 = NAND(${x1}, ${x1}) = <strong>${out}</strong></div>
                </div>
            `;

            svgContent = `
                <g transform="translate(100, 150)">
                    <circle r="24" fill="${x1 ? 'rgba(0,242,254,0.3)' : '#121824'}" stroke="${x1 ? '#00f2fe' : '#64748b'}" stroke-width="2"/>
                    <text y="5" text-anchor="middle" fill="#fff" font-family="monospace">x₁ = ${x1}</text>
                </g>
                <path d="M 124 150 L 350 150" stroke="${x1 ? '#00f2fe' : '#64748b'}" stroke-width="3" fill="none"/>
                
                <!-- NAND Gate Node -->
                <g transform="translate(400, 150)">
                    <circle r="40" fill="${out ? 'rgba(16,185,129,0.2)' : 'rgba(255,0,127,0.2)'}" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="3"/>
                    <text y="-8" text-anchor="middle" fill="#fff" font-weight="bold">MP NAND</text>
                    <text y="14" text-anchor="middle" fill="${out ? '#10b981' : '#ff007f'}" font-family="monospace">Output = ${out}</text>
                </g>
                <path d="M 440 150 L 650 150" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="4" fill="none"/>
                
                <g transform="translate(680, 150)">
                    <circle r="28" fill="${out ? 'rgba(16,185,129,0.3)' : '#121824'}" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="3"/>
                    <text y="6" text-anchor="middle" fill="#fff" font-family="monospace" font-size="20">${out}</text>
                </g>
            `;
        } else if (gate === 'AND') {
            const n1 = nand(x1, x2);
            const out = nand(n1, n1);
            titleText = `Synthesizing AND(${x1}, ${x2}) = NOT(NAND(${x1}, ${x2})) = ${out}`;

            stagesHtml = `
                <div class="stage-card">
                    <div class="stage-title">Stage 1: Primary NAND</div>
                    <div class="stage-calc">N1 = NAND(${x1}, ${x2}) = <strong>${n1}</strong></div>
                </div>
                <div class="stage-card">
                    <div class="stage-title">Stage 2: Inverter NAND</div>
                    <div class="stage-calc">Out = NAND(${n1}, ${n1}) = <strong>${out}</strong></div>
                </div>
            `;

            svgContent = `
                <g transform="translate(80, 90)">
                    <circle r="20" fill="${x1 ? 'rgba(0,242,254,0.3)' : '#121824'}" stroke="${x1 ? '#00f2fe' : '#64748b'}" stroke-width="2"/>
                    <text y="4" text-anchor="middle" fill="#fff" font-family="monospace">x₁=${x1}</text>
                </g>
                <g transform="translate(80, 210)">
                    <circle r="20" fill="${x2 ? 'rgba(0,242,254,0.3)' : '#121824'}" stroke="${x2 ? '#00f2fe' : '#64748b'}" stroke-width="2"/>
                    <text y="4" text-anchor="middle" fill="#fff" font-family="monospace">x₂=${x2}</text>
                </g>

                <path d="M 100 90 Q 200 90 260 135" stroke="${x1 ? '#00f2fe' : '#64748b'}" stroke-width="3" fill="none"/>
                <path d="M 100 210 Q 200 210 260 165" stroke="${x2 ? '#00f2fe' : '#64748b'}" stroke-width="3" fill="none"/>

                <!-- NAND 1 -->
                <g transform="translate(300, 150)">
                    <circle r="35" fill="rgba(157, 78, 221, 0.2)" stroke="#9d4edd" stroke-width="3"/>
                    <text y="-5" text-anchor="middle" fill="#fff" font-size="12">NAND 1</text>
                    <text y="14" text-anchor="middle" fill="#9d4edd" font-family="monospace">N1 = ${n1}</text>
                </g>

                <path d="M 335 150 L 515 150" stroke="${n1 ? '#00f2fe' : '#64748b'}" stroke-width="3" fill="none"/>

                <!-- NAND 2 -->
                <g transform="translate(550, 150)">
                    <circle r="35" fill="${out ? 'rgba(16,185,129,0.2)' : 'rgba(255,0,127,0.2)'}" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="3"/>
                    <text y="-5" text-anchor="middle" fill="#fff" font-size="12">NAND 2</text>
                    <text y="14" text-anchor="middle" fill="${out ? '#10b981' : '#ff007f'}" font-family="monospace">Out = ${out}</text>
                </g>

                <path d="M 585 150 L 710 150" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="4" fill="none"/>
                <g transform="translate(740, 150)">
                    <circle r="26" fill="${out ? 'rgba(16,185,129,0.3)' : '#121824'}" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="3"/>
                    <text y="6" text-anchor="middle" fill="#fff" font-family="monospace" font-size="18">${out}</text>
                </g>
            `;
        } else if (gate === 'OR') {
            const notX1 = nand(x1, x1);
            const notX2 = nand(x2, x2);
            const out = nand(notX1, notX2);

            titleText = `Synthesizing OR(${x1}, ${x2}) = NAND(NOT(${x1}), NOT(${x2})) = ${out}`;

            stagesHtml = `
                <div class="stage-card">
                    <div class="stage-title">Stage 1: NOT(x₁)</div>
                    <div class="stage-calc">N1 = NAND(${x1}, ${x1}) = <strong>${notX1}</strong></div>
                </div>
                <div class="stage-card">
                    <div class="stage-title">Stage 1: NOT(x₂)</div>
                    <div class="stage-calc">N2 = NAND(${x2}, ${x2}) = <strong>${notX2}</strong></div>
                </div>
                <div class="stage-card">
                    <div class="stage-title">Stage 2: Output NAND</div>
                    <div class="stage-calc">Out = NAND(${notX1}, ${notX2}) = <strong>${out}</strong></div>
                </div>
            `;

            svgContent = `
                <g transform="translate(60, 80)"><circle r="18" fill="${x1 ? '#00f2fe' : '#121824'}" stroke="#00f2fe" stroke-width="2"/><text y="4" text-anchor="middle" fill="#fff">x₁=${x1}</text></g>
                <g transform="translate(60, 220)"><circle r="18" fill="${x2 ? '#00f2fe' : '#121824'}" stroke="#00f2fe" stroke-width="2"/><text y="4" text-anchor="middle" fill="#fff">x₂=${x2}</text></g>

                <path d="M 78 80 L 210 80" stroke="#00f2fe" stroke-width="2"/>
                <path d="M 78 220 L 210 220" stroke="#00f2fe" stroke-width="2"/>

                <g transform="translate(240, 80)"><circle r="30" fill="rgba(157,78,221,0.2)" stroke="#9d4edd" stroke-width="2"/><text y="4" text-anchor="middle" fill="#fff" font-size="11">NOT x₁ (${notX1})</text></g>
                <g transform="translate(240, 220)"><circle r="30" fill="rgba(157,78,221,0.2)" stroke="#9d4edd" stroke-width="2"/><text y="4" text-anchor="middle" fill="#fff" font-size="11">NOT x₂ (${notX2})</text></g>

                <path d="M 270 80 Q 400 80 470 135" stroke="#9d4edd" stroke-width="2"/>
                <path d="M 270 220 Q 400 220 470 165" stroke="#9d4edd" stroke-width="2"/>

                <g transform="translate(510, 150)"><circle r="38" fill="${out ? 'rgba(16,185,129,0.2)' : 'rgba(255,0,127,0.2)'}" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="3"/><text y="-4" text-anchor="middle" fill="#fff" font-size="12">NAND Out</text><text y="14" text-anchor="middle" fill="${out ? '#10b981' : '#ff007f'}">${out}</text></g>

                <path d="M 548 150 L 680 150" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="4"/>
                <g transform="translate(710, 150)"><circle r="24" fill="${out ? 'rgba(16,185,129,0.3)' : '#121824'}" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="3"/><text y="5" text-anchor="middle" fill="#fff" font-family="monospace" font-size="16">${out}</text></g>
            `;
        } else if (gate === 'XOR') {
            const n1 = nand(x1, x2);
            const n2 = nand(x1, n1);
            const n3 = nand(x2, n1);
            const out = nand(n2, n3);

            titleText = `Synthesizing XOR(${x1}, ${x2}) using 4 Interconnected NAND MP Neurons = ${out}`;

            stagesHtml = `
                <div class="stage-card"><div class="stage-title">NAND 1 (Cross)</div><div class="stage-calc">N1 = NAND(${x1}, ${x2}) = <strong>${n1}</strong></div></div>
                <div class="stage-card"><div class="stage-title">NAND 2 (Upper)</div><div class="stage-calc">N2 = NAND(${x1}, ${n1}) = <strong>${n2}</strong></div></div>
                <div class="stage-card"><div class="stage-title">NAND 3 (Lower)</div><div class="stage-calc">N3 = NAND(${x2}, ${n1}) = <strong>${n3}</strong></div></div>
                <div class="stage-card"><div class="stage-title">NAND 4 (Final)</div><div class="stage-calc">Out = NAND(${n2}, ${n3}) = <strong>${out}</strong></div></div>
            `;

            svgContent = `
                <g transform="translate(60, 70)"><circle r="18" fill="${x1 ? '#00f2fe' : '#121824'}" stroke="#00f2fe"/><text y="4" text-anchor="middle" fill="#fff">x₁=${x1}</text></g>
                <g transform="translate(60, 230)"><circle r="18" fill="${x2 ? '#00f2fe' : '#121824'}" stroke="#00f2fe"/><text y="4" text-anchor="middle" fill="#fff">x₂=${x2}</text></g>

                <g transform="translate(240, 150)"><circle r="28" fill="rgba(157,78,221,0.2)" stroke="#9d4edd" stroke-width="2"/><text y="4" text-anchor="middle" fill="#fff" font-size="11">N1=${n1}</text></g>
                <g transform="translate(420, 70)"><circle r="28" fill="rgba(157,78,221,0.2)" stroke="#9d4edd" stroke-width="2"/><text y="4" text-anchor="middle" fill="#fff" font-size="11">N2=${n2}</text></g>
                <g transform="translate(420, 230)"><circle r="28" fill="rgba(157,78,221,0.2)" stroke="#9d4edd" stroke-width="2"/><text y="4" text-anchor="middle" fill="#fff" font-size="11">N3=${n3}</text></g>
                <g transform="translate(600, 150)"><circle r="34" fill="${out ? 'rgba(16,185,129,0.2)' : 'rgba(255,0,127,0.2)'}" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="3"/><text y="4" text-anchor="middle" fill="#fff" font-size="13">Out=${out}</text></g>

                <path d="M 78 70 Q 150 70 215 135" stroke="#00f2fe" stroke-width="2"/>
                <path d="M 78 230 Q 150 230 215 165" stroke="#00f2fe" stroke-width="2"/>
                <path d="M 78 70 L 392 70" stroke="#00f2fe" stroke-width="2"/>
                <path d="M 78 230 L 392 230" stroke="#00f2fe" stroke-width="2"/>

                <path d="M 268 150 L 392 85" stroke="#9d4edd" stroke-width="2"/>
                <path d="M 268 150 L 392 215" stroke="#9d4edd" stroke-width="2"/>

                <path d="M 448 70 Q 520 70 570 135" stroke="#9d4edd" stroke-width="2"/>
                <path d="M 448 230 Q 520 230 570 165" stroke="#9d4edd" stroke-width="2"/>
            `;
        } else if (gate === 'XNOR') {
            const xorOut = nand(nand(x1, nand(x1, nand(x1, x2))), nand(x2, nand(x1, x2)));
            const out = nand(xorOut, xorOut);

            titleText = `Synthesizing XNOR(${x1}, ${x2}) = NOT(XOR(${x1}, ${x2})) = ${out}`;

            stagesHtml = `
                <div class="stage-card"><div class="stage-title">XOR Stage (4 NANDs)</div><div class="stage-calc">XOR = <strong>${xorOut}</strong></div></div>
                <div class="stage-card"><div class="stage-title">Inverter Stage (5th NAND)</div><div class="stage-calc">XNOR = NAND(${xorOut}, ${xorOut}) = <strong>${out}</strong></div></div>
            `;

            svgContent = `
                <g transform="translate(100, 150)"><rect x="-40" y="-30" width="180" height="60" rx="10" fill="rgba(157,78,221,0.2)" stroke="#9d4edd" stroke-width="2"/><text y="5" text-anchor="middle" fill="#fff">4-NAND XOR Block (${xorOut})</text></g>
                <path d="M 240 150 L 450 150" stroke="#9d4edd" stroke-width="3"/>
                <g transform="translate(490, 150)"><circle r="36" fill="${out ? 'rgba(16,185,129,0.2)' : 'rgba(255,0,127,0.2)'}" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="3"/><text y="5" text-anchor="middle" fill="#fff">NAND 5 (${out})</text></g>
                <path d="M 526 150 L 680 150" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="4"/>
                <g transform="translate(710, 150)"><circle r="26" fill="${out ? 'rgba(16,185,129,0.3)' : '#121824'}" stroke="${out ? '#10b981' : '#ff007f'}" stroke-width="3"/><text y="6" text-anchor="middle" fill="#fff" font-family="monospace" font-size="18">${out}</text></g>
            `;
        }

        el.univTitle.textContent = titleText;
        el.univStagesBox.innerHTML = stagesHtml;
        el.univSvg.innerHTML = svgContent;
    }

    // =================================================================
    // Tab 4: Real-World Industrial Safety Interlock Simulation
    // =================================================================
    function initSafetyProject() {
        el.swGuard.addEventListener('change', updateSafetySystem);
        el.swButtons.addEventListener('change', updateSafetySystem);
        el.swEstop.addEventListener('change', updateSafetySystem);

        updateSafetySystem();
    }

    function updateSafetySystem() {
        const guard = el.swGuard.checked ? 1 : 0;
        const buttons = el.swButtons.checked ? 1 : 0;
        const estop = el.swEstop.checked ? 1 : 0;

        // MP NAND Neuron Stage 1: NAND(Guard, Buttons)
        const n1 = (guard === 1 && buttons === 1) ? 0 : 1;

        // MP NAND Neuron Stage 2 (Inverter to form AND): NAND(N1, N1)
        const clearance = (n1 === 0) ? 1 : 0;

        // Final MP Inhibitory Neuron: Clearance is input, E-stop is inhibitory input
        const permission = (estop === 1) ? 0 : clearance;

        // Update Neural Trace UI
        el.traceN1.textContent = `N1 = ${n1}`;
        el.traceClearance.textContent = `Clearance = ${clearance}`;
        el.tracePermission.textContent = `Permission = ${permission}`;

        // Machine Status UI
        if (permission === 1) {
            el.beaconLight.className = 'status-beacon beacon-green';
            el.machineStatusTitle.textContent = 'PRESS AUTHORIZED & OPERATING SAFELY';
            el.machineStatusSub.textContent = 'Guard closed, dual palm controls pressed. Zero safety hazards detected.';
            el.pressRam.classList.add('operating');
        } else {
            el.beaconLight.className = 'status-beacon beacon-red';
            el.pressRam.classList.remove('operating');

            if (estop === 1) {
                el.machineStatusTitle.textContent = 'EMERGENCY STOP (E-STOP) ENGAGED!';
                el.machineStatusSub.textContent = 'Hardware interlock tripped by emergency palm button. Motor power cut.';
            } else if (guard === 0) {
                el.machineStatusTitle.textContent = 'SAFETY HAZARD: Guard Enclosure Open!';
                el.machineStatusSub.textContent = 'Acrylic safety guard opened. Press operation prohibited.';
            } else {
                el.machineStatusTitle.textContent = 'SAFETY HAZARD: Two-Hand Buttons Released!';
                el.machineStatusSub.textContent = 'Dual palm buttons not pressed. Requires two-hand operation clearance.';
            }
        }
    }
});
