#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Browser Manager - Centralized Browser Lifecycle Management
===========================================================

Provides robust browser session management for all Selenium scrapers.

Features:
- Retry logic for browser startup (3 attempts)
- Banner/consent dialog dismissal
- Safe navigation with timeouts
- Guaranteed cleanup (never hangs)
- Force kill if driver.quit() fails

Usage:
    from Scraper.lib.browser_manager import BrowserManager

    # Setup
    driver = BrowserManager.setup_chrome()

    # Navigate
    BrowserManager.safe_navigate(driver, "https://example.com")
    BrowserManager.dismiss_banners(driver)

    # Cleanup
    BrowserManager.force_close(driver)
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BrowserManager:
    """Manages browser lifecycle with robust error handling"""

    # Default Chrome profile for all scrapers
    DEFAULT_PROFILE_PATH = r"C:\Users\Iccanui\AppData\Local\Google\Chrome\User Data\Scraper_Profile"

    @staticmethod
    def setup_chrome(profile_path: str = None, headless: bool = False) -> webdriver.Chrome:
        """
        Open Chrome with scraper profile.

        Args:
            profile_path: Chrome profile directory (default: DEFAULT_PROFILE_PATH)
            headless: Run in headless mode (default: False)

        Returns:
            WebDriver instance

        Raises:
            Exception: If Chrome fails to start after 3 attempts
        """
        if profile_path is None:
            profile_path = BrowserManager.DEFAULT_PROFILE_PATH

        for attempt in range(3):
            try:
                options = Options()
                options.add_argument(f"user-data-dir={profile_path}")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-logging"])
                options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

                if headless:
                    options.add_argument("--headless")

                print(f"[BrowserManager] Starting Chrome (attempt {attempt + 1}/3)...")
                driver = webdriver.Chrome(options=options)
                driver.maximize_window()

                print("[BrowserManager] ✅ Chrome started successfully")
                return driver

            except Exception as e:
                print(f"[BrowserManager] ❌ Attempt {attempt + 1} failed: {e}")
                if attempt == 2:  # Last attempt
                    raise Exception(f"Failed to start Chrome after 3 attempts: {e}")
                time.sleep(5)  # Wait before retry

    @staticmethod
    def dismiss_banners(driver: webdriver.Chrome):
        """
        Dismiss common consent and modal banners.

        Non-blocking - doesn't fail if no banners found.
        """
        selectors = [
            (By.ID, "onetrust-accept-btn-handler"),
            (By.CSS_SELECTOR, "#onetrust-accept-btn-handler"),
            (By.XPATH, "//button[contains(., 'Accept All')]"),
            (By.XPATH, "//button[contains(., 'I Accept')]"),
            (By.XPATH, "//button[contains(., 'I agree') or contains(., 'I Agree')]"),
            (By.CSS_SELECTOR, "button[aria-label='Close']"),
            (By.XPATH, "//button[contains(., 'Close')]"),
        ]

        for by, selector in selectors:
            try:
                element = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((by, selector))
                )
                element.click()
                print("[BrowserManager] ✓ Dismissed consent banner")
                time.sleep(1)  # Let animation complete
                return
            except:
                pass  # Continue to next selector

    @staticmethod
    def safe_navigate(driver: webdriver.Chrome, url: str, retries: int = 3) -> bool:
        """
        Navigate to URL with retry logic.

        Args:
            driver: WebDriver instance
            url: Target URL
            retries: Number of retry attempts (default: 3)

        Returns:
            True if successful, False if all retries failed
        """
        for attempt in range(retries):
            try:
                print(f"[BrowserManager] Navigating to: {url} (attempt {attempt + 1}/{retries})")
                driver.get(url)

                # Wait for page to load (basic check)
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )

                print(f"[BrowserManager] ✓ Page loaded successfully")
                return True

            except Exception as e:
                print(f"[BrowserManager] ❌ Navigation failed: {e}")
                if attempt < retries - 1:
                    time.sleep(3)  # Wait before retry

        return False

    @staticmethod
    def force_close(driver: webdriver.Chrome):
        """
        Guaranteed cleanup - never fails.

        Attempts driver.quit() first, then force kills Chrome processes if needed.
        """
        try:
            print("[BrowserManager] Closing browser...")
            driver.quit()
            print("[BrowserManager] ✓ Browser closed successfully")
        except:
            print("[BrowserManager] ⚠ driver.quit() failed, attempting force kill...")
            try:
                # Try psutil for clean process kill
                import psutil
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        if 'chrome' in proc.info['name'].lower():
                            cmdline = proc.info['cmdline'] or []
                            if any('Scraper_Profile' in str(arg) for arg in cmdline):
                                proc.kill()
                                print(f"[BrowserManager] ✓ Killed Chrome process {proc.info['pid']}")
                    except:
                        pass
            except ImportError:
                # Fallback: Use OS-specific kill
                import os
                import subprocess
                if sys.platform == 'win32':
                    # Windows: taskkill
                    try:
                        subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'],
                                     capture_output=True, timeout=5)
                        print("[BrowserManager] ✓ Chrome processes killed (Windows)")
                    except:
                        print("[BrowserManager] ⚠ Force kill failed")
                else:
                    # Unix: pkill
                    try:
                        subprocess.run(['pkill', '-9', 'chrome'],
                                     capture_output=True, timeout=5)
                        print("[BrowserManager] ✓ Chrome processes killed (Unix)")
                    except:
                        print("[BrowserManager] ⚠ Force kill failed")

    @staticmethod
    def wait_for_element(driver: webdriver.Chrome, by: By, selector: str, timeout: int = 10):
        """
        Wait for element to be present.

        Args:
            driver: WebDriver instance
            by: Locator strategy (By.ID, By.CSS_SELECTOR, etc.)
            selector: Element selector
            timeout: Max wait time in seconds

        Returns:
            WebElement if found, None if timeout
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return element
        except:
            return None

    @staticmethod
    def click_if_present(driver: webdriver.Chrome, by: By, selector: str, timeout: int = 2) -> bool:
        """
        Click element if present (non-blocking).

        Returns:
            True if clicked, False if not found
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, selector))
            )
            element.click()
            return True
        except:
            return False
