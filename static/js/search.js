var customDropdown = document.getElementById("customDropdown");
var dropdownContent = document.getElementById("dropdownContent");

customDropdown.addEventListener("click", function (event) {
    // 切換下拉選單的顯示和隱藏狀態
    dropdownContent.classList.toggle("active");

    // 防止事件冒泡，避免點擊下拉選單內容時觸發文檔點擊事件
    event.stopPropagation();
});

// 添加單獨的點擊事件，以防止下拉選單內容的點擊事件影響文檔點擊事件
dropdownContent.addEventListener("click", function (event) {
    event.stopPropagation();
});

function closeDropdown() {
    // 關閉下拉選單
    dropdownContent.classList.remove("active");
}

function performSearch() {
    // 在這裡添加執行搜索的邏輯
    // ...
    // 關閉下拉選單
    closeDropdown();
}

// 點擊文檔時隱藏下拉選單
document.addEventListener("click", function () {
    closeDropdown();
});

