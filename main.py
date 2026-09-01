import streamlit as st

st.set_page_config(
    page_title="3D City Highway Racing",
    page_icon="🏁",
    layout="wide",
)

def run_game():
    game_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>3D City Highway Racing</title>
        <style>
            body { margin: 0; overflow: hidden; background-color: #111; color: white; font-family: sans-serif; }
            #ui-layer {
                position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                pointer-events: none; display: flex; flex-direction: column; align-items: center;
            }
            .header {
                background: rgba(0,0,0,0.7); padding: 10px 20px; border-radius: 0 0 15px 15px;
                border: 1px solid #00ffcc; pointer-events: auto; display: flex; gap: 15px; align-items: center;
            }
            select { background: #333; color: #fff; padding: 5px; border: 1px solid #777; border-radius: 5px; }
            .hud {
                position: absolute; bottom: 80px; left: 20px;
                background: rgba(0,0,0,0.6); padding: 15px; border-radius: 10px; border-left: 4px solid #ff3300;
                font-size: 20px; font-weight: bold;
            }
            #restartBtn {
                position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
                padding: 12px 30px; font-size: 18px; font-weight: bold; background: #00ffcc;
                color: #000; border: none; border-radius: 8px; cursor: pointer; pointer-events: auto;
                box-shadow: 0 0 15px rgba(0,255,204,0.5); display: none;
            }
            #restartBtn:hover { background: #00cca3; }
            #message {
                position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);
                font-size: 50px; font-weight: 900; text-shadow: 2px 2px 10px #000; display: none;
                text-align: center; color: #ffcc00;
            }
            .controls-info {
                position: absolute; bottom: 20px; right: 20px; background: rgba(0,0,0,0.5);
                padding: 10px; border-radius: 8px; font-size: 14px; text-align: right; pointer-events: auto;
            }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="ui-layer">
            <div class="header">
                <h2>🏙️ 3D Highway Racer</h2>
                <label>차량 선택:</label>
                <select id="carSelect" onchange="changeCar()">
                    <option value="gtr">Nissan GT-R (Acceleration)</option>
                    <option value="svj">Lambo Aventador SVJ (Top Speed)</option>
                    <option value="porsche">Porsche 911 GT3 (Handling)</option>
                    <option value="ferrari">Ferrari 488 Pista (Balanced)</option>
                    <option value="mclaren">McLaren 720S (Boost Power)</option>
                    <option value="bugatti">Bugatti Chiron (Heavy & Fast)</option>
                    <option value="aston">Aston Martin Vantage (Drift)</option>
                </select>
            </div>
            
            <div class="hud">
                <div>속도: <span id="speedUi">0</span> km/h</div>
                <div>부스터: <span id="nitroUi">100</span>%</div>
                <div>남은 거리: <span id="distUi">10000</span> m</div>
            </div>

            <div id="message">FINISH!</div>
            <button id="restartBtn" onclick="resetGame()">🔄 다시 하기</button>

            <div class="controls-info">
                <b>[W]</b> 가속 &nbsp; <b>[S]</b> 브레이크<br>
                <b>[A][D]</b> 좌우 조향<br>
                <b>[SPACE]</b> 니트로 부스터
            </div>
        </div>

        <script>
            // === Three.js 씬 셋업 ===
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB); // 하늘색 배경
            scene.fog = new THREE.Fog(0x87CEEB, 100, 800); // 도심 안개 효과

            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // 조명
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
            dirLight.position.set(100, 200, 50);
            scene.add(dirLight);

            // === 차량 데이터 ===
            const carSpecs = {
                gtr: { color: 0x0055ff, maxSpeed: 2.2, accel: 0.015, handling: 0.3, nitroMax: 3.0 },
                svj: { color: 0xffaa00, maxSpeed: 2.5, accel: 0.012, handling: 0.25, nitroMax: 3.3 },
                porsche: { color: 0xffffff, maxSpeed: 2.1, accel: 0.018, handling: 0.4, nitroMax: 2.8 },
                ferrari: { color: 0xff0000, maxSpeed:
