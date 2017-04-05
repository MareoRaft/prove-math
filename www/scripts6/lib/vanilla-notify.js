// THE LICENSE BELOW APPLIES TO THIS FILE ONLY
// see http://www.cssscript.com/native-javascript-growl-notification-library-vanilla-notify/
// The MIT License (MIT)

// Copyright (c) 2014 Martin Laritz

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

define([], function() {

let positionOption = {
	topLeft: 'topLeft',
	topCenter: 'topCenter',
	topRight: 'topRight',
	bottomLeft: 'bottomLeft',
	bottomRight: 'bottomRight',
	center: 'center',
}

let options = { // DEFAULTS
	fadeInDuration: 1000,
	fadeOutDuration: 1000,
	fadeInterval: 50,
	visibleDuration: 'forever',
	postHoverVisibleDuration: 'forever',
	position: 'topCenter',
	sticky: false,
	showClose: true,
}

let info = function(params) {
	params.notifyClass = 'vnotify-info'
	return addNotify(params)
}

let success = function(params) {
	params.notifyClass = 'vnotify-success'
	return addNotify(params)
}

let error = function(params) {
	params.notifyClass = 'vnotify-error'
	return addNotify(params)
}

let warning = function(params) {
	params.notifyClass = 'vnotify-warning'
	return addNotify(params)
}

let notify = function(params) {
	params.notifyClass = 'vnotify-notify'
	return addNotify(params)
}

let custom = function(params) {
	return addNotify(params)
}

let addNotify = function(params) {
	if (!params.title && !params.text) {
		return null
	}

	let frag = document.createDocumentFragment()

	let item = document.createElement('div')
	item.classList.add('vnotify-item')
	item.classList.add(params.notifyClass)
	item.style.opacity = 0

	item.options = getOptions(params)

	if (params.title) {
		item.appendChild(addTitle(params.title))
	}
	if (params.text) {
		item.appendChild(addText(params.text))
	}
	if (item.options.showClose) {
		item.appendChild(addClose(item))
	}

	item.visibleDuration = item.options.visibleDuration //option

	let hideNotify = function() {
		item.fadeInterval = fade('out', item.options.fadeOutDuration, item)
	}

	let resetInterval = function() {
		clearTimeout(item.interval)
		clearTimeout(item.fadeInterval)
		item.style.opacity = null
		item.visibleDuration = item.options.postHoverVisibleDuration
	}

	let hideTimeout = function () {
		if( item.visibleDuration === 'forever' ){
			// pass
		} else {
			item.interval = setTimeout(hideNotify, item.visibleDuration)
		}
	}

	frag.appendChild(item)
	let container = getNotifyContainer(item.options.position)
	container.appendChild(frag)

	item.addEventListener("mouseover", resetInterval)

	fade('in', item.options.fadeInDuration, item)

	if (!item.options.sticky){
		item.addEventListener("mouseout", hideTimeout)
		hideTimeout()
	}

	return item
}

let addText = function(text) {
	let item = document.createElement('div')
	item.classList.add('vnotify-text')
	item.innerHTML = text
	return item
}

let addTitle = function(title) {
	let item = document.createElement('div')
	item.classList.add('vnotify-title')
	item.innerHTML = title
	return item
}

let addClose = function(parent) {
	let item = document.createElement('span')
	item.classList.add('vn-close')
	item.addEventListener('click', function(){remove(parent)})
	return item
}

let getNotifyContainer = function(position) {
	let positionClass = getPositionClass(position)
	let container = document.querySelector('.' + positionClass)
	return container ? container : createNotifyContainer(positionClass)
}

let createNotifyContainer = function(positionClass) {
	let frag = document.createDocumentFragment()
	let container = document.createElement('div')
	container.classList.add('vnotify-container')
	container.classList.add(positionClass)
	container.setAttribute('role', 'alert')

	frag.appendChild(container)
	document.getElementById('notify-overlay').appendChild(frag) // changed by matt

	return container
}

let getPositionClass = function(option) {
	switch (option) {
		case positionOption.topLeft:
			return 'vn-top-left'
		case positionOption.topCenter:
			return 'vn-top-center'
		case positionOption.bottomRight:
			return 'vn-bottom-right'
		case positionOption.bottomLeft:
			return 'vn-bottom-left'
		case positionOption.center:
			return 'vn-center'
		default:
			return 'vn-top-right'
	}
}

let getOptions = function(opts) {
	return {
		fadeInDuration: opts.fadeInDuration || options.fadeInDuration,
		fadeOutDuration: opts.fadeOutDuration || options.fadeOutDuration,
		fadeInterval: opts.fadeInterval || options.fadeInterval,
		visibleDuration: opts.visibleDuration || options.visibleDuration,
		postHoverVisibleDuration: opts.postHoverVisibleDuration || options.postHoverVisibleDuration,
		position: opts.position || options.position,
		sticky: opts.sticky != null ? opts.sticky : options.sticky,
		showClose: opts.showClose != null ? opts.showClose : options.showClose,
	}
}

let remove = function(item) {
	item.style.display = 'none'
	item.outerHTML = ''
	item = null
}

//New fade - based on http://toddmotto.com/raw-javascript-jquery-style-fadein-fadeout-functions-hugo-giraudel/
let fade = function(type, ms, el) {
	let isIn = type === 'in',
		opacity = isIn ? 0 : el.style.opacity || 1,
		goal = isIn ? 0.8 : 0,
		gap = options.fadeInterval / ms

	if(isIn) {
		el.style.display = 'block'
		el.style.opacity = opacity
	}

	function func() {
		opacity = isIn ? opacity + gap : opacity - gap
		el.style.opacity = opacity

		if(opacity <= 0) {
			remove(el)
			checkRemoveContainer()
		}
		if((!isIn && opacity <= goal) || (isIn && opacity >= goal)) {
			window.clearInterval(fading)
		}
	}

	let fading = window.setInterval(func, options.fadeInterval)
	return fading
}

let checkRemoveContainer = function() {
	let item = document.querySelector('.vnotify-item')
	if (!item) {
		let container = document.querySelectorAll('.vnotify-container')
		for (let i=0 i< container.length i++) {
			container[i].outerHTML = ''
			container[i] = null
		}
	}
}

return {
	info: info,
	success: success,
	error: error,
	warning: warning,
	notify: notify,
	custom: custom,
	options: options,
	positionOption: positionOption,
}

}) // end define
