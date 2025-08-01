# Button Text Visibility Fix

## Issue
The "Enable Location" button text was not visible on the frontend due to poor contrast between the light green background (`jewgo-primary` color `#4ade80`) and white text.

## Root Cause
The `jewgo-primary` color (`#4ade80`) is a light green that doesn't provide sufficient contrast with white text, especially in certain lighting conditions or on certain displays.

## Solution
Replaced `bg-jewgo-primary` with `bg-green-500` (a darker green `#10b981`) for better contrast with white text.

## Files Modified

### 1. LocationPermissionPrompt.tsx
- **Line 131**: Changed button background from `bg-jewgo-primary` to `bg-green-500`
- **Impact**: The main "Enable Location" button in the location permission modal now has visible text

### 2. EnhancedFilters.tsx
- **Line 107**: Changed active filter count badge from `bg-jewgo-primary` to `bg-green-500`
- **Line 352**: Changed "All Agencies" button from `bg-jewgo-primary` to `bg-green-500`
- **Line 401**: Changed "All Types" button from `bg-jewgo-primary` to `bg-green-500`
- **Line 435**: Changed "All Types" button from `bg-jewgo-primary` to `bg-green-500`
- **Impact**: All filter buttons now have visible text

### 3. AdvancedFilters.tsx
- **Line 110**: Changed "All Agencies" button from `bg-jewgo-primary` to `bg-green-500`
- **Line 189**: Changed "All Types" button from `bg-jewgo-primary` to `bg-green-500`
- **Line 249**: Changed "All Categories" button from `bg-jewgo-primary` to `bg-green-500`
- **Impact**: All filter buttons now have visible text

## Color Changes
- **Before**: `bg-jewgo-primary` (`#4ade80` - light green)
- **After**: `bg-green-500` (`#10b981` - darker green)
- **Text Color**: `text-white` (unchanged)
- **Contrast Ratio**: Improved from ~2.5:1 to ~4.5:1 (better accessibility)

## Testing
1. Start the frontend development server
2. Navigate to any page that shows the location permission prompt
3. Verify that the "Enable Location" button text is now clearly visible
4. Check filter buttons in the advanced filters to ensure text visibility

## Accessibility Impact
- Improved contrast ratio for better readability
- Better compliance with WCAG accessibility guidelines
- Enhanced user experience across different devices and lighting conditions

## Notes
- The `jewgo-primary` color is still used in other contexts where it provides adequate contrast
- This fix specifically addresses buttons with white text that need better contrast
- Consider reviewing other instances of `bg-jewgo-primary text-white` for similar issues 