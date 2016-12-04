'use strict';

const URL = window.location.origin;
const dashboard = document.querySelector('.dashboard-container');
let updatedAt = 0;

let newTextBoard = board => {
    let el = document.createElement('p');
    el.appendChild(document.createTextNode(board.content));
    return el;
};

let newImageBoard = board => {
    let el = document.createElement('img');
    el.src = board.content;
    return el;
};

let createBoard = board => {
    let el;
  if (board.type == 'text') {
      el = newTextBoard(board);
  } else if (board.type == 'image-url') {
      el = newImageBoard(board);
  }
    el.className += board.size;
    let style = `top: ${board.location.y}%;`;
    style += `left: ${board.location.x}%;`;
    el.setAttribute('style', style);
    dashboard.appendChild(el);
};

let updateView = () => {
  fetch(`${URL}/dashboard.json`).then(res => {
    if (!res.ok) {
        console.log('Network response was not ok.');
        return null;
    } else {
        return res.json();
    }
  }).then(processJSON);
};

let processJSON = data => {
  if (data && data.boards) {
    let timestamps = data.boards.map(board => {
        return board.timestamp;
    });
    let mostRecentTimestamp = Math.max.apply(null, timestamps);
    if (mostRecentTimestamp > updatedAt) {
        dashboard.innerHTML = '';
        data.boards.map(createBoard);
        data.boards.map(board => {console.log(board);});
        updatedAt = mostRecentTimestamp;
    }
  }
};

// form logic
let clickHandler = event => {
    let input = document.querySelector('#post-input');
    input.select();
    let inputContainer = document.querySelector('#input-container');
    inputContainer.className = '';
    inputContainer.setAttribute('style', `left: ${event.clientX}px; top: ${event.clientY}px;`);
};

let submit = size => {
    let type = 'text';
    let input = document.querySelector('#post-input');
    if(/^(?:(?:(?:https?|ftp):)?\/\/).*/i.test(input.value)) {
        type="photo";
    }
    let pos_x = parseInt(input.getBoundingClientRect().left/window.innerWidth*100);
    let pos_y = parseInt(input.getBoundingClientRect().top/window.innerHeight*100);
    let params = {
        size: size,
        content: input.value,
        pos_x: parseInt(pos_x),
        pos_y: parseInt(pos_y),
        pos_z: 0
    };
    fetch(`${URL}/post/${type}`, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(params)
    }).then(res => {
        document.querySelector('#input-container').className= 'hidden';
        updateView();
    });
};
