import streamlit as st

st.set_page_config(
    page_title="3D Supercar World Racing",
    page_icon="🏎️",
    layout="wide",
)

def run_game():
    game_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>3D Supercar World Racing</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');

            body { margin: 0; overflow: hidden; background-color: #0c0e14; color: white; font-family: 'Montserrat', sans-serif; }
            
            /* === UI/UX 대폭 개선 (1000% 멋짐) === */
            #ui-layer {
                position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                pointer-events: none; display: flex; flex-direction: column;
            }

            .main-header {
                background: rgba(12, 14, 20, 0.85); padding: 15px 40px; 
                border-bottom: 3px solid #ffcc00; 
                display: flex; justify-content: space-between; align-items: center;
                pointer-events: auto; backdrop-filter: blur(5px);
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.6);
            }
            .main-title { font-size: 28px; font-weight: 900; color: #ffcc00; text-transform: uppercase; letter-spacing: 2px; }
            .car-picker-container { display: flex; align-items: center; gap: 15px; }
            select { background: #1a1e28; color: #fff; padding: 10px 15px; border: 1px solid #444; border-radius: 8px; font-size: 16px; font-family: inherit; cursor: pointer; }
            
            .hud-container {
                position: absolute; bottom: 30px; left: 30px;
                display: flex; gap: 20px;
                pointer-events: auto;
            }
            .hud-panel {
                background: rgba(26, 30, 40, 0.8); padding: 15px; 
                border-radius: 12px; border: 1px solid #333;
                box-shadow: 0 4px 15px rgba(0,0,0,0.4);
                backdrop-filter: blur(5px);
            }
            .hud-label { font-size: 12px; text-transform: uppercase; color: #aaa; margin-bottom: 5px; }
            .hud-value-container { display: flex; align-items: flex-end; gap: 5px; }
            .hud-value { font-size: 36px; font-weight: 900; color: #ffcc00; }
            .hud-unit { font-size: 14px; font-weight: 700; color: #aaa; }

            #nitro-gauge {
                height: 10px; background: #222; border-radius: 5px; overflow: hidden;
                margin-top: 10px; border: 1px solid #333;
            }
            #nitro-bar {
                height: 100%; width: 100%; background: #00ffcc;
                transition: width 0.1s linear, background 0.3s;
                box-shadow: 0 0 10px #00ffcc;
            }

            .right-hud-panel {
                position: absolute; top: 100px; right: 30px;
                pointer-events: auto;
            }

            .controls-panel {
                background: rgba(26, 30, 40, 0.8); padding: 15px; 
                border-radius: 12px; border: 1px solid #333;
                backdrop-filter: blur(5px);
                font-size: 14px; text-align: center;
                display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;
            }
            .key-box {
                width: 40px; height: 40px; background: #333; 
                border: 1px solid #555; border-radius: 6px;
                display: flex; align-items: center; justify-content: center;
                font-weight: 700;
            }
            .w-key { grid-column: 2 / 3; }
            .s-key { grid-column: 2 / 3; grid-row: 2 / 3; }
            .a-key { grid-column: 1 / 2; grid-row: 2 / 3; }
            .d-key { grid-column: 3 / 4; grid-row: 2 / 3; }
            .space-key { grid-column: 1 / 4; grid-row: 3 / 4; width: 100%; height: 30px; }

            #finish-message {
                position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);
                font-size: 80px; font-weight: 900; text-transform: uppercase; letter-spacing: 5px;
                background: linear-gradient(90deg, #ffcc00, #ff00cc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                text-shadow: 0 0 30px rgba(255, 204, 0, 0.8); display: none; text-align: center;
            }

            #restartBtn {
                position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
                padding: 18px 45px; font-size: 22px; font-weight: 900; text-transform: uppercase;
                background: #ffcc00; color: #000; border: none; border-radius: 12px; cursor: pointer; pointer-events: auto;
                box-shadow: 0 0 25px rgba(255, 204, 0, 0.7); display: none;
                transition: transform 0.1s, box-shadow 0.2s;
            }
            #restartBtn:hover { transform: translateX(-50%) scale(1.05); box-shadow: 0 0 35px rgba(255, 204, 0, 0.9); }

        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="ui-layer">
            <header class="main-header">
                <div class="main-title">3D Supercar Racing</div>
                <div class="car-picker-container">
                    <label>SELECTED CAR:</label>
                    <select id="carSelect" onchange="changeCar()">
                        <option value="gtr">Nissan GT-R NISMO</option>
                        <option value="svj">Lambo Aventador SVJ</option>
                        <option value="porsche">Porsche 911 GT3</option>
                        <option value="ferrari">Ferrari 488 Pista</option>
                        <option value="mclaren">McLaren 720S</option>
                        <option value="bugatti">Bugatti Chiron</option>
                        <option value="aston">Aston Martin Vantage</option>
                    </select>
                </div>
            </header>
            
            <div class="hud-container">
                <div class="hud-panel">
                    <div class="hud-label">SPEED</div>
                    <div class="hud-value-container">
                        <div class="hud-value" id="speedUi">0</div>
                        <div class="hud-unit">km/h</div>
                    </div>
                </div>
                <div class="hud-panel" style="flex: 1; border-left: 4px solid #00ffcc;">
                    <div class="hud-label">NITRO BOOST</div>
                    <div id="nitro-gauge"><div id="nitro-bar"></div></div>
                </div>
                <div class="hud-panel">
                    <div class="hud-label">DISTANCE TO FINISH</div>
                    <div class="hud-value-container">
                        <div class="hud-value" id="distUi">10000</div>
                        <div class="hud-unit">m</div>
                    </div>
                </div>
            </div>

            <div class="right-hud-panel hud-panel">
                <div class="hud-label">CONTROLS</div>
                <div class="controls-panel">
                    <div class="key-box w-key">W</div>
                    <div class="key-box a-key">A</div>
                    <div class="key-box s-key">S</div>
                    <div class="key-box d-key">D</div>
                    <div class="key-box space-key">SPACE</div>
                </div>
            </div>

            <div id="finish-message">FINISH!</div>
            <button id="restartBtn" onclick="resetGame()">🔄 RESTART RACE</button>
        </div>

        <script>
            // === Three.js 씬 셋업 (GTA & 카트라이더 융합 배경) ===
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x1a2133); // 밤하늘 도심 분위기
            scene.fog = new THREE.Fog(0x1a2133, 150, 1000); // 도심 안개 효과

            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1500);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // 조명 (밤 도심 조명)
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
            scene.add(ambientLight);
            const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
            dirLight.position.set(100, 200, 50);
            scene.add(dirLight);

            // === 정교한 3D 차량 모델링 (GTR NISMO 특징 반영) ===
            const playerCarModel = new THREE.Group();

            const carSpecs = {
                gtr: { color: 0xffffff, roofColor: 0x111111, accentColor: 0xdd0000, maxSpeed: 2.3, accel: 0.016, handling: 0.35, nitroMax: 3.1 },
                svj: { color: 0xffaa00, roofColor: 0x111111, accentColor: 0xff4400, maxSpeed: 2.6, accel: 0.013, handling: 0.28, nitroMax: 3.4 },
                porsche: { color: 0xffffff, roofColor: 0x111111, accentColor: 0xff0000, maxSpeed: 2.2, accel: 0.019, handling: 0.45, nitroMax: 2.9 },
                ferrari: { color: 0xff0000, roofColor: 0x111111, accentColor: 0x000000, maxSpeed: 2.4, accel: 0.015, handling: 0.38, nitroMax: 3.2 },
                mclaren: { color: 0xff7700, roofColor: 0x111111, accentColor: 0xffffff, maxSpeed: 2.5, accel: 0.014, handling: 0.32, nitroMax: 3.6 },
                bugatti: { color: 0x000033, roofColor: 0x000011, accentColor: 0x55ccff, maxSpeed: 2.9, accel: 0.009, handling: 0.20, nitroMax: 3.9 },
                aston: { color: 0x004411, roofColor: 0x111111, accentColor: 0xffffff, maxSpeed: 2.2, accel: 0.016, handling: 0.4, nitroMax: 3.0 }
            };

            let currentCarType = "gtr";
            let playerSpeed = 0;
            let currentNitro = 100;
            let progressDist = 10000;
            let isFinished = false;

            // 정교한 기하학적 블록으로 GTR NISMO 모델링 구축
            function buildCarModel(carType) {
                // 기존 모델 초기화
                while(playerCarModel.children.length > 0){ 
                    playerCarModel.remove(playerCarModel.children[0]); 
                }

                const spec = carSpecs[carType];

                // === 차체 구축 ===
                // 메인 바디
                const bodyGeo = new THREE.BoxGeometry(4, 2, 9);
                const bodyMat = new THREE.MeshLambertMaterial({ color: spec.color });
                const bodyMesh = new THREE.Mesh(bodyGeo, bodyMat);
                bodyMesh.position.y = 1.5;
                playerCarModel.add(bodyMesh);

                // 프론트 노즈 (GTR의 특징적인 그릴 형태)
                const frontNoseGeo = new THREE.BoxGeometry(4, 1.5, 3);
                const frontNoseMesh = new THREE.Mesh(frontNoseGeo, bodyMat);
                frontNoseMesh.position.set(0, 1.25, -4.5);
                playerCarModel.add(frontNoseMesh);

                // 리어 바디
                const rearBodyGeo = new THREE.BoxGeometry(4, 1.8, 3);
                const rearBodyMesh = new THREE.Mesh(rearBodyGeo, bodyMat);
                rearBodyMesh.position.set(0, 1.4, 4.5);
                playerCarModel.add(rearBodyMesh);

                // 조종석 (Cabin) & 검은색 루프 (NISMO)
                const cabinGeo = new THREE.BoxGeometry(3.5, 1.8, 4.5);
                const cabinMat = new THREE.MeshLambertMaterial({ color: 0x050505 }); // 유리
                const cabinMesh = new THREE.Mesh(cabinGeo, cabinMat);
                cabinMesh.position.set(0, 3, -1);
                playerCarModel.add(cabinMesh);

                const roofGeo = new THREE.BoxGeometry(3.6, 0.2, 4.6);
                const roofMat = new THREE.MeshLambertMaterial({ color: spec.roofColor });
                const roofMesh = new THREE.Mesh(roofGeo, roofMat);
                roofMesh.position.set(0, 3.9, -1);
                playerCarModel.add(roofMesh);

                // === NISMO 특징 구현 ===
                // 1. 대형 리어 윙 (NISMO 대형 탄소 섬유 스포일러)
                const wingBladeGeo = new THREE.BoxGeometry(4.8, 0.1, 1.8);
                const wingMat = new THREE.MeshLambertMaterial({ color: spec.roofColor });
                const wingBlade = new THREE.Mesh(wingBladeGeo, wingMat);
                wingBlade.position.set(0, 4.5, 4);
                playerCarModel.add(wingBlade);
                
                // 윙 지지대
                const wingStandGeo = new THREE.BoxGeometry(0.1, 1, 0.1);
                const wingStand1 = new THREE.Mesh(wingStandGeo, wingMat);
                wingStand1.position.set(1.5, 4, 3.8);
                const wingStand2 = new THREE.Mesh(wingStandGeo, wingMat);
                wingStand2.position.set(-1.5, 4, 3.8);
                playerCarModel.add(wingStand1);
                playerCarModel.add(wingStand2);

                // 2. 프론트 에어 덕트 & 빨간색 NISMO 액센트 라인
                const accentGeo = new THREE.BoxGeometry(4.1, 0.1, 0.1);
                const accentMat = new THREE.MeshLambertMaterial({ color: spec.accentColor });
                const frontAccent = new THREE.Mesh(accentGeo, accentMat);
                frontAccent.position.set(0, 0.5, -5.9);
                playerCarModel.add(frontAccent);

                // 3. 헤드라이트 (NISMO LED)
                const headGeo = new THREE.BoxGeometry(0.8, 0.3, 0.1);
                const headMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
                const head1 = new THREE.Mesh(headGeo, headMat);
                head1.position.set(1.2, 1.8, -5.9);
                const head2 = new THREE.Mesh(headGeo, headMat);
                head2.position.set(-1.2, 1.8, -5.9);
                playerCarModel.add(head1);
                playerCarModel.add(head2);

                // === 휠 & 타이어 ===
                const wheelGeo = new THREE.CylinderGeometry(0.8, 0.8, 0.8, 16);
                const wheelMat = new THREE.MeshLambertMaterial({ color: 0x1a1a1a });
                const wheelPositions = [
                    { x: -2.1, y: 0.8, z: -3 },
                    { x: 2.1, y: 0.8, z: -3 },
                    { x: -2.1, y: 0.8, z: 3 },
                    { x: 2.1, y: 0.8, z: 3 }
                ];
                wheelPositions.forEach(pos => {
                    const wheel = new THREE.Mesh(wheelGeo, wheelMat);
                    wheel.position.set(pos.x, pos.y, pos.z);
                    wheel.rotation.z = Math.PI / 2;
                    playerCarModel.add(wheel);
                });
            }

            buildCarModel(currentCarType);
            scene.add(playerCarModel);

            // === 트랙 및 환경 생성 ===
            // 도로
            const roadGeo = new THREE.PlaneGeometry(80, 20000);
            const roadMat = new THREE.MeshLambertMaterial({ color: 0x111111 });
            const road = new THREE.Mesh(roadGeo, roadMat);
            road.rotation.x = -Math.PI / 2;
            road.position.z = -9000;
            scene.add(road);

            // 도로 가장자리 네온 라인 (카트라이더 느낌)
            const neonGeo = new THREE.PlaneGeometry(1, 20000);
            const neonMat = new THREE.MeshBasicMaterial({ color: 0x00ffff });
            const neon1 = new THREE.Mesh(neonGeo, neonMat);
            neon1.rotation.x = -Math.PI / 2;
            neon1.position.set(-39, 0.1, -9000);
            const neon2 = new THREE.Mesh(neonGeo, neonMat);
            neon2.rotation.x = -Math.PI / 2;
            neon2.position.set(39, 0.1, -9000);
            scene.add(neon1);
            scene.add(neon2);

            // 중앙선
            const lines = new THREE.Group();
            for(let i=0; i<400; i++) {
                const lineGeo = new THREE.PlaneGeometry(1.5, 12);
                const lineMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
                const line = new THREE.Mesh(lineGeo, lineMat);
                line.rotation.x = -Math.PI / 2;
                line.position.set(0, 0.1, -i * 50);
                lines.add(line);
            }
            scene.add(lines);

            // 도심 빌딩 (GTA 느낌 배경)
            const buildings = new THREE.Group();
            const buildGeo = new THREE.BoxGeometry(20, 100, 20);
            for(let i=0; i<100; i++) {
                const buildMat = new THREE.MeshLambertMaterial({ color: Math.random() * 0xffffff });
                const b1 = new THREE.Mesh(buildGeo, buildMat);
                b1.position.set(60 + Math.random()*20, 50, -Math.random()*10000);
                const b2 = new THREE.Mesh(buildGeo, buildMat);
                b2.position.set(-60 - Math.random()*20, 50, -Math.random()*10000);
                buildings.add(b1);
                buildings.add(b2);
            }
            scene.add(buildings);

            // 결승선
            const finishGeo = new THREE.PlaneGeometry(80, 10);
            const finishMat = new THREE.MeshBasicMaterial({ color: 0xffcc00 });
            const finishLine = new THREE.Mesh(finishGeo, finishMat);
            finishLine.rotation.x = -Math.PI / 2;
            finishLine.position.set(0, 0.2, -10000);
            scene.add(finishLine);

            // 장애물(트래픽 차량)
            const traffic = [];
            const trafficGeo = new THREE.BoxGeometry(4.5, 2.8, 10);
            const trafficMat = new THREE.MeshLambertMaterial({ color: 0xaa0000 });
            for(let i=0; i<80; i++) {
                const tr = new THREE.Mesh(trafficGeo, trafficMat);
                tr.position.set((Math.random() - 0.5) * 70, 1.4, -500 - (Math.random() * 9500));
                scene.add(tr);
                traffic.push(tr);
            }

            // === 입력 처리 (WASD - 에러 없이 정교하게) ===
            const keys = { w: false, a: false, s: false, d: false, space: false };
            window.addEventListener('keydown', (e) => {
                const key = e.key.toLowerCase();
                if (keys.hasOwnProperty(key)) keys[key] = true;
                if (e.code === 'Space') keys.space = true;
                
                // UI Key Highlight
                if (key === 'w' || key === 's' || key === 'a' || key === 'd') {
                    document.querySelector(`.${key}-key`).style.background = '#ffcc00';
                    document.querySelector(`.${key}-key`).style.color = '#000';
                }
                if (e.code === 'Space') {
                    document.querySelector('.space-key').style.background = '#00ffcc';
                    document.querySelector('.space-key').style.color = '#000';
                }
            });
            window.addEventListener('keyup', (e) => {
                const key = e.key.toLowerCase();
                if (keys.hasOwnProperty(key)) keys[key] = false;
                if (e.code === 'Space') keys.space = false;
                
                // UI Key Unhighlight
                if (key === 'w' || key === 's' || key === 'a' || key === 'd') {
                    document.querySelector(`.${key}-key`).style.background = '';
                    document.querySelector(`.${key}-key`).style.color = '';
                }
                if (e.code === 'Space') {
                    document.querySelector('.space-key').style.background = '';
                    document.querySelector('.space-key').style.color = '';
                }
            });

            window.changeCar = function() {
                currentCarType = document.getElementById("carSelect").value;
                buildCarModel(currentCarType);
            };

            window.resetGame = function() {
                playerCarModel.position.set(0, 0, 0);
                playerSpeed = 0;
                currentNitro = 100;
                progressDist = 10000;
                isFinished = false;
                document.getElementById("finish-message").style.display = "none";
                document.getElementById("restartBtn").style.display = "none";
            };

            // === 게임 루프 ===
            function animate() {
                requestAnimationFrame(animate);

                if (!isFinished) {
                    let spec = carSpecs[currentCarType];
                    let currentMax = spec.maxSpeed;

                    // 부스터 (SPACE - 카트라이더 연출)
                    const nitroBar = document.getElementById("nitro-bar");
                    if (keys.space && currentNitro > 0) {
                        currentMax = spec.nitroMax;
                        currentNitro -= 0.6;
                        camera.fov = 85; // 부스터 시야각
                        nitroBar.style.background = "#ffcc00"; // 부스터 색상 변화
                        nitroBar.style.boxShadow = "0 0 15px #ffcc00";
                    } else {
                        if (currentNitro < 100) currentNitro += 0.15;
                        camera.fov = 75;
                        nitroBar.style.background = ""; // 기본 색상
                        nitroBar.style.boxShadow = "";
                    }
                    camera.updateProjectionMatrix();

                    // 가속 & 감속 (W, S)
                    if (keys.w) {
                        playerSpeed += spec.accel;
                        if (playerSpeed > currentMax) playerSpeed = currentMax;
                    } else if (keys.s) {
                        playerSpeed -= 0.06;
                    } else {
                        playerSpeed -= 0.015; // 자연 감속
                    }
                    if (playerSpeed < 0) playerSpeed = 0;

                    // 좌우 조향 (A, D) - 속도 비례
                    if (keys.a && playerCarModel.position.x > -37) {
                        playerCarModel.position.x -= spec.handling * (playerSpeed/1.5);
                        playerCarModel.rotation.y = 0.12;
                    } else if (keys.d && playerCarModel.position.x < 37) {
                        playerCarModel.position.x += spec.handling * (playerSpeed/1.5);
                        playerCarModel.rotation.y = -0.12;
                    } else {
                        playerCarModel.rotation.y = 0;
                    }

                    // 전진
                    playerCarModel.position.z -= playerSpeed;
                    progressDist = 10000 + playerCarModel.position.z;

                    // 충돌 감지 (카트라이더 방식 페널티 - 속도 감소 및 튕김)
                    if (playerCarModel.position.x <= -37 || playerCarModel.position.x >= 37) {
                        playerSpeed *= 0.85; // 코스 이탈 페널티
                    }
                    for(let i=0; i<traffic.length; i++) {
                        let tr = traffic[i];
                        if (Math.abs(playerCarModel.position.z - tr.position.z) < 10 && 
                            Math.abs(playerCarModel.position.x - tr.position.x) < 4.5) {
                            playerSpeed *= 0.45; // 트래픽 충돌 페널티
                            playerCarModel.position.z += 3; // 약간 튕겨나감
                        }
                    }

                    // 완주 체크
                    if (progressDist <= 0) {
                        isFinished = true;
                        document.getElementById("finish-message").style.display = "block";
                        document.getElementById("restartBtn").style.display = "block";
                    }

                    // 카메라 추적 (3인칭 백뷰)
                    camera.position.x = playerCarModel.position.x;
                    camera.position.y = playerCarModel.position.y + 7;
                    camera.position.z = playerCarModel.position.z + 23;
                    camera.lookAt(playerCarModel.position.x, playerCarModel.position.y, playerCarModel.position.z - 10);

                    // UI 업데이트
                    document.getElementById("speedUi").innerText = Math.floor(playerSpeed * 120);
                    nitroBar.style.width = currentNitro + "%";
                    document.getElementById("distUi").innerText = Math.max(0, Math.floor(progressDist));
                }

                renderer.render(scene, camera);
            }

            // 반응형 리사이징
            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });

            animate();
        </script>
    </body>
    </html>
    """

    st.components.v1.html(game_html, height=850, scrolling=False)

if __name__ == "__main__":
    run_game()
