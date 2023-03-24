// анимации через IO
function element_visible(entry) {
    entry.forEach(change => {
        if (change.isIntersecting) {
            change.target.classList.add('element-shown');            
        };
    });
};

let options = {threshold: [0.15]};
let observer = new IntersectionObserver(element_visible, options);
let elements = $(".fade-up, .fade-down, .fade-right, .fade-left, .scale");

for (let elm of elements) {
    observer.observe(elm);
};