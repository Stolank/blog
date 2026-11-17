const menu = document.querySelector(".menu-toggle");
if (menu) {
    menu.setAttribute("aria-expanded", "false");
    menu.hidden = false;
    menu.addEventListener("click", () => {
        const open = menu.getAttribute("aria-expanded") === "true";
        menu.setAttribute("aria-expanded", String(!open));
    });
    document.getElementById("site-navigation").addEventListener("keydown", (event) => {
        if (event.key === "Escape" && window.getComputedStyle(menu).display !== "none") {
            menu.setAttribute("aria-expanded", "false");
            menu.focus();
        }
    });
}
