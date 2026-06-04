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
