document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector("[data-nav-toggle]");
    const links = document.querySelector("[data-nav-links]");
    if (toggle && links) {
        toggle.addEventListener("click", () => {
            const open = links.classList.toggle("is-open");
            toggle.setAttribute("aria-expanded", String(open));
        });
    }

    const slider = document.querySelector("[data-split-slider]");
    const details = document.querySelector("[data-problem-details]");
    const editor = document.querySelector("[data-problem-editor]");
    if (!slider || !details || !editor) return;

    let dragging = false;
    const setSplit = (clientX) => {
        const layout = slider.parentElement.getBoundingClientRect();
        const percentage = Math.min(90, Math.max(10, ((clientX - layout.left) / layout.width) * 100));
        details.style.flexBasis = `${percentage}%`;
        editor.style.flexBasis = `${100 - percentage}%`;
    };

    slider.addEventListener("pointerdown", (event) => {
        dragging = true;
        slider.setPointerCapture(event.pointerId);
        event.preventDefault();
    });
    slider.addEventListener("pointermove", (event) => {
        if (dragging) setSplit(event.clientX);
    });
    slider.addEventListener("pointerup", () => { dragging = false; });
    slider.addEventListener("pointercancel", () => { dragging = false; });
});
