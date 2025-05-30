const options = {
    root: null,
    rootMargin: "0px 0px 0px 0px",
    // Відсоток від розміру об'єкту.
    // При появі якого спрацьовує подія
    // Де 0 це будь яка поява
    // 1 це повна поява об'кта в в'юпорті
    threshold: 0.2,
}
const callback = (entries, observer) => {
    entries.forEach(entry => {
        const currentElement = entry.target
        if (entry.isIntersecting) {
            currentElement.classList.add('--animate')
            //console.log('я тебе бачу')
            observer.unobserve(currentElement); // 💡 отключаем наблюдение после первого появления

        }
    })
}
const observer = new IntersectionObserver(callback, options)

const animElements = document.querySelectorAll('[class*="--anim"]')
animElements.forEach(animElement => {
    observer.observe(animElement)
})