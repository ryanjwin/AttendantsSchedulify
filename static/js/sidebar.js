window.onload = function() {

    const checkbox = document.querySelector("#openSidebarMenu");
    const sidebar = document.querySelector("#sidebarMenu");

    checkbox.addEventListener("change", () => {
    if (checkbox.checked) {
        sidebar.style.transform = "translateX(0)";
    } else {
        sidebar.style.transform = "translateX(-250px)";
    }
    });

}