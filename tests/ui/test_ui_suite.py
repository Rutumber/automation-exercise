import uuid


def generate_email():
    return f"automation{uuid.uuid4().hex[:8]}@example.com"


def register_user(page, email, password="Password123"):
    page.goto("https://automationexercise.com/signup", wait_until="domcontentloaded", timeout=60000)
    page.fill("input[data-qa='signup-name']", "Test User")
    page.fill("input[data-qa='signup-email']", email)
    page.click("button[data-qa='signup-button']")

    page.wait_for_selector("text=Enter Account Information", timeout=15000)
    page.check("input#id_gender1")
    page.fill("input[data-qa='password']", password)
    page.select_option("select[data-qa='days']", "1")
    page.select_option("select[data-qa='months']", "January")
    page.select_option("select[data-qa='years']", "2000")
    page.check("input#newsletter")
    page.check("input#optin")

    page.fill("input[data-qa='first_name']", "Test")
    page.fill("input[data-qa='last_name']", "User")
    page.fill("input#company", "TestCo")
    page.fill("input#address1", "123 Test St")
    page.fill("input#address2", "Suite 1")
    page.select_option("select#country", "India")
    page.fill("input#state", "TestState")
    page.fill("input#city", "TestCity")
    page.fill("input#zipcode", "12345")
    page.fill("input#mobile_number", "1234567890")

    page.click("button[data-qa='create-account']")
    page.wait_for_url("**/account_created", timeout=20000)
    page.click("a[data-qa='continue-button']")
    page.wait_for_url("https://automationexercise.com/", timeout=30000)
    page.wait_for_selector("a[href='/logout']", timeout=15000)


def test_register_user(page):
    email = generate_email()
    register_user(page, email)
    assert page.locator("text=Logged in as").first.is_visible()


def login_user(page, email, password="Password123"):
    page.goto("https://automationexercise.com/login", wait_until="domcontentloaded", timeout=60000)
    page.fill("input[data-qa='login-email']", email)
    page.fill("input[data-qa='login-password']", password)
    page.click("button[data-qa='login-button']")
    page.wait_for_selector("text=Logged in as", timeout=15000)


def add_first_product_to_cart(page):
    page.goto("https://automationexercise.com/products", wait_until="domcontentloaded", timeout=60000)
    page.evaluate("window.scrollTo(0, 800)")
    page.locator("a", has_text="Add to cart").first.click()
    page.wait_for_selector("#cartModal", timeout=15000)
    page.locator("a", has_text="View Cart").click()
    page.wait_for_url("**/view_cart", timeout=15000)


def proceed_to_checkout(page):
    page.locator("a.check_out").click()
    page.wait_for_selector("text=Checkout", timeout=20000)
    page.wait_for_timeout(500)


def open_payment_page(page):
    page.locator("a[href='/payment']").click()
    page.wait_for_url("**/payment", timeout=20000)


def test_login_user_with_correct_email_and_password(page):
    email = generate_email()
    password = "Password123"
    register_user(page, email, password)
    page.click("a[href='/logout']")

    login_user(page, email, password)
    assert page.locator("text=Logged in as").first.is_visible()


def test_login_user_with_incorrect_email_and_password(page):
    page.goto("https://automationexercise.com/login", wait_until="domcontentloaded", timeout=60000)

    page.fill("input[data-qa='login-email']", "invalid_user@example.com")
    page.fill("input[data-qa='login-password']", "WrongPassword123")
    page.click("button[data-qa='login-button']")

    page.wait_for_selector("text=Your email or password is incorrect!", timeout=10000)
    assert "Your email or password is incorrect!" in page.text_content("body")


def test_logout_user(page):
    email = generate_email()
    register_user(page, email)
    page.click("a[href='/logout']")
    page.wait_for_url("**/login", timeout=20000)

    assert page.locator("h2", has_text="Login to your account").is_visible()


def test_register_user_with_existing_email(page):
    email = generate_email()
    register_user(page, email)

    page.goto("https://automationexercise.com/signup", wait_until="domcontentloaded", timeout=60000)
    page.fill("input[data-qa='signup-name']", "Test User")
    page.fill("input[data-qa='signup-email']", email)
    page.click("button[data-qa='signup-button']")

    page.wait_for_selector("text=Email Address already exist!", timeout=15000)
    assert "Email Address already exist!" in page.text_content("body")


