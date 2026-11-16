const products = [
    { id: "mug", name: "Кружка «Мох»", category: "ceramics", price: 4900, image: "mug.jpg", description: "Керамическая кружка с глянцевой оливковой глазурью и широкой ручкой.", variants: [{ name: "280 мл", stock: 4 }, { name: "360 мл", stock: 2 }] },
    { id: "notebook", name: "Блокнот «Лён»", category: "paper", price: 6200, image: "notebook.jpg", description: "Блокнот в льняном переплёте для заметок и набросков. Бумага цвета слоновой кости.", variants: [{ name: "А5 · без линовки", stock: 5 }, { name: "А5 · точка", stock: 3 }] },
    { id: "lamp", name: "Лампа «Арка»", category: "light", price: 24900, image: "lamp.jpg", description: "Настольная лампа с округлым плафоном и тёплым направленным светом.", variants: [{ name: "Оливковая", stock: 0 }] },
];
const categories = { all: "Все товары", ceramics: "Керамика", paper: "Бумага", light: "Свет" };
const money = new Intl.NumberFormat("ru-KZ", { style: "currency", currency: "KZT", maximumFractionDigits: 0 });
const main = document.querySelector("#main");
const notice = document.querySelector("#notice");
const storageKey = "oldschool-storefront-cart";
let cart = readCart();
let completedOrder = null;
let noticeTimeout;

function readCart() {
    try {
        const stored = JSON.parse(sessionStorage.getItem(storageKey) || "{}");
        return Object.fromEntries(products.flatMap(product => product.variants.map((variant, index) => {
            const key = `${product.id}-${index}`;
            const quantity = stored?.[key];
            return [key, Number.isInteger(quantity) ? Math.max(0, Math.min(quantity, variant.stock)) : 0];
        })));
    } catch {
        return {};
    }
}

function saveCart() {
    try {
        sessionStorage.setItem(storageKey, JSON.stringify(cart));
    } catch {
        // The prototype also runs when browser storage is unavailable.
    }
    document.querySelector("#cart-count").textContent = Object.values(cart).reduce((sum, count) => sum + count, 0);
}

function showNotice(message) {
    notice.textContent = message;
    clearTimeout(noticeTimeout);
    noticeTimeout = setTimeout(() => { notice.textContent = ""; }, 3200);
}

function items() {
    return products.flatMap(product => product.variants.flatMap((variant, index) => {
        const key = `${product.id}-${index}`;
        const quantity = cart[key];
        return quantity ? [{ product, variant, key, quantity }] : [];
    }));
}

function subtotal(lines) {
    return lines.reduce((sum, item) => sum + item.quantity * item.product.price, 0);
}

function productCards(list) {
    return `<div class="cards">${list.map(product => `
        <a class="card-link" href="#product/${product.id}">
            <img src="assets/${product.image}" alt="" width="600" height="600" loading="lazy">
            <div class="card-meta">
                <p class="label">${categories[product.category]}</p>
                <h3>${product.name}</h3>
                <p class="price">${money.format(product.price)}</p>
                ${product.variants.every(variant => !variant.stock) ? '<p class="label">Нет в наличии</p>' : ""}
            </div>
        </a>`).join("")}</div>`;
}

function homePage() {
    return `<section class="hero">
        <div class="hero-copy">
            <h1>Предметы для рабочего стола</h1>
            <p>Керамика, бумага и свет для чтения, заметок и работы.</p>
            <a class="button" href="#catalog">Смотреть каталог</a>
        </div>
        <img src="assets/hero.jpg" alt="Оливковая кружка, льняной блокнот и лампа в солнечном свете" width="1536" height="1024">
    </section>
    <section class="section" aria-labelledby="collection-title">
        <div class="section-head"><h2 id="collection-title">Коллекция</h2><a href="#catalog">Весь каталог</a></div>
        ${productCards(products)}
    </section>`;
}

