document.addEventListener("DOMContentLoaded", function () {
    const newBooksContainer = document.getElementById("newBooksContainer");
    const recommendBooksContainer = document.getElementById("recommendBooksContainer")

    const scrollToNewBooksButton = document.getElementById("scrollToNewBooksButton");
    const scrollToRecommendBooksButton = document.getElementById("scrollToRecommendBooksButton");

    const prevButton = document.getElementById("prevButton");
    const nextButton = document.getElementById("nextButton");

    // 切換到上一頁
    prevButton.addEventListener("click", function () {
        if (currentPage > 1) {
            currentPage--;
            updateBooks();
        }
    });

    // 切換到下一頁
    nextButton.addEventListener("click", function () {
        const totalPages = Math.ceil(booksData.length / booksPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            updateBooks();
        }
    });

});

function createBookElement(book) {
    const BookElement = document.createElement("div");
    BookElement.classList.add("book");

    const imageElement = document.createElement("img");
    imageElement.src = book.image;
    imageElement.alt = book.title;

    const titleLinkElement = document.createElement("a");
    titleLinkElement.href = "{{url_for('getDetailProductInfo',id=book.id)}}";
    titleLinkElement.textContent = book.title;

    const authorElement = document.createElement("p");
    authorElement.textContent = `作者: ${book.author}`;

    const priceElement = document.createElement("p");
    priceElement.textContent = `價格: ${book.price}`;

    BookElement.appendChild(imageElement);
    BookElement.appendChild(titleLinkElement);
    BookElement.appendChild(authorElement);
    BookElement.appendChild(priceElement);

    return BookElement;
}
