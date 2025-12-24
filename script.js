let paging = Array(16).fill(0);
let segment = Array(16).fill(0);
let pid = 1;
let auto = false;
let timer = null;

function draw() {
  const p = document.getElementById("paging");
  const s = document.getElementById("segment");
  p.innerHTML = "";
  s.innerHTML = "";

  let used = 0;

  paging.forEach(v => {
    const d = document.createElement("div");
    d.className = "block " + (v ? "p" + v : "");
    d.textContent = v ? "P" + v : "Free";
    if (v) used++;
    p.appendChild(d);
  });

  segment.forEach(v => {
    const d = document.createElement("div");
    d.className = "block " + (v ? "p" + v : "");
    d.textContent = v ? "P" + v : "Free";
    s.appendChild(d);
  });

  document.getElementById("used").textContent = used;
  document.getElementById("free").textContent = 16 - used;
}

function allocate() {
  let need = 2 + Math.floor(Math.random() * 3);
  let done = 0;

  for (let i = 0; i < paging.length && done < need; i++) {
    if (paging[i] === 0) {
      paging[i] = pid;
      done++;
    }
  }

  done = 0;
  for (let i = 0; i < segment.length && done < need; i++) {
    if (segment[i] === 0) {
      segment[i] = pid;
      done++;
    }
  }

  pid = pid % 4 + 1;
  draw();
}

function freeProcess() {
  let target = Math.floor(Math.random() * 4) + 1;
  paging = paging.map(v => v === target ? 0 : v);
  segment = segment.map(v => v === target ? 0 : v);
  draw();
}

function toggleAuto() {
  auto = !auto;
  if (auto) {
    timer = setInterval(() => {
      Math.random() > 0.5 ? allocate() : freeProcess();
    }, 900);
  } else {
    clearInterval(timer);
  }
}

draw();
