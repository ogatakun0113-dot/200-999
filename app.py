<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>伝送値換算 (200-999)</title>
    <style>
        :root { --royalblue: #4169E1; --red: #FF4B4B; --bg: #f0f2f6; --text: #31333F; }
        body { font-family: sans-serif; color: var(--text); background: #fff; margin: 0; padding: 15px; }
        .credit { text-align: right; font-size: 14px; color: #666; margin-bottom: 5px; }
        h1 { font-size: 18px; margin: 10px 0; color: var(--text); border-bottom: 2px solid var(--royalblue); padding-bottom: 5px; }
        
        /* 設定エリア */
        details { background: #f9f9f9; border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-bottom: 15px; }
        summary { font-weight: bold; cursor: pointer; color: #444; }
        .config-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
        .config-item label { font-size: 12px; font-weight: bold; color: var(--royalblue); }
        .config-item input, .config-item select { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 5px; font-size: 14px; box-sizing: border-box; }

        /* 入力モード切替 */
        .mode-selector { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 15px; background: #eee; padding: 5px; border-radius: 8px; }
        .mode-btn { flex: 1; min-width: 70px; text-align: center; padding: 8px 2px; font-size: 11px; cursor: pointer; background: #fff; border-radius: 5px; border: 1px solid #ccc; }
        .mode-btn.active { background: var(--royalblue); color: #fff; border-color: var(--royalblue); font-weight: bold; }

        .input-main label { display: block; font-size: 18px; font-weight: 800; color: var(--royalblue); margin-bottom: 10px; }
        .input-main input { width: 100%; height: 55px; padding: 10px; border: 3px solid var(--royalblue); border-radius: 10px; box-sizing: border-box; font-size: 24px; font-weight: bold; outline: none; }
        .calc-note { color: #d63384; font-weight: bold; font-size: 14px; margin-top: 5px; display: none; }

        /* 結果ボックス */
        .result-box { background: var(--bg); padding: 15px; border-radius: 10px; border-left: 5px solid var(--royalblue); margin-top: 20px; }
        .res-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 15px; }
        .metric { text-align: center; }
        .metric-label { font-size: 11px; color: #666; }
        .metric-value { font-size: 16px; font-weight: bold; display: block; color: #000; }
        .bit-display { text-align: center; border-top: 1px solid #ccc; padding-top: 10px; }
        .bit-value { font-size: 32px; font-weight: bold; color: var(--royalblue); }

        .footer-note { font-size: 11px; color: #888; margin-top: 15px; }
    </style>
</head>
<body>

<div class="credit">開発/制作：緒方</div>
<h1>📱 伝送値換算 (200-999)(DEC)</h1>

<details open>
    <summary>⚙️ 基本情報設定 (200-999基準)</summary>
    <div class="config-grid">
        <div class="config-item"><label>指示 0%</label><input type="number" id="s_min" value="0.00" oninput="calc()"></div>
        <div class="config-item"><label>指示 100%</label><input type="number" id="s_max" value="100.00" oninput="calc()"></div>
        <div class="config-item"><label>電流 4mA</label><input type="number" id="a_min" value="4.00" step="0.01" oninput="updateVoltage()"></div>
        <div class="config-item"><label>電流 20mA</label><input type="number" id="a_max" value="20.00" step="0.01" oninput="updateVoltage()"></div>
        <div class="config-item">
            <label>入力抵抗を選択 (Ω)</label>
            <select id="resistance" onchange="updateVoltage()">
                <option value="250">250 Ω</option>
                <option value="500">500 Ω</option>
                <option value="50">50 Ω</option>
            </select>
        </div>
        <div class="config-item">
            <label>電圧表示 (V)</label>
            <input type="text" id="v_display" value="1.000 V" readonly style="background:#eee;">
        </div>
    </div>
</details>

<div class="mode-selector">
    <div class="mode-btn active" onclick="setMode('bit')">伝送値</div>
    <div class="mode-btn" onclick="setMode('val')">指示値</div>
    <div class="mode-btn" onclick="setMode('per')">割合(%)</div>
    <div class="mode-btn" onclick="setMode('ma')">電流(mA)</div>
    <div class="mode-btn" onclick="setMode('v')">電圧(V)</div>
</div>

<div class="input-main">
    <label id="input_label">現在の伝送値 (200-999)</label>
    <input type="number" id="main_input" value="999" oninput="calc()">
    <div id="calc_note" class="calc-note">※999bitを1000bitとして計算中</div>
</div>

<div class="result-box">
    <div class="res-grid">
        <div class="metric">
            <span class="metric-label">指示値</span>
            <span id="res_scale" class="metric-value">0.00</span>
        </div>
        <div class="metric">
            <span class="metric-label">電流(mA)</span>
            <span id="res_ma" class="metric-value">4.00</span>
        </div>
        <div class="metric">
            <span class="metric-label">電圧(V)</span>
            <span id="res_v" class="metric-value">1.000</span>
        </div>
    </div>
    <div class="bit-display">
        <span class="metric-label">伝送値 (bit)</span><br>
        <span id="res_t" class="bit-value">999</span>
    </div>
</div>

<div class="footer-note">
    ※分母を800bitとして計算し、999bit入力時は100%（1000bit相当）として読み替えています。
</div>

<script>
    let currentMode = 'bit';
    const T_OFFSET = 200;
    const T_DIV = 800;

    function setMode(mode) {
        currentMode = mode;
        const btns = document.querySelectorAll('.mode-btn');
        btns.forEach(b => b.classList.remove('active'));
        event.target.classList.add('active');

        const labels = {
            'bit': '現在の伝送値 (200-999)',
            'val': '指示値を入力',
            'per': '割合(%)を入力',
            'ma': '電流(mA)を入力',
            'v': '電圧(V)を入力'
        };
        document.getElementById('input_label').innerText = labels[mode];
        calc();
    }

    function updateVoltage() {
        const aMin = parseFloat(document.getElementById('a_min').value) || 0;
        const aMax = parseFloat(document.getElementById('a_max').value) || 0;
        const res = parseFloat(document.getElementById('resistance').value);
        const vMin = (aMin / 1000) * res;
        const vMax = (aMax / 1000) * res;
        
        // 小数点以下3桁で表示
        document.getElementById('v_display').value = vMin.toFixed(3) + "V / " + vMax.toFixed(3) + "V";
        calc();
    }

    function calc() {
        const inputVal = parseFloat(document.getElementById('main_input').value) || 0;
        const sMin = parseFloat(document.getElementById('s_min').value) || 0;
        const sMax = parseFloat(document.getElementById('s_max').value) || 0;
        const aMin = parseFloat(document.getElementById('a_min').value) || 0;
        const aMax = parseFloat(document.getElementById('a_max').value) || 0;
        const res = parseFloat(document.getElementById('resistance').value);
        const vMin = (aMin / 1000) * res;
        const vMax = (aMax / 1000) * res;
        const note = document.getElementById('calc_note');

        let percent = 0;
        note.style.display = 'none';

        if (currentMode === 'bit') {
            let calcBit = inputVal;
            if (inputVal === 999) {
                calcBit = 1000;
                note.style.display = 'block';
            }
            percent = (calcBit - T_OFFSET) / T_DIV;
        } else if (currentMode === 'val') {
            percent = (inputVal - sMin) / (s_max - s_min);
        } else if (currentMode === 'per') {
            percent = inputVal / 100;
        } else if (currentMode === 'ma') {
            percent = (inputVal - aMin) / (a_max - a_min);
        } else if (currentMode === 'v') {
            percent = (inputVal - vMin) / (vMax - vMin);
        }

        if (isNaN(percent) || !isFinite(percent)) percent = 0;

        const resScale = sMin + (s_max - s_min) * percent;
        const resMa = aMin + (a_max - a_min) * percent;
        const resV = vMin + (vMax - vMin) * percent;
        
        let resT = Math.round(T_OFFSET + (T_DIV * percent));
        if (resT >= 1000) resT = 999;

        document.getElementById('res_scale').innerText = resScale.toFixed(2);
        document.getElementById('res_ma').innerText = resMa.toFixed(2);
        document.getElementById('res_v').innerText = resV.toFixed(3); // 電圧を3桁表示
        document.getElementById('res_t').innerText = resT;
    }

    window.onload = updateVoltage;
</script>

</body>
</html>
