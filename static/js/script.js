window.addEventListener('DOMContentLoaded', () => {
	// bars
	const bars = document.querySelector('.bars'),
		navListItems = document.querySelector('.navListItems'),
		itemDrop = document.querySelectorAll('.itemDrop'),
		listItem = navListItems.querySelectorAll('.listItem'),
		listDrop = navListItems.querySelectorAll('.listDrop')

	bars.addEventListener('click', () => {
		if (navListItems.classList.contains('active')) {
			navListItems.classList.remove('active', 'acLeft')
		} else {
			navListItems.classList.add('active', 'acLeft')
		}
	})

	itemDrop.forEach(item => {
		item.addEventListener('click', () => {
			// itemDrop.forEach(i => i.classList.remove('dropActiv'))
			if (item.classList.contains('dropActiv')) {
				item.classList.remove('dropActiv')
			} else {
				item.classList.add('dropActiv')
			}
		})
	})

	bars.addEventListener('click', () => {
		console.log(listItem)
		listItem.forEach(item => {
			item.addEventListener('click', () => {
				if (item.classList.contains('itemDrop')) {
					listDrop.forEach(i => {
						i.addEventListener('click', () => {
							navListItems.classList.remove('active', 'acLeft')
						})
					})
				} else {
					navListItems.classList.remove('active', 'acLeft')
				}
			})
		})
	})

	// nav-listItem
	const itemA = document.querySelectorAll('.itemA')

	itemA.forEach(item => {
		item.addEventListener('click', () => {
			itemA.forEach(i => i.classList.remove('bag'))
			item.classList.add('bag')
		})
	})

	// count js
	const counters = document.querySelectorAll('.count')
	let animated = false

	const animateCounters = () => {
		counters.forEach(counter => {
			const updateCount = () => {
				const target = +counter.getAttribute('data-target')
				const count = +counter.innerText
				const increment = Math.max(1, Math.ceil(target / 100))

				if (count < target) {
					counter.innerText = count + increment
					setTimeout(updateCount, 20)
				} else {
					counter.innerText = target
				}
			}
			updateCount()
		})
	}

	const observer = new IntersectionObserver(
		(entries, observer) => {
			entries.forEach(entry => {
				if (entry.isIntersecting && !animated) {
					animated = true
					animateCounters()
					observer.disconnect()
				}
			})
		},
		{
			threshold: 0.5,
		}
	)

	const section = document.querySelector('.sectionCount')
	if (section) {
		observer.observe(section)
	}

	// const counts = document.querySelectorAll('.count')
	// const speed = 25
	// counts.forEach(counter => {
	// 	function upDate() {
	// 		const target = Number(counter.getAttribute('data-target'))
	// 		const count = Number(counter.innerHTML)
	// 		const inc = target / speed
	// 		if (count < target) {
	// 			counter.innerHTML = Math.floor(inc + count)
	// 			setTimeout(upDate, 80)
	// 		} else {
	// 			counter.innerText = target
	// 		}
	// 	}
	// 	upDate()
	// })

	// Accardion about section
	const accardion = document.querySelectorAll('.accardion')

	accardion.forEach(i => {
		const acc = i.nextElementSibling
		const acc1 = i.lastElementChild
		accardion.forEach(item => {
			item.addEventListener('click', () => {
				const panel = item.nextElementSibling
				const plusMinus = item.lastElementChild
				if (i == item) {
					if (panel.classList.contains('aboutNone')) {
						panel.classList.add('aboutBlock')
						panel.classList.remove('aboutNone')
						plusMinus.classList.add('fa-minus')
						plusMinus.classList.remove('fa-plus')
					} else {
						panel.classList.remove('aboutBlock')
						panel.classList.add('aboutNone')
						plusMinus.classList.remove('fa-minus')
						plusMinus.classList.add('fa-plus')
					}
				} else {
					acc.classList.remove('aboutBlock')
					acc.classList.add('aboutNone')
					acc1.classList.remove('fa-minus')
					acc1.classList.add('fa-plus')
				}
			})
		})
	})

	// Login-in and sign-up
	const userBtnExit = document.querySelector('.userBtnExit')
	const exit = document.querySelector('.exit')

	if (userBtnExit && exit) {
		// Tugma bosilganda chiqish panelini ko‘rsatish/yashirish
		userBtnExit.addEventListener('click', event => {
			event.stopPropagation() // Bu event window ga yetib bormasin
			exit.classList.toggle('bnone')
		})

		// Window bosilganda panelni yashirish
		window.addEventListener('click', () => {
			if (!exit.classList.contains('bnone')) {
				exit.classList.add('bnone')
			}
		})

		// Panelning o‘ziga bosilganda windowga ketmasligi uchun
		exit.addEventListener('click', event => {
			event.stopPropagation()
		})
	}
})
