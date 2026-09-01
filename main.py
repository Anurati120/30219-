import streamlit as st

st.set_page_config(
    page_title="High-End Sports Car Racing",
    page_icon="🏎️",
    layout="wide",
)


def run_code():
  # HTML, CSS, JavaScript를 활용한 고성능 웹 레이싱 게임 엔진
  game_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>Sports Car Racing</title>
        <style>
            body {
                background-color: #121212;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            #game-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-top: 20px;
            }
            canvas {
                background: #2b2b2b;
                border: 4px solid #00ffcc;
                box-shadow: 0 0 20px rgba(0, 255, 204, 0.5);
            }
            .ui-panel {
                margin-top: 15px;
                display: flex;
                gap: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            .control-box {
                margin-top: 20px;
                background: #1e1e1e;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #444;
                max-width: 600px;
            }
            select {
                padding: 8px;
                background: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <div id="game-container">
            <h1>🏎️ SUPREME SPORTS CAR RACING</h1>
            <div>
                <label for="carSelect">차량 선택: </label>
                <select id="carSelect" onchange="changeCar()">
                    <option value="gtr">Nissan GT-R Skyline R34 (Twin-Turbo I6)</option>
                    <option value="lambo">Lamborghini Aventador SVJ (V12 Naturally Aspirated)</option>
                </select>
            </div>
            
            <canvas id="gameCanvas" width="800" height="500"></canvas>
            
            <div class="ui-panel">
                <div>속도: <span id="speedDisplay">0</span> km/h</div>
                <div>점수: <span id="scoreDisplay">0</span></div>
                <div>부스터 게이지: <span id="nitroDisplay">100</span>%</div>
            </div>

            <div class="control-box">
                <p>🎮 <b>조작 방법</b>: 방향키 [←] [→] 이동 | [↑] 가속 | [↓] 브레이크 | [SPACE] 카트라이더식 부스터</p>
                <p id="carDesc" style="color: #00ffcc; font-size: 14px;"></p>
            </div>
        </div>

        <script>
            const canvas = document.getElementById("gameCanvas");
            const ctx = canvas.getContext("2d");

            // 차량 디테일 설정 데이터
            const cars = {
                gtr: {
                    name: "Nissan GT-R Skyline R34",
                    color: "#0055ff",
                    accent: "#00ffff",
                    maxSpeed: 12,
                    accel: 0.2,
                    handling: 6,
                    desc: "전설의 RB26DETT 트윈터보 엔진 탑재. 완벽한 4륜구동 트랙션과 코너링 안정성 제공."
                },
                lambo: {
                    name: "Lamborghini Aventador SVJ",
                    color: "#ffcc00",
                    accent: "#ff3300",
                    maxSpeed: 16,
                    accel: 0.3,
                    handling: 5,
                    desc: "6.5리터 V12 자연흡기 엔진과 ALA 2.0 공기역학 시스템으로 무장한 트랙의 괴물."
                }
            };

            let currentCarKey = "gtr";
            let car = {
                x: 375,
                y: 400,
                width: 50,
                height: 90,
                speed: 0,
                maxSpeed: 12,
                accel: 0.2,
                handling: 6,
                nitro: 100
            };

            let keys = {};
            let obstacles = [];
            let roadOffset = 0;
            let score = 0;
            let isGameOver = false;

            function changeCar() {
                const select = document.getElementById("carSelect");
                currentCarKey = select.value;
                let spec = cars[currentCarKey];
                car.maxSpeed = spec.maxSpeed;
                car.accel = spec.accel;
                car.handling = spec.handling;
                document.getElementById("carDesc").innerText = spec.desc;
            }
            changeCar();

            window.addEventListener("keydown", (e) => { keys[e.code] = true; });
            window.addEventListener("keyup", (e) => { keys[e.code] = false; });

            function spawnObstacle() {
                if (Math.random() < 0.03) {
                    let obsX = Math.random() * (canvas.width - 150) + 75;
                    obstacles.push({ x: obsX, y: -100, width: 50, height: 90, speed: 4 + Math.random() * 3 });
                }
            }

            function update() {
                if (isGameOver) return;

                // 가속 및 감속
                if (keys["ArrowUp"]) {
                    if (car.speed < car.maxSpeed) car.speed += car.accel;
                } else if (keys["ArrowDown"]) {
                    if (car.speed > 0) car.speed -= 0.4;
                } else {
                    if (car.speed > 0) car.speed -= 0.1;
                }

                // 카트라이더식 부스터 (스페이스바)
                if (keys["Space"] && car.nitro > 0) {
                    car.maxSpeed = 22;
                    car.nitro -= 1.5;
                } else {
                    car.maxSpeed = cars[currentCarKey].maxSpeed;
                    if (car.nitro < 100 && !keys["Space"]) car.nitro += 0.2;
                }

                // 좌우 이동
                if (keys["ArrowLeft"] && car.x > 75) {
                    car.x -= car.handling;
                }
                if (keys["ArrowRight"] && car.x < canvas.width - 125) {
                    car.x += car.handling;
                }

                roadOffset += car.speed;
                score += Math.floor(car.speed);

                // 장애물 업데이트
                for (let i = obstacles.length - 1; i >= 0; i--) {
                    obstacles[i].y += car.speed + obstacles[i].speed;

                    // 충돌 감지
                    if (
                        car.x < obstacles[i].x + obstacles[i].width &&
                        car.x + car.width > obstacles[i].x &&
                        car.y < obstacles[i].y + obstacles[i].height &&
                        car.y + car.height > obstacles[i].y
                    ) {
                        isGameOver = true;
                    }

                    // 화면 밖으로 나간 장애물 제거
                    if (obstacles[i].y > canvas.height) {
                        obstacles.splice(i, 1);
                    }
                }

                spawnObstacle();
            }

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // 도로 그리기
                ctx.fillStyle = "#333";
                ctx.fillRect(50, 0, canvas.width - 100, canvas.height);

                // 도로 가장자라 라인
                ctx.fillStyle = "#fff";
                ctx.fillRect(45, 0, 5, canvas.height);
                ctx.fillRect(canvas.width - 50, 0, 5, canvas.height);

                // 중앙선 점선 애니메이션
                ctx.strokeStyle = "#ffcc00";
                ctx.lineWidth = 6;
                ctx.setLineDash([30, 30]);
                ctx.lineDashOffset = -roadOffset;
                ctx.beginPath();
                ctx.moveTo(canvas.width / 2, 0);
                ctx.lineTo(canvas.width / 2, canvas.height);
                ctx.stroke();
                ctx.setLineDash([]);

                // 장애물(다른 차량) 그리기
                for (let obs of obstacles) {
                    ctx.fillStyle = "#aa0000";
                    ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
                    // 차량 헤드라이트
                    ctx.fillStyle = "#fffa00";
                    ctx.fillRect(obs.x + 5, obs.y, 8, 4);
                    ctx.fillRect(obs.x + obs.width - 13, obs.y, 8, 4);
                }

                // 플레이어 자동차 렌더링 (디테일 강화)
                let spec = cars[currentCarKey];
                ctx.fillStyle = spec.color;
                ctx.fillRect(car.x, car.y, car.width, car.height);

                // 리어 윙 (스포일러)
                ctx.fillStyle = "#111";
                ctx.fillRect(car.x - 4, car.y + car.height - 15, car.width + 8, 8);

                // 헤드라이트 및 테일램프
                ctx.fillStyle = keys["Space"] ? "#00ffff" : "#ffffff";
                ctx.fillRect(car.x + 4, car.y, 10, 5);
                ctx.fillRect(car.x + car.width - 14, car.y, 10, 5);

                // UI 업데이트
                document.getElementById("speedDisplay").innerText = Math.floor(car.speed * 15);
                document.getElementById("scoreDisplay").innerText = score;
                document.getElementById("nitroDisplay").innerText = Math.floor(car.nitro);

                if (isGameOver) {
                    ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = "#ff3300";
                    ctx.font = "bold 40px sans-serif";
                    ctx.textAlign = "center";
                    ctx.fillText("CRASHED! GAME OVER", canvas.width / 2, canvas.height / 2 - 20);
                    ctx.fillStyle = "#ffffff";
                    ctx.font = "20px sans-serif";
                    ctx.fillText("새로고침(F5)을 눌러 다시 시작하세요", canvas.width / 2, canvas.height / 2 + 30);
                }
            }

            function loop() {
                update();
                draw();
                if (!isGameOver) {
                    requestAnimationFrame(loop);
                }
            }

            loop();
        </script>
    </body>
    </html>
    """

  # 스트림릿 내에 HTML 컴포넌트 삽입
  st.components.v1.html(game_html, height=750, scrolling=True)


if __name__ == "__main__":
  run_code()