function catalogPage(category) {
    const selected = Object.hasOwn(categories, category || "") ? category : "all";
    const list = selected === "all" ? products : products.filter(product => product.category === selected);
    return `<h1>Каталог</h1>
        <nav class="filters" aria-label="Категории товаров">${Object.entries(categories).map(([key, label]) => `
            <a href="#catalog/${key}"${key === selected ? ' aria-current="page"' : ""}>${label}</a>`).join("")}</nav>
        ${productCards(list)}`;
}

function productPage(product) {
    const available = product.variants.some(variant => variant.stock);
    return `<a class="trail" href="#catalog">Каталог</a>
        <article class="product">
            <img src="assets/${product.image}" alt="${product.name}" width="600" height="600">
            <div class="product-content">
                <p class="label">${categories[product.category]}</p>
                <h1>${product.name}</h1>
                <p class="price">${money.format(product.price)}</p>
                <p>${product.description}</p>
                <p class="availability" id="availability" role="status">${available ? "В наличии" : "Нет в наличии"}</p>
                <form id="add-product" data-product="${product.id}">
                    ${product.variants.length > 1 ? `<label>Вариант<select name="variant">${product.variants.map((variant, index) => `<option value="${index}">${variant.name}</option>`).join("")}</select></label>` : `<input type="hidden" name="variant" value="0"><p>${product.variants[0].name}</p>`}
                    <button class="button" type="submit" ${available ? "" : "disabled"}>В корзину</button>
                    <a href="#cart">Перейти в корзину</a>
                </form>
            </div>
        </article>`;
}

function emptyCart() {
    return '<div class="empty"><p>Корзина пуста.</p><a class="button" href="#catalog">Перейти в каталог</a></div>';
}

function totals(lines, delivery) {
    const amount = subtotal(lines);
    return `<dl>
        <div><dt>Товары</dt><dd>${money.format(amount)}</dd></div>
        <div><dt>Доставка</dt><dd>${delivery === null ? "При оформлении" : money.format(delivery)}</dd></div>
        <div class="total"><dt>${delivery === null ? "Всего без доставки" : "К оплате"}</dt><dd>${money.format(amount + (delivery || 0))}</dd></div>
    </dl>`;
}

function cartPage(lines) {
    if (!lines.length) return `<h1>Корзина</h1>${emptyCart()}`;
    return `<h1>Корзина</h1><div class="split">
        <section aria-label="Товары в корзине">${lines.map(({ product, variant, key, quantity }) => `
            <article class="cart-row" data-key="${key}">
                <img src="assets/${product.image}" alt="" width="80" height="80">
                <div>
                    <h3><a href="#product/${product.id}">${product.name}</a></h3>
                    <p>${variant.name} · <strong>${money.format(quantity * product.price)}</strong></p>
                    <div class="quantity">
                        <button type="button" data-action="less" aria-label="Уменьшить количество: ${product.name}, ${variant.name}" ${quantity === 1 ? "disabled" : ""}>−</button>
                        <span aria-label="Количество">${quantity}</span>
                        <button type="button" data-action="more" aria-label="Увеличить количество: ${product.name}, ${variant.name}" ${quantity === variant.stock ? "disabled" : ""}>+</button>
                        <button type="button" class="remove" data-action="remove" aria-label="Удалить ${product.name}, ${variant.name}">Удалить</button>
                    </div>
                </div>
            </article>`).join("")}
        </section>
        <aside class="summary" aria-label="Итог заказа">${totals(lines, null)}<a class="button" href="#checkout">Оформить заказ</a></aside>
    </div>`;
}

const deliveryMethods = { pickup: { label: "Самовывоз", price: 0 }, courier: { label: "Курьер", price: 1500 } };

function checkoutPage(lines) {
    if (!lines.length) return `<h1>Оформление заказа</h1>${emptyCart()}`;
    return `<a class="trail" href="#cart">Назад в корзину</a><h1>Оформление заказа</h1>
        <div class="split">
            <form id="checkout" class="checkout-form">
                <p class="label">Демонстрация оформления. Используйте вымышленные данные.</p>
                <label>Имя<input name="customer" maxlength="100" required autocomplete="off"></label>
                <label>Электронная почта<input name="email" type="email" maxlength="254" required autocomplete="off" placeholder="demo@example.test"></label>
                <label>Получение<select name="delivery">${Object.entries(deliveryMethods).map(([key, method]) => `<option value="${key}">${method.label} · ${money.format(method.price)}</option>`).join("")}</select></label>
                <label id="address-field" hidden>Адрес доставки<input name="address" maxlength="150" autocomplete="off" disabled></label>
                <button class="button" type="submit">Подтвердить демозаказ</button>
            </form>
            <aside class="summary" id="checkout-total" aria-label="Итог заказа" aria-live="polite">${totals(lines, 0)}</aside>
        </div>`;
}

