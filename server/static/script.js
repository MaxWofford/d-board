'use strict'

const URL = window.location.origin
const dashboard = document.querySelector('.dashboard-container')
let updatedAt = 0

let newTextBoard = board => {
  let el = document.createElement('p')
  el.appendChild(document.createTextNode(board.content))
  return el
}

let newImageBoard = board => {
  let el = document.createElement('img')
  el.src = board.content
  return el
}

let createBoard = board => {
  let el
  if (board.type == 'text') {
    el = newTextBoard(board)
  } else if (board.type == 'image-url') {
    el = newImageBoard(board)
  }
  el.className += board.size
  dashboard.appendChild(el)
}

let updateView = () => {
  fetch(`${URL}/dashboard.json`).then(res => {
    if (!res.ok) {
      console.log('Network response was not ok.')
    } else {
      return res.json()
    }
  }).then(processJSON)
}

let processJSON = data => {
  let timestamps = data.boards.map(board => {
    return board.timestamp
  })
  let mostRecentTimestamp = Math.max.apply(null, timestamps)
  if (mostRecentTimestamp > updatedAt) {
    dashboard.innerHTML = ''
    data.boards.map(createBoard)
    data.boards.map(board => {console.log(board)})
    updatedAt = mostRecentTimestamp
  }
}

// Update the view every 5 seconds
updateView()
setTimeout(updateView, 5000)
