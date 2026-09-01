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
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

            body { margin: 0; overflow: hidden; background-color: #050510; color: white; font-family: 'Orbitron', sans-serif; user-select: none; }
            
            /* === UI/UX Glassmorphism 디자인 === */
            #ui-layer {
                position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                pointer-events: none; display: flex; flex-direction: column;
            }

            .main-header {
                background: rgba(10, 10, 25, 0.6); padding: 15px 40px; 
                border-bottom: 2px solid #ff2a6d; 
                display: flex; justify-content: space-between; align-items: center;
                pointer-events: auto; backdrop-filter: blur(10px);
                box-shadow: 0 5px 30px rgba(255, 42, 109, 0.4);
            }
            .main-title { font-size: 28px; font-weight: 900; color: #05d9e8; text-shadow: 0 0 10px #05d9e8; letter-spacing: 3px; }
            .car-picker-container { display: flex; align-items: center; gap: 15px; }
            
            select { 
                background: rgba(5, 217, 232, 0.1); color: #05d9e8; padding: 10px 20px; 
                border: 1px solid #05d9e8; border-radius: 8px; font-size: 16px; 
                font-family: inherit; font-weight: bold; cursor: pointer; outline: none;
                box-shadow: 0 0 10px rgba(5, 217, 232, 0.3); transition: all 0.3s ease;
            }
            select:hover { background: rgba(5, 217, 232, 0.3); }
            option { background: #050510; color: white; }
            
            .hud-container {
                position: absolute; bottom: 40px; left: 40px;
                display: flex; gap: 25px; pointer-events: auto;
            }
            .hud-panel {
                background: rgba(10, 10, 25, 0.6); padding: 20px; 
                border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 10px 30px rgba(0,0,0,0.5); backdrop-filter: blur(10px);
                position: relative; overflow: hidden;
            }
            .hud-panel::before {
                content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px;
                background: linear-gradient(90deg, #ff2a6d, #01ffe5);
            }
            
            .hud-label { font-size: 12px; letter-spacing: 2px; color: #8892b0; margin-bottom: 8px; }
            .hud-value-container { display: flex; align-items: baseline; gap: 8px; }
            .hud-value { font-size: 42px; font-weight: 900; color: #fff; text-shadow: 0 0 15px rgba(255,255,255,0.5); }
            .hud-unit { font-size: 16px; font-weight: 700; color: #01ffe5; }

            #nitro-gauge {
                height: 14px; background: rgba(255,255,255,0.1); border-radius: 7px; overflow: hidden;
                margin-top: 15px; border: 1px solid rgba(255,255,255,0.2); width: 250px;
            }
            #nitro-bar {
                height: 100%; width: 100%; background: linear-gradient(90deg, #01ffe5, #ff2a6d);
                transition: width 0.1s linear; box-shadow: 0 0 15px #ff2a6d;
            }

            .right-hud-panel { position: absolute; bottom: 40px; right: 40px; pointer-events: auto; }

            .controls-panel { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px;}
            .key-box {
                width: 45px; height: 45px; background: rgba(255,255,255,0.05); 
                border: 1px solid rgba(255,255,255,0.2); border-radius: 8px;
                display: flex; align-items: center; justify-content: center;
                font-weight: 700; font-size: 18px; color: #8892b0; transition: all 0.1s;
            }
            .w-key { grid-column: 2 / 3; } .s-key { grid-column: 2 / 3; grid-row: 2 / 3; }
            .a-key { grid-column: 1 / 2; grid-row: 2 / 3; } .d-key { grid-column: 3 / 4; grid-row: 2 / 3; }
            .space-key { grid-column: 1 / 4; grid-row: 3 / 4; width: 100%; height: 35px; font-size: 14px; letter-spacing: 2px;}

            /* 키 눌림 효과 적용 클래스 */
            .key-active { background: #ff2a6d !important; color: white !important; box-shadow: 0 0 15px #ff2a6d, inset 0 0 10px rgba(0,0,0,0.5) !important; border-color: #ff2a6d !important; transform: translateY(2px); }
            .space-active { background: #01ffe5 !important; color: black !important; box-shadow: 0 0 15px #01ffe5 !important; border-color: #01ffe5 !important; transform: translateY(2px); }

            #finish-message {
                position: absolute; top: 35%; left: 50%; transform: translate(-50%, -50%);
                font-size: 100px; font-weight: 900; letter-spacing: 10px;
                background: linear-gradient(90deg, #ff2a6d, #01ffe5); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                text-shadow: 0 0 50px rgba(255, 42, 109, 0.5); display: none; text-align: center;
            }

            #restartBtn {
                position: absolute; bottom: 30%; left: 50%; transform: translateX(-50%);
                padding: 20px 50px; font-size: 24px; font-weight: 900; font-family: 'Orbitron', sans-serif;
                background: #01ffe5; color: #050510; border: none; border-radius: 12px; cursor: pointer; pointer-events: auto;
                box-shadow: 0 0 30px rgba(1, 255, 229, 0.6); display: none; transition: all 0.2s;
            }
            #restartBtn:hover { background: #ff2a6d; color: white; box-shadow: 0 0 40px rgba(255, 42, 109, 0.8); scale: 1.05; }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="ui-layer">
            <header class="main-header">
                <div class="main-title">NEON RACER : 2077</div>
                <div class="car-picker-container">
                    <label style="font-weight:700; color:#8892b0; letter-spacing:1px;">GARAGE :</label>
                    <select id="carSelect" onchange="changeCar()">
                        <option value="gtr">Nissan GT-R NISMO</option>
                        <option value="svj">Lambo Aventador SVJ</option>
                        <option value="porsche">Porsche 911 GT3</option>
                    </select>
                </div>
            </header>
            
            <div class="hud-container">
                <div class="hud-panel">
                    <div class="hud-label">CURRENT SPEED</div>
                    <div class="hud-value-container">
                        <div class="hud-value" id="speedUi">0</div>
                        <div class="hud-unit">KM/H</div>
                    </div>
                </div>
                <div class="hud-panel" style="width: 250px;">
                    <div class="hud-label">NITROUS SYSTEM</div>
                    <div id="nitro-gauge"><div id="nitro-bar"></div></div>
                </div>
                <div class="hud-panel">
                    <div class="hud-label">DISTANCE REMAINING</div>
                    <div class="hud-value-container">
                        <div class="hud-value" id="distUi">3000</div>
                        <div class="hud-unit">M</div>
                    </div>
                </div>
            </div>

            <div class="right-hud-panel hud-panel">
                <div class="hud-label" style="text-align: center;">DRIVE SYSTEM</div>
                <div class="controls-panel">
                    <div class="key-box w-key">W</div>
                    <div class="key-box a-key">A</div>
                    <div class="key-box s-key">S</div>
                    <div class="key-box d-key">D</div>
                    <div class="key-box space-key">SPACE (BOOST)</div>
                </div>
            </div>

            <div id="finish-message">RACE CLEARED</div>
            <button id="restartBtn" onclick="resetGame()">INITIALIZE RESTART</button>
        </div>

        <script>
            // === 1. 환상적인 Synthwave 씬 셋업 ===
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x050510);
            scene.fog = new THREE.FogExp2(0x050510, 0.003); // 원근감을 주는 안개

            const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 2000);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            document.body.appendChild(renderer.domElement);

            // 조명 세팅 (네온 감성)
            const ambientLight = new THREE.AmbientLight(0x222244, 1.5);
            scene.add(ambientLight);
            const spotLight = new THREE.SpotLight(0x01ffe5, 2);
            spotLight.position.set(0, 100, 50);
            spotLight.castShadow = true;
            scene.add(spotLight);
            const pinkLight = new THREE.PointLight(0xff2a6d, 1, 100);
            scene.add(pinkLight);

            // === 2. 환경 및 트랙 (네온 그리드 바닥) ===
            const gridHelper = new THREE.GridHelper(400, 80, 0xff2a6d, 0x222244);
            gridHelper.position.y = 0;
            scene.add(gridHelper);
            
            // 아스팔트 도로 
            const roadGeo = new THREE.PlaneGeometry(60, 4000);
            const roadMat = new THREE.MeshPhongMaterial({ color: 0x0a0a0a });
            const road = new THREE.Mesh(roadGeo, roadMat);
            road.rotation.x = -Math.PI / 2;
            road.position.z = -1500;
            road.receiveShadow = true;
            scene.add(road);

            // 가로등/네온 기둥 추가
            const pillars = new THREE.Group();
            for(let i=0; i<50; i++) {
                const pGeo = new THREE.CylinderGeometry(0.5, 0.5, 20, 8);
                const pMat = new THREE.MeshBasicMaterial({ color: i%2===0 ? 0x01ffe5 : 0xff2a6d });
                const p1 = new THREE.Mesh(pGeo, pMat);
                p1.position.set(-32, 10, -i*80);
                const p2 = new THREE.Mesh(pGeo, pMat);
                p2.position.set(32, 10, -i*80);
                pillars.add(p1); pillars.add(p2);
            }
            scene.add(pillars);

            // 결승선
            const finishGeo = new THREE.BoxGeometry(60, 2, 2);
            const finishMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
            const finishLine = new THREE.Mesh(finishGeo, finishMat);
            finishLine.position.set(0, 1, -3000);
            scene.add(finishLine);

            // === 3. 정교화된 차량 시스템 ===
            const playerCarModel = new THREE.Group();
            let wheels = []; // 바퀴 회전 애니메이션을 위한 배열

            const carSpecs = {
                gtr: { color: 0xffffff, accent: 0xff0000, maxSpeed: 2.8, accel: 0.02, handling: 0.4, nitroMax: 4.0 },
                svj: { color: 0xffaa00, accent: 0x000000, maxSpeed: 3.1, accel: 0.015, handling: 0.35, nitroMax: 4.5 },
                porsche: { color: 0x22aa33, accent: 0xffffff, maxSpeed: 2.7, accel: 0.025, handling: 0.5, nitroMax: 3.8 }
            };

            let currentCarType = "gtr";
            let playerSpeed = 0;
            let currentNitro = 100;
            let progressDist = 3000;
            let isFinished = false;

            function buildCarModel(carType) {
                while(playerCarModel.children.length > 0) { playerCarModel.remove(playerCarModel.children[0]); }
                wheels = [];
                const spec = carSpecs[carType];

                // 바디
                const bodyMat = new THREE.MeshPhongMaterial({ color: spec.color, shininess: 100 });
                const bodyMesh = new THREE.Mesh(new THREE.BoxGeometry(4.2, 1.2, 9), bodyMat);
                bodyMesh.position.y = 1.2;
                bodyMesh.castShadow = true;
                playerCarModel.add(bodyMesh);

                // 루프(캐빈)
                const cabinMat = new THREE.MeshPhongMaterial({ color: 0x111111, shininess: 150 });
                const cabinMesh = new THREE.Mesh(new THREE.BoxGeometry(3.6, 1.0, 4.5), cabinMat);
                cabinMesh.position.set(0, 2.3, -0.5);
                playerCarModel.add(cabinMesh);

                // 스포일러
                const wingMesh = new THREE.Mesh(new THREE.BoxGeometry(4.6, 0.2, 1.2), new THREE.MeshPhongMaterial({ color: spec.accent }));
                wingMesh.position.set(0, 2.5, 4);
                playerCarModel.add(wingMesh);
                
                // 후미등 (네온 빛)
                const tailLightGeo = new THREE.BoxGeometry(1.2, 0.4, 0.1);
                const tailLightMat = new THREE.MeshBasicMaterial({ color: 0xff0000 });
                const tl1 = new THREE.Mesh(tailLightGeo, tailLightMat); tl1.position.set(1.4, 1.4, 4.55);
                const tl2 = new THREE.Mesh(tailLightGeo, tailLightMat); tl2.position.set(-1.4, 1.4, 4.55);
                playerCarModel.add(tl1); playerCarModel.add(tl2);

                // 바퀴 생성 및 배열에 저장 (회전을 위해)
                const wheelGeo = new THREE.CylinderGeometry(0.8, 0.8, 1, 16);
                const wheelMat = new THREE.MeshPhongMaterial({ color: 0x222222 });
                const wheelPos = [ {x: -2.3, z: -2.8}, {x: 2.3, z: -2.8}, {x: -2.3, z: 2.8}, {x: 2.3, z: 2.8} ];
                
                wheelPos.forEach(pos => {
                    const wheel = new THREE.Mesh(wheelGeo, wheelMat);
                    wheel.position.set(pos.x, 0.8, pos.z);
                    wheel.rotation.z = Math.PI / 2;
                    playerCarModel.add(wheel);
                    wheels.push(wheel);
                });
            }

            buildCarModel(currentCarType);
            scene.add(playerCarModel);

            // === 4. 조작 및 버그 픽스 시스템 ===
            const keys = { w: false, a: false, s: false, d: false, space: false };
            
            window.addEventListener('keydown', (e) => {
                const key = e.key.toLowerCase();
                if (keys.hasOwnProperty(key)) keys[key] = true;
                if (e.code === 'Space') keys.space = true;
                
                // UI 하이라이트
                if (['w', 'a', 's', 'd'].includes(key)) document.querySelector(`.${key}-key`).classList.add('key-active');
                if (e.code === 'Space') document.querySelector('.space-key').classList.add('space-active');
            });

            window.addEventListener('keyup', (e) => {
                const key = e.key.toLowerCase();
                if (keys.hasOwnProperty(key)) keys[key] = false;
                if (e.code === 'Space') keys.space = false;
                
                // UI 하이라이트 해제
                if (['w', 'a', 's', 'd'].includes(key)) document.querySelector(`.${key}-key`).classList.remove('key-active');
                if (e.code === 'Space') document.querySelector('.space-key').classList.remove('space-active');
            });

            window.changeCar = function() {
                currentCarType = document.getElementById("carSelect").value;
                buildCarModel(currentCarType);
                // ⚠️ 핵심 버그 수정: 차종 선택 후 포커스를 해제하여 키보드 입력 시 차종이 바뀌지 않게 함
                document.getElementById("carSelect").blur(); 
            };

            window.resetGame = function() {
                playerCarModel.position.set(0, 0, 0);
                playerCarModel.rotation.set(0, 0, 0);
                playerSpeed = 0; currentNitro = 100; progressDist = 3000; isFinished = false;
                document.getElementById("finish-message").style.display = "none";
                document.getElementById("restartBtn").style.display = "none";
                gridHelper.position.z = 0; // 그리드 초기화
            };

            // === 5. 메인 게임 루프 ===
            let cameraShake = 0;

            function animate() {
                requestAnimationFrame(animate);

                if (!isFinished) {
                    let spec = carSpecs[currentCarType];
                    let currentMax = spec.maxSpeed;

                    // 니트로 부스트 처리
                    const nitroBar = document.getElementById("nitro-bar");
                    if (keys.space && currentNitro > 0) {
                        currentMax = spec.nitroMax;
                        currentNitro -= 0.5;
                        camera.fov = THREE.MathUtils.lerp(camera.fov, 90, 0.1); // 시야각 줌아웃 연출
                        cameraShake = 0.15; // 부스터 시 카메라 진동
                    } else {
                        if (currentNitro < 100) currentNitro += 0.1;
                        camera.fov = THREE.MathUtils.lerp(camera.fov, 70, 0.1);
                        cameraShake = 0;
                    }
                    camera.updateProjectionMatrix();

                    // 가감속 및 물리
                    if (keys.w) {
                        playerSpeed += spec.accel;
                        if (playerSpeed > currentMax) playerSpeed = currentMax;
                    } else if (keys.s) {
                        playerSpeed -= 0.1;
                    } else {
                        playerSpeed -= 0.02; // 마찰 저항
                    }
                    if (playerSpeed < 0) playerSpeed = 0;

                    // 조향 시스템 (고속일수록 부드럽게)
                    let turnAmount = spec.handling * (playerSpeed / 1.5);
                    if (turnAmount > spec.handling) turnAmount = spec.handling; // 한계 조향각
                    
                    if (keys.a && playerCarModel.position.x > -28) {
                        playerCarModel.position.x -= turnAmount;
                        playerCarModel.rotation.y = THREE.MathUtils.lerp(playerCarModel.rotation.y, 0.15, 0.1);
                    } else if (keys.d && playerCarModel.position.x < 28) {
                        playerCarModel.position.x += turnAmount;
                        playerCarModel.rotation.y = THREE.MathUtils.lerp(playerCarModel.rotation.y, -0.15, 0.1);
                    } else {
                        playerCarModel.rotation.y = THREE.MathUtils.lerp(playerCarModel.rotation.y, 0, 0.1);
                    }

                    // 전진 처리 및 무한 그리드 착시 연출
                    playerCarModel.position.z -= playerSpeed;
                    progressDist -= playerSpeed;
                    
                    // 자동차 주변 네온 핑크 조명 이동
                    pinkLight.position.set(playerCarModel.position.x, 5, playerCarModel.position.z);

                    // 바퀴 회전 애니메이션 적용
                    wheels.forEach(wheel => { wheel.rotation.x -= playerSpeed * 0.5; });

                    // 완주 판정
                    if (progressDist <= 0) {
                        progressDist = 0;
                        isFinished = true;
                        document.getElementById("finish-message").style.display = "block";
                        document.getElementById("restartBtn").style.display = "block";
                    }

                    // 역동적인 카메라 백뷰 + 카메라 셰이크
                    let shakeX = (Math.random() - 0.5) * cameraShake * (playerSpeed / 3);
                    let shakeY = (Math.random() - 0.5) * cameraShake * (playerSpeed / 3);
                    
                    camera.position.x = THREE.MathUtils.lerp(camera.position.x, playerCarModel.position.x + shakeX, 0.1);
                    camera.position.y = THREE.MathUtils.lerp(camera.position.y, playerCarModel.position.y + 6 + shakeY, 0.1);
                    camera.position.z = THREE.MathUtils.lerp(camera.position.z, playerCarModel.position