function confirmationPage() {
    if (!completedOrder) return `<h1>Оформление заказа</h1>${emptyCart()}`;
    return `<h1>Демозаказ оформлен</h1><div class="empty">
        <p>${completedOrder.method} · ${money.format(completedOrder.total)}</p>
        <p>Оплата не проводилась.</p>
        <a href="#catalog" class="button secondary">Вернуться в каталог</a>
    </div>`;
}

function render(focus = false) {
    const [page = "home", detail] = (location.hash.slice(1) || "home").split("/");
    const product = products.find(candidate => candidate.id === detail);
    let view;
    switch (page) {
        case "catalog": view = catalogPage(detail); break;
        case "product": view = product ? productPage(product) : catalogPage(); break;
        case "cart": view = cartPage(items()); break;
        case "checkout": view = checkoutPage(items()); break;
        case "confirmation": view = confirmationPage(); break;
        default: view = homePage();
    }
    main.innerHTML = view;
    document.title = `${main.querySelector("h1").textContent} · OldSchool Journal`;
    document.querySelectorAll(".header-row nav a, .basket").forEach(link => {
        if (link.hash === `#${page}`) link.setAttribute("aria-current", "page");
        else link.removeAttribute("aria-current");
    });
    if (focus) {
        window.scrollTo(0, 0);
        main.focus({ preventScroll: true });
    }
}

document.querySelector(".skip").addEventListener("click", event => {
    event.preventDefault();
    main.focus();
});

main.addEventListener("click", event => {
    const button = event.target.closest("button[data-action]");
    if (!button) return;
    const key = button.closest("[data-key]").dataset.key;
    const item = items().find(line => line.key === key);
    if (!item) return;
    const action = button.dataset.action;
    if (action === "remove") delete cart[key];
    if (action === "less") cart[key] = Math.max(1, item.quantity - 1);
    if (action === "more") cart[key] = Math.min(item.variant.stock, item.quantity + 1);
    saveCart();
    render();
    const replacement = main.querySelector(`[data-key="${key}"] [data-action="${action}"]:not(:disabled)`);
    (replacement || main).focus({ preventScroll: true });
    showNotice(action === "remove" ? "Товар удалён" : "Количество обновлено");
});

main.addEventListener("change", event => {
    if (event.target.name !== "delivery") return;
    const method = deliveryMethods[event.target.value];
    const address = main.querySelector("#address-field");
    const courier = event.target.value === "courier";
    address.hidden = !courier;
    address.querySelector("input").disabled = !courier;
    address.querySelector("input").required = courier;
    main.querySelector("#checkout-total").innerHTML = totals(items(), method.price);
});

main.addEventListener("submit", event => {
    event.preventDefault();
    if (event.target.id === "add-product") {
        const product = products.find(candidate => candidate.id === event.target.dataset.product);
        const index = Number(new FormData(event.target).get("variant"));
        const variant = product.variants[index];
        const key = `${product.id}-${index}`;
        const quantity = cart[key] || 0;
        if (quantity >= variant.stock) {
            showNotice("Доступное количество уже в корзине");
            return;
        }
        cart[key] = quantity + 1;
        saveCart();
        showNotice("Товар добавлен в корзину");
    } else if (event.target.id === "checkout" && items().length) {
        const method = deliveryMethods[new FormData(event.target).get("delivery")];
        completedOrder = { method: method.label, total: subtotal(items()) + method.price };
        cart = {};
        saveCart();
        notice.textContent = "";
        location.hash = "confirmation";
    }
});

window.addEventListener("hashchange", () => render(true));
saveCart();
render();
