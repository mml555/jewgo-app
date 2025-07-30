import { chromium, FullConfig } from '@playwright/test';

/**
 * Global setup for Playwright tests
 * This runs once before all tests
 */
async function globalSetup(config: FullConfig) {
  const { baseURL, storageState } = config.projects[0].use;
  
  console.log('🔧 Setting up global test environment...');
  
  // Start browser
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  try {
    // Navigate to the application
    await page.goto(baseURL || 'http://localhost:3000');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check if we need to handle authentication
    const isLoggedIn = await page.locator('[data-testid="user-menu"]').isVisible().catch(() => false);
    
    if (!isLoggedIn) {
      console.log('⚠️  User not logged in, setting up test authentication...');
      
      // For now, we'll skip authentication in tests
      // In a real scenario, you might want to:
      // 1. Create a test user
      // 2. Log in programmatically
      // 3. Save the authentication state
      
      // Example authentication setup (commented out):
      /*
      await page.goto(`${baseURL}/auth/signin`);
      await page.fill('[data-testid="email"]', 'test@example.com');
      await page.fill('[data-testid="password"]', 'testpassword');
      await page.click('[data-testid="signin-button"]');
      await page.waitForURL(`${baseURL}/`);
      */
    }
    
    // Save authentication state for other tests
    await page.context().storageState({ path: storageState as string });
    
    console.log('✅ Global setup completed successfully');
    
  } catch (error) {
    console.error('❌ Global setup failed:', error);
    throw error;
  } finally {
    await browser.close();
  }
}

export default globalSetup; 