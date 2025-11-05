"""
Browser testing tool to check for console errors in web applications
"""
import asyncio
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, ConsoleMessage
from loguru import logger


class BrowserTester:
    """Test web applications using browser automation"""
    
    def __init__(self):
        """Initialize browser tester"""
        self.console_messages = []
        self.console_errors = []
        
    async def check_webapp_console(
        self, 
        url: str, 
        wait_time: int = 5,
        check_network: bool = True
    ) -> Dict:
        """
        Open a web application and check for console errors
        
        Args:
            url: URL to test (e.g., http://localhost:3000)
            wait_time: How long to wait for page to load (seconds)
            check_network: Whether to check for network errors
            
        Returns:
            Dict with console errors, warnings, and network issues
        """
        logger.info(f"Testing web app at: {url}")
        
        self.console_messages = []
        self.console_errors = []
        network_errors = []
        
        try:
            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Listen to console messages
                page.on("console", lambda msg: self._handle_console_message(msg))
                
                # Listen to page errors
                page.on("pageerror", lambda err: self.console_errors.append({
                    "type": "pageerror",
                    "message": str(err)
                }))
                
                # Listen to network failures if requested
                if check_network:
                    page.on("requestfailed", lambda req: network_errors.append({
                        "url": req.url,
                        "error": req.failure
                    }))
                
                # Navigate to URL
                try:
                    await page.goto(url, timeout=wait_time * 1000)
                    
                    # Wait for page to load and stabilize
                    await page.wait_for_load_state("networkidle", timeout=wait_time * 1000)
                    
                    # Take screenshot for reference
                    screenshot_path = "last_test_screenshot.png"
                    await page.screenshot(path=screenshot_path)
                    logger.info(f"Screenshot saved to: {screenshot_path}")
                    
                    # Get page title
                    title = await page.title()
                    
                except Exception as e:
                    logger.error(f"Failed to load page: {str(e)}")
                    await browser.close()
                    return {
                        "success": False,
                        "error": f"Failed to load page: {str(e)}",
                        "console_errors": [],
                        "console_warnings": [],
                        "network_errors": []
                    }
                
                await browser.close()
                
                # Filter console messages
                console_errors = [msg for msg in self.console_messages if msg["type"] == "error"]
                console_warnings = [msg for msg in self.console_messages if msg["type"] == "warning"]
                
                # Build result
                result = {
                    "success": True,
                    "url": url,
                    "title": title,
                    "console_errors": console_errors,
                    "console_warnings": console_warnings,
                    "network_errors": network_errors,
                    "has_errors": len(console_errors) > 0 or len(self.console_errors) > 0,
                    "screenshot": screenshot_path
                }
                
                # Log summary
                if result["has_errors"]:
                    logger.warning(f"Found {len(console_errors)} console errors")
                else:
                    logger.info("No console errors found!")
                
                return result
                
        except Exception as e:
            logger.error(f"Browser test failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "console_errors": [],
                "console_warnings": [],
                "network_errors": []
            }
    
    def _handle_console_message(self, msg: ConsoleMessage):
        """Handle console message from browser"""
        msg_type = msg.type
        msg_text = msg.text
        
        self.console_messages.append({
            "type": msg_type,
            "message": msg_text
        })
        
        if msg_type == "error":
            self.console_errors.append({
                "type": "error",
                "message": msg_text
            })
    
    async def test_react_app(self, port: int = 3000) -> Dict:
        """Test a React app running on localhost"""
        return await self.check_webapp_console(f"http://localhost:{port}")
    
    async def test_flask_app(self, port: int = 5000) -> Dict:
        """Test a Flask app running on localhost"""
        return await self.check_webapp_console(f"http://localhost:{port}")
    
    async def test_fastapi_app(self, port: int = 8000) -> Dict:
        """Test a FastAPI app running on localhost"""
        return await self.check_webapp_console(f"http://localhost:{port}")


async def test_browser_tool():
    """Quick test of the browser tester"""
    tester = BrowserTester()
    result = await tester.check_webapp_console("https://example.com")
    print(f"Success: {result['success']}")
    print(f"Errors: {len(result['console_errors'])}")
    return result


if __name__ == "__main__":
    asyncio.run(test_browser_tool())


