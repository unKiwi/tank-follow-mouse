let tankX = 0;
let speed = 1
let fps = 144

let draw = () => {
    tankX += speed / fps
}

setInterval(draw, 1000 / fps);
setInterval(() => {
    console.log(tankX);
}, 1000);