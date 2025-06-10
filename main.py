from playwright.sync_api import sync_playwright
import time

def open_and_wait(url):
    playwright = sync_playwright().start()
    browser = playwright.firefox.launch(
        headless=True,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage', 
            '--disable-web-security',
            '--window-size=1920,1080',
            '--start-maximized',
            '--single-process',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-software-rasterizer',
            '--disable-logging',
            '--no-zygote',
            '--disable-background-networking'
        ]
    )
    
    page = browser.new_page(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        bypass_csp=True,
        ignore_https_errors=True,
        java_script_enabled=True
    )
    
    page.set_extra_http_headers({
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    })
    
    page.evaluate("""() => {
        Object.defineProperty(window, 'navigator', {
            value: new Proxy(navigator, {
                has: (target, key) => (key === 'webdriver' ? false : key in target),
                get: (target, key) =>
                    key === 'webdriver' ?
                    false :
                    typeof target[key] === 'function' ?
                    target[key].bind(target) :
                    target[key]
            })
        });
        
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {
                    0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                    description: "Portable Document Format",
                    filename: "internal-pdf-viewer",
                    length: 1,
                    name: "PDF Viewer"
                }
            ]
        });
        
        Object.defineProperty(navigator, 'languages', {
            get: () => ['ru-RU', 'ru', 'en-US', 'en']
        });
    }""")
    
    page.set_default_navigation_timeout(60000)
    page.set_default_timeout(60000)
    
    page.on("load", lambda: page.evaluate("""() => {
        window.localStorage.clear();
        window.sessionStorage.clear();
        caches.keys().then((keys) => {
            keys.forEach((key) => caches.delete(key));
        });
    }"""))

    # Open the link and wait for 35 seconds
    page.goto("")
    time.sleep(35) 
    
    # Close the browser and playwright
    browser.close()
    playwright.stop()