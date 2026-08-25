import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌깨기")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {
        margin: 0;
        padding: 0;
        background: #111;
        overflow: hidden;
        font-family: Arial, sans-serif;
    }

    #game {
        display: block;
        margin: auto;
        background: #181818;
        border: 3px solid white;
        max-width: 100%;
    }

    #info {
        color: white;
        text-align: center;
        font-size: 18px;
        padding: 8px;
    }

    button {
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        border: none;
        border-radius: 8px;
    }
</style>
</head>

<body>

<div id="info">
    점수: <span id="score">0</span>
    &nbsp;&nbsp;
    목숨: <span id="lives">3</span>
</div>

<canvas id="game" width="700" height="500"></canvas>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let score = 0;
let lives = 3;

let ball = {
    x: canvas.width / 2,
    y: canvas.height - 60,
    dx: 4,
    dy: -4,
    radius: 8
};

let paddle = {
    width: 110,
    height: 15,
    x: canvas.width / 2 - 55,
    y: canvas.height - 35,
    speed: 8
};

let rightPressed = false;
let leftPressed = false;

const brickRowCount = 6;
const brickColumnCount = 9;

const brickWidth = 65;
const brickHeight = 22;
const brickPadding = 10;
const brickOffsetTop = 45;
const brickOffsetLeft = 22;

let bricks = [];

function createBricks() {
    bricks = [];

    for (let c = 0; c < brickColumnCount; c++) {
        bricks[c] = [];

        for (let r = 0; r < brickRowCount; r++) {
            bricks[c][r] = {
                x: 0,
                y: 0,
                status: 1
            };
        }
    }
}

createBricks();

document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);

function keyDownHandler(e) {

    if (e.key === "ArrowRight") {
        rightPressed = true;
    }

    if (e.key === "ArrowLeft") {
        leftPressed = true;
    }
}

function keyUpHandler(e) {

    if (e.key === "ArrowRight") {
        rightPressed = false;
    }

    if (e.key === "ArrowLeft") {
        leftPressed = false;
    }
}

// 마우스 조작
canvas.addEventListener("mousemove", function(e) {

    const rect = canvas.getBoundingClientRect();

    const mouseX =
        e.clientX - rect.left;

    paddle.x =
        mouseX * canvas.width / rect.width
        - paddle.width / 2;

    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (paddle.x > canvas.width - paddle.width) {
        paddle.x = canvas.width - paddle.width;
    }
});

// 모바일 터치 조작
canvas.addEventListener("touchmove", function(e) {

    e.preventDefault();

    const rect = canvas.getBoundingClientRect();

    const touchX =
        e.touches[0].clientX - rect.left;

    paddle.x =
        touchX * canvas.width / rect.width
        - paddle.width / 2;

    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (paddle.x > canvas.width - paddle.width) {
        paddle.x = canvas.width - paddle.width;
    }

}, {passive:false});


function drawBall() {

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "white";
    ctx.fill();

    ctx.closePath();
}


function drawPaddle() {

    ctx.beginPath();

    ctx.roundRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height,
        6
    );

    ctx.fillStyle = "#00d4ff";
    ctx.fill();

    ctx.closePath();
}


function drawBricks() {

    for (let c = 0; c < brickColumnCount; c++) {

        for (let r = 0; r < brickRowCount; r++) {

            if (bricks[c][r].status === 1) {

                const brickX =
                    c * (brickWidth + brickPadding)
                    + brickOffsetLeft;

                const brickY =
                    r * (brickHeight + brickPadding)
                    + brickOffsetTop;

                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;

                ctx.beginPath();

                ctx.roundRect(
                    brickX,
                    brickY,
                    brickWidth,
                    brickHeight,
                    5
                );

                ctx.fillStyle =
                    `hsl(${r * 45 + c * 8}, 80%, 55%)`;

                ctx.fill();

                ctx.closePath();
            }
        }
    }
}


function collisionDetection() {

    let remaining = 0;

    for (let c = 0; c < brickColumnCount; c++) {

        for (let r = 0; r < brickRowCount; r++) {

            let b = bricks[c][r];

            if (b.status === 1) {

                remaining++;

                if (
                    ball.x > b.x &&
                    ball.x < b.x + brickWidth &&
                    ball.y > b.y &&
                    ball.y < b.y + brickHeight
                ) {

                    ball.dy = -ball.dy;

                    b.status = 0;

                    score++;

                    document.getElementById(
                        "score"
                    ).textContent = score;
                }
            }
        }
    }

    if (remaining === 0) {

        alert(
            "🎉 게임 클리어!\\n점수: "
            + score
        );

        location.reload();
    }
}


function resetBall() {

    ball.x = canvas.width / 2;
    ball.y = canvas.height - 60;

    ball.dx =
        Math.random() > 0.5 ? 4 : -4;

    ball.dy = -4;

    paddle.x =
        canvas.width / 2
        - paddle.width / 2;
}


function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawBricks();
    drawBall();
    drawPaddle();

    collisionDetection();

    // 벽 충돌
    if (
        ball.x + ball.dx >
        canvas.width - ball.radius ||

        ball.x + ball.dx <
        ball.radius
    ) {

        ball.dx = -ball.dx;
    }

    if (
        ball.y + ball.dy <
        ball.radius
    ) {

        ball.dy = -ball.dy;
    }

    // 패들 충돌
    if (
        ball.y + ball.dy >
        paddle.y - ball.radius &&

        ball.x >
        paddle.x &&

        ball.x <
        paddle.x + paddle.width
    ) {

        ball.dy = -Math.abs(ball.dy);

        // 패들의 맞은 위치에 따라 방향 변화
        let hit =
            (ball.x -
            (paddle.x + paddle.width / 2))
            / (paddle.width / 2);

        ball.dx = hit * 6;
    }

    // 바닥
    if (
        ball.y + ball.dy >
        canvas.height - ball.radius
    ) {

        lives--;

        document.getElementById(
            "lives"
        ).textContent = lives;

        if (lives <= 0) {

            alert(
                "게임 오버!\\n점수: "
                + score
            );

            location.reload();

        } else {

            resetBall();
        }
    }

    // 키보드 이동
    if (rightPressed) {

        paddle.x += paddle.speed;

    } else if (leftPressed) {

        paddle.x -= paddle.speed;
    }

    // 패들 화면 밖 방지
    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (
        paddle.x >
        canvas.width - paddle.width
    ) {

        paddle.x =
            canvas.width - paddle.width;
    }

    ball.x += ball.dx;
    ball.y += ball.dy;

    requestAnimationFrame(draw);
}

draw();

</script>

</body>
</html>
"""

components.html(
    html_code,
    height=570,
    scrolling=False
)