def test_contact_us_form(page):
    page.goto("https://automationexercise.com/contact_us", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("form#contact-us-form", timeout=10000)

    assert page.locator("input[data-qa='name']").is_visible()
    assert page.locator("input[data-qa='email']").is_visible()
    assert page.locator("textarea[data-qa='message']").is_visible()

    page.fill("input[data-qa='name']", "Test Contact")
    page.fill("input[data-qa='email']", "testcontact@example.com")
    page.fill("input[data-qa='subject']", "Test subject")
    page.fill("textarea[data-qa='message']", "This is a test message.")
    page.once("dialog", lambda dialog: dialog.accept())
    page.click("input[data-qa='submit-button']")

    page.wait_for_selector("div.status.alert.alert-success", timeout=20000)
    success_text = page.text_content("div.status.alert.alert-success")
    assert success_text is not None and "successfully" in success_text.lower()


def test_verify_test_cases_page(page):
    page.goto("https://automationexercise.com/test_cases", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("text=Test Cases", timeout=10000)

    assert page.locator("text=Test Case 1: Register User").is_visible()


def test_verify_all_products_and_product_detail_page(page):
    page.goto("https://automationexercise.com/products", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("input#search_product", timeout=10000)

    assert page.locator("input#search_product").is_visible()
    assert page.locator("a[href*='/product_details']").count() > 0

    page.click("a[href*='/product_details']")
    page.wait_for_url("**/product_details/**", timeout=10000)

    assert page.locator("div.product-information").is_visible()


def test_search_product(page):
    page.goto("https://automationexercise.com/products", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("input#search_product", timeout=10000)

    page.fill("input#search_product", "Blue Top")
    page.click("button#submit_search")
    page.wait_for_selector("div.features_items div.col-sm-4", timeout=10000)

    assert "Blue Top" in page.text_content("div.features_items")
    assert page.locator("div.features_items div.col-sm-4").count() >= 1


def test_verify_subscription_in_home_page(page):
    page.goto("https://automationexercise.com", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("h2:has-text('Subscription')", timeout=10000)

    assert page.locator("h2:has-text('Subscription')").is_visible()
    assert page.locator("input#susbscribe_email").is_visible()


def test_verify_subscription_in_cart_page(page):
    page.goto("https://automationexercise.com/view_cart", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("h2:has-text('Subscription')", timeout=10000)

    assert page.locator("h2:has-text('Subscription')").is_visible()
    assert page.locator("input#susbscribe_email").is_visible()


def test_add_products_in_cart(page):
    add_first_product_to_cart(page)
    assert page.locator("section#cart_items tbody tr").count() >= 1
    assert page.locator("ol.breadcrumb li.active:has-text('Shopping Cart')").is_visible()


def test_verify_product_quantity_in_cart(page):
    add_first_product_to_cart(page)
    assert page.locator("section#cart_items tbody tr").count() >= 1
    assert page.locator("section#cart_items tbody tr td.cart_quantity button").first.text_content().strip() == "1"


def test_place_order_register_while_checkout(page):
    add_first_product_to_cart(page)
    proceed_to_checkout(page)

    page.locator("a[href='/login']", has_text="Register / Login").first.click()
    page.wait_for_url("**/login", timeout=15000)

    email = generate_email()
    page.fill("input[data-qa='signup-name']", "Test User")
    page.fill("input[data-qa='signup-email']", email)
    page.click("button[data-qa='signup-button']")

    page.wait_for_selector("text=Enter Account Information", timeout=15000)
    page.check("input#id_gender1")
    page.fill("input[data-qa='password']", "Password123")
    page.select_option("select[data-qa='days']", "1")
    page.select_option("select[data-qa='months']", "January")
    page.select_option("select[data-qa='years']", "2000")
    page.check("input#newsletter")
    page.check("input#optin")
    page.fill("input[data-qa='first_name']", "Test")
    page.fill("input[data-qa='last_name']", "User")
    page.fill("input#company", "TestCo")
    page.fill("input#address1", "123 Test St")
    page.fill("input#address2", "Suite 1")
    page.select_option("select#country", "India")
    page.fill("input#state", "TestState")
    page.fill("input#city", "TestCity")
    page.fill("input#zipcode", "12345")
    page.fill("input#mobile_number", "1234567890")
    page.click("button[data-qa='create-account']")

    page.wait_for_url("**/account_created", timeout=20000)
    assert page.locator("text=Account Created").is_visible()


def test_place_order_register_before_checkout(page):
    email = generate_email()
    register_user(page, email)
    add_first_product_to_cart(page)
    proceed_to_checkout(page)

    assert page.locator("h2", has_text="Address Details").is_visible()


def test_place_order_login_before_checkout(page):
    email = generate_email()
    password = "Password123"
    register_user(page, email, password)
    page.click("a[href='/logout']")
    login_user(page, email, password)

    add_first_product_to_cart(page)
    proceed_to_checkout(page)

    assert page.locator("h2", has_text="Address Details").is_visible()


def test_remove_products_from_cart(page):
    add_first_product_to_cart(page)
    assert page.locator("section#cart_items tbody tr").count() >= 1
    page.locator("a.cart_quantity_delete").first.click()
    page.wait_for_timeout(1000)
    assert page.locator("section#cart_items tbody tr").count() == 0


def test_view_category_products(page):
    page.goto("https://automationexercise.com", wait_until="domcontentloaded", timeout=60000)
    page.locator("div.panel-group.category-products a").first.click()
    page.wait_for_selector("text=Category", timeout=15000)

    assert page.locator("div.features_items").count() > 0
    assert page.locator("text=Category").is_visible()


def test_view_and_cart_brand_products(page):
    page.goto("https://automationexercise.com", wait_until="domcontentloaded", timeout=60000)
    page.locator("div.left-sidebar h2:has-text('Brands') ~ div a").first.click()
    page.wait_for_url("**/brand_products/**", timeout=15000)

    assert page.locator("div.features_items").count() > 0
    page.evaluate("window.scrollTo(0, 800)")
    page.locator("a", has_text="Add to cart").first.click()
    page.wait_for_selector("#cartModal", timeout=15000)
    assert page.locator("a", has_text="View Cart").is_visible()


def test_search_products_and_verify_cart_after_login(page):
    email = generate_email()
    password = "Password123"
    register_user(page, email, password)
    page.click("a[href='/logout']")
    login_user(page, email, password)

    page.goto("https://automationexercise.com/products", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("input#search_product", timeout=10000)
    page.fill("input#search_product", "Blue Top")
    page.click("button#submit_search")
    page.wait_for_selector("div.features_items div.col-sm-4", timeout=10000)

    page.evaluate("window.scrollTo(0, 800)")
    page.locator("a", has_text="Add to cart").first.click()
    page.wait_for_selector("#cartModal", timeout=15000)
    page.locator("a", has_text="View Cart").click()
    page.wait_for_url("**/view_cart", timeout=15000)

    assert page.locator("section#cart_items tbody tr td.cart_description h4 a").first.is_visible()


def test_add_review_on_product(page):
    page.goto("https://automationexercise.com/product_details/1", wait_until="domcontentloaded", timeout=60000)
    page.fill("input#name", "Test Reviewer")
    page.fill("input#email", "testreview@example.com")
    page.fill("textarea#review", "This is an automated review.")
    page.click("button[type='submit']")
    page.wait_for_selector("div.alert-success.alert", timeout=10000)

    assert "thank you for your review" in page.text_content("div.alert-success.alert").lower()


def test_add_to_cart_from_recommended_items(page):
    page.goto("https://automationexercise.com", wait_until="domcontentloaded", timeout=60000)
    page.evaluate("window.scrollTo(0, 800)")
    page.locator("div.recommended_items a", has_text="Add to cart").first.click()
    page.wait_for_selector("#cartModal", timeout=15000)

    assert page.locator("#cartModal").is_visible()


def test_verify_address_details_in_checkout_page(page):
    email = generate_email()
    register_user(page, email)
    add_first_product_to_cart(page)
    proceed_to_checkout(page)

    assert page.locator("text=Address Details").count() > 0


def test_download_invoice_after_purchase_order(page):
    email = generate_email()
    password = "Password123"
    register_user(page, email, password)
    add_first_product_to_cart(page)
    proceed_to_checkout(page)
    open_payment_page(page)

    page.fill("input[data-qa='name-on-card']", "Test Card")
    page.fill("input[name='card_number']", "4242424242424242")
    page.fill("input[name='cvc']", "123")
    page.fill("input[name='expiry_month']", "12")
    page.fill("input[name='expiry_year']", "2028")
    page.click("button[data-qa='pay-button']")

    page.wait_for_url("**/payment_done/**", timeout=20000)
    assert "download invoice" in page.text_content("body").lower()
    assert page.locator("a", has_text="Download Invoice").count() > 0


def test_verify_scroll_up_with_arrow_button(page):
    page.goto("https://automationexercise.com", wait_until="domcontentloaded", timeout=60000)
    assert page.locator("#scrollUp").count() == 1
    assert not page.locator("#scrollUp").is_visible()

    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    assert page.locator("#scrollUp").is_visible()
    page.click("#scrollUp")
    page.wait_for_timeout(1000)
    assert page.evaluate("window.scrollY") == 0


def test_verify_scroll_up_without_arrow_button_and_scroll_down(page):
    page.goto("https://automationexercise.com", wait_until="domcontentloaded", timeout=60000)
    page.evaluate("window.scrollTo(0, 1000)")
    page.wait_for_timeout(1000)
    assert page.evaluate("window.scrollY") > 0
    page.evaluate("window.scrollTo(0, 0)")
    assert page.evaluate("window.scrollY") == 0
