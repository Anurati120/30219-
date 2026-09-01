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
                ferrari: { color: 0xff0000, maxSpeed: 2.3, accel: 0.014, handling: 0.3, nitroMax: 3.1 },
                mclaren: { color: 0xff5500, maxSpeed: 2.4, accel: 0.013, handling: 0.28, nitroMax: 3.5 },
                bugatti: { color: 0x000033, maxSpeed: 2.8, accel: 0.008, handling: 0.18, nitroMax: 3.8 },
                aston: { color: 0x004411, maxSpeed: 2.1, accel: 0.015, handling: 0.35, nitroMax: 2.9 }
            };

            let currentCarType = "gtr";
            let playerSpeed = 0;
            let currentNitro = 100;
            let progressDist = 10000;
            let isFinished = false;

            // === 플레이어 차량 생성 (3D 블록 조합) ===
            const playerCar = new THREE.Group();
            
            // 차체 (Chassis)
            const bodyGeo = new THREE.BoxGeometry(4, 2, 9);
            const bodyMat = new THREE.MeshLambertMaterial({ color: carSpecs[currentCarType].color });
            const bodyMesh = new THREE.Mesh(bodyGeo, bodyMat);
            bodyMesh.position.y = 1.5;
            playerCar.add(bodyMesh);
            
            // 조종석 (Cabin)
            const cabinGeo = new THREE.BoxGeometry(3, 1.5, 4);
            const cabinMat = new THREE.MeshLambertMaterial({ color: 0x111111 });
            const cabinMesh = new THREE.Mesh(cabinGeo, cabinMat);
            cabinMesh.position.set(0, 3, -0.5);
            playerCar.add(cabinMesh);

            scene.add(playerCar);

            // === 트랙 및 환경 생성 ===
            // 도로
            const roadGeo = new THREE.PlaneGeometry(60, 20000);
            const roadMat = new THREE.MeshLambertMaterial({ color: 0x222222 });
            const road = new THREE.Mesh(roadGeo, roadMat);
            road.rotation.x = -Math.PI / 2;
            road.position.z = -9000;
            scene.add(road);

            // 중앙선 (Dashed line 효과를 위해 여러 개의 Plane 사용)
            const lines = new THREE.Group();
            for(let i=0; i<400; i++) {
                const lineGeo = new THREE.PlaneGeometry(1, 10);
                const lineMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
                const line = new THREE.Mesh(lineGeo, lineMat);
                line.rotation.x = -Math.PI / 2;
                line.position.set(0, 0.1, -i * 50);
                lines.add(line);
            }
            scene.add(lines);

            // 도심 빌딩 (배경 장식)
            const buildings = new THREE.Group();
            const buildGeo = new THREE.BoxGeometry(20, 100, 20);
            for(let i=0; i<100; i++) {
                const buildMat = new THREE.MeshLambertMaterial({ color: Math.random() * 0xffffff });
                const b1 = new THREE.Mesh(buildGeo, buildMat);
                b1.position.set(50 + Math.random()*20, 50, -Math.random()*10000);
                const b2 = new THREE.Mesh(buildGeo, buildMat);
                b2.position.set(-50 - Math.random()*20, 50, -Math.random()*10000);
                buildings.add(b1);
                buildings.add(b2);
            }
            scene.add(buildings);

            // 결승선
            const finishGeo = new THREE.PlaneGeometry(60, 5);
            const finishMat = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
            const finishLine = new THREE.Mesh(finishGeo, finishMat);
            finishLine.rotation.x = -Math.PI / 2;
            finishLine.position.set(0, 0.2, -10000);
            scene.add(finishLine);

            // 장애물(트래픽 차량)
            const traffic = [];
            const trafficGeo = new THREE.BoxGeometry(4, 2.5, 9);
            const trafficMat = new THREE.MeshLambertMaterial({ color: 0xaa0000 });
            for(let i=0; i<80; i++) {
                const tr = new THREE.Mesh(trafficGeo, trafficMat);
                tr.position.set((Math.random() - 0.5) * 50, 1.25, -500 - (Math.random() * 9000));
                scene.add(tr);
                traffic.push(tr);
            }

            // === 입력 처리 (WASD) ===
            const keys = { w: false, a: false, s: false, d: false, space: false };
            window.addEventListener('keydown', (e) => {
                const key = e.key.toLowerCase();
                if (key === 'w') keys.w = true;
                if (key === 'a') keys.a = true;
                if (key === 's') keys.s = true;
                if (key === 'd') keys.d = true;
                if (e.code === 'Space') keys.space = true;
            });
            window.addEventListener('keyup', (e) => {
                const key = e.key.toLowerCase();
                if (key === 'w') keys.w = false;
                if (key === 'a') keys.a = false;
                if (key === 's') keys.s = false;
                if (key === 'd') keys.d = false;
                if (e.code === 'Space') keys.space = false;
            });

            window.changeCar = function() {
                currentCarType = document.getElementById("carSelect").value;
                bodyMesh.material.color.setHex(carSpecs[currentCarType].color);
            };

            window.resetGame = function() {
                playerCar.position.set(0, 0, 0);
                playerSpeed = 0;
                currentNitro = 100;
                progressDist = 10000;
                isFinished = false;
                document.getElementById("message").style.display = "none";
                document.getElementById("restartBtn").style.display = "none";
            };

            // === 게임 루프 ===
            function animate() {
                requestAnimationFrame(animate);

                if (!isFinished) {
                    let spec = carSpecs[currentCarType];
                    let currentMax = spec.maxSpeed;

                    // 부스터 (SPACE)
                    if (keys.space && currentNitro > 0) {
                        currentMax = spec.nitroMax;
                        currentNitro -= 0.5;
                        camera.fov = 85; // 부스터 시 시야각 넓어짐 (속도감 연출)
                    } else {
                        if (currentNitro < 100) currentNitro += 0.1;
                        camera.fov = 75;
                    }
                    camera.updateProjectionMatrix();

                    // 가속 & 감속 (W, S)
                    if (keys.w) {
                        playerSpeed += spec.accel;
                        if (playerSpeed > currentMax) playerSpeed = currentMax;
                    } else if (keys.s) {
                        playerSpeed -= 0.05;
                    } else {
                        playerSpeed -= 0.01; // 자연 감속
                    }
                    if (playerSpeed < 0) playerSpeed = 0;

                    // 좌우 조향 (A, D) - 속도에 비례해서 꺾임
                    if (keys.a && playerCar.position.x > -28) {
                        playerCar.position.x -= spec.handling * (playerSpeed/1.5);
                        playerCar.rotation.y = 0.1;
                    } else if (keys.d && playerCar.position.x < 28) {
                        playerCar.position.x += spec.handling * (playerSpeed/1.5);
                        playerCar.rotation.y = -0.1;
                    } else {
                        playerCar.rotation.y = 0;
                    }

                    // 전진
                    playerCar.position.z -= playerSpeed;
                    progressDist = 10000 + playerCar.position.z;

                    // 충돌 감지 (벽 및 트래픽)
                    // 1. 코스 이탈 페널티
                    if (playerCar.position.x <= -28 || playerCar.position.x >= 28) {
                        playerSpeed *= 0.8; // 속도 급감
                    }
                    // 2. 트래픽 차량 충돌 페널티
                    for(let i=0; i<traffic.length; i++) {
                        let tr = traffic[i];
                        if (Math.abs(playerCar.position.z - tr.position.z) < 9 && 
                            Math.abs(playerCar.position.x - tr.position.x) < 4) {
                            playerSpeed *= 0.4; // 강하게 속도 감소 (카트라이더 방식 페널티)
                            playerCar.position.z += 2; // 살짝 튕겨나감
                        }
                    }

                    // 완주 체크
                    if (progressDist <= 0) {
                        isFinished = true;
                        document.getElementById("message").style.display = "block";
                        document.getElementById("restartBtn").style.display = "block";
                    }

                    // 카메라 추적 (3인칭 백뷰)
                    camera.position.x = playerCar.position.x;
                    camera.position.y = playerCar.position.y + 7;
                    camera.position.z = playerCar.position.z + 20;
                    camera.lookAt(playerCar.position.x, playerCar.position.y, playerCar.position.z - 10);

                    // UI 업데이트
                    document.getElementById("speedUi").innerText = Math.floor(playerSpeed * 120);
                    document.getElementById("nitroUi").innerText = Math.floor(currentNitro);
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

    # height를 넉넉하게 주어 전체화면 느낌을 살림
    st.components.v1.html(game_html, height=800, scrolling=False)

if __name__ == "__main__":
    run_game()
