// Landing page enhancements: rotating hero word + animated stat counters.
document.addEventListener("DOMContentLoaded", function () {

    // Rotating word in hero heading
    const words = ["ID card", "wallet", "charger", "earphones", "keys", "water bottle"];
    const rotatingEl = document.getElementById("rotatingWord");
    if (rotatingEl) {
        let i = 0;
        setInterval(function () {
            i = (i + 1) % words.length;
            rotatingEl.style.opacity = 0;
            setTimeout(function () {
                rotatingEl.textContent = words[i];
                rotatingEl.style.opacity = 1;
            }, 250);
        }, 2200);
    }

    // Animated count-up for stat numbers
    const counters = document.querySelectorAll(".counter");
    counters.forEach(function (counter) {
        const target = parseInt(counter.getAttribute("data-target"), 10) || 0;
        const duration = 900;
        const start = performance.now();

        function tick(now) {
            const progress = Math.min((now - start) / duration, 1);
            counter.textContent = Math.floor(progress * target);
            if (progress < 1) {
                requestAnimationFrame(tick);
            } else {
                counter.textContent = target;
            }
        }
        requestAnimationFrame(tick);
    });
});