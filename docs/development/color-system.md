# 🎨 JewGo Color System Guide

## Overview

This document outlines the comprehensive and consistent color system for the JewGo application. The color system is designed to provide semantic meaning, maintain brand consistency, and ensure accessibility across all components.

## 🎯 Design Principles

- **Semantic Colors**: Colors have specific meanings (success, warning, kosher types, etc.)
- **Brand Consistency**: Primary colors reflect the JewGo brand identity
- **Accessibility**: All color combinations meet WCAG contrast requirements
- **Scalability**: Color system supports future growth and new features

## 🌈 Primary Brand Colors

### JewGo Mint Green Scale
```css
--jewgo-50: #f0fdf4   /* Very light mint */
--jewgo-100: #dcfce7  /* Light mint */
--jewgo-200: #bbf7d0  /* Lighter mint */
--jewgo-300: #86efac  /* Light mint */
--jewgo-400: #4ade80  /* Primary mint green */
--jewgo-500: #22c55e  /* Medium mint */
--jewgo-600: #16a34a  /* Darker mint */
--jewgo-700: #15803d  /* Dark mint */
--jewgo-800: #166534  /* Very dark mint */
--jewgo-900: #14532d  /* Darkest mint */
--jewgo-950: #052e16  /* Near black mint */
```

**Usage**: Primary brand color, buttons, links, active states

## 🎨 Neutral Colors

### Gray Scale (Neutral)
```css
--neutral-50: #fafafa   /* Very light gray */
--neutral-100: #f5f5f5  /* Light gray */
--neutral-200: #e5e5e5  /* Lighter gray */
--neutral-300: #d4d4d4  /* Light gray */
--neutral-400: #a3a3a3  /* Medium gray */
--neutral-500: #737373  /* Gray */
--neutral-600: #525252  /* Darker gray */
--neutral-700: #404040  /* Dark gray */
--neutral-800: #262626  /* Very dark gray */
--neutral-900: #171717  /* Darkest gray */
--neutral-950: #0a0a0a  /* Near black */
```

**Usage**: Text, borders, backgrounds, disabled states

## 🌟 Accent Colors

### Blue Accent
```css
--accent-blue: #3B82F6      /* Primary blue */
--accent-blue-dark: #2563EB /* Dark blue */
```

### Green Accent
```css
--accent-green: #10B981     /* Success green */
--accent-green-dark: #059669 /* Dark green */
```

### Yellow Accent
```css
--accent-yellow: #F59E0B    /* Warning yellow */
--accent-yellow-dark: #D97706 /* Dark yellow */
```

### Purple Accent
```css
--accent-purple: #8B5CF6    /* Purple accent */
--accent-purple-dark: #7C3AED /* Dark purple */
```

### Orange Accent
```css
--accent-orange: #F97316    /* Orange accent */
--accent-orange-dark: #EA580C /* Dark orange */
```

## 🍽️ Kosher Category Colors

### Meat (Red)
```css
--kosher-meat: #ef4444        /* Meat red */
--kosher-meat-light: #fef2f2  /* Light meat background */
--kosher-meat-dark: #dc2626   /* Dark meat */
```

### Dairy (Blue)
```css
--kosher-dairy: #3b82f6       /* Dairy blue */
--kosher-dairy-light: #eff6ff /* Light dairy background */
--kosher-dairy-dark: #2563eb  /* Dark dairy */
```

### Pareve (Yellow)
```css
--kosher-pareve: #f59e0b      /* Pareve yellow */
--kosher-pareve-light: #fffbeb /* Light pareve background */
--kosher-pareve-dark: #d97706 /* Dark pareve */
```

### Unknown (Gray)
```css
--kosher-unknown: #6b7280     /* Unknown gray */
--kosher-unknown-light: #f9fafb /* Light unknown background */
--kosher-unknown-dark: #374151 /* Dark unknown */
```

## 🏛️ Certification Agency Colors

### ORB (Blue)
```css
--agency-orb: #1e40af         /* ORB blue */
--agency-orb-light: #dbeafe   /* Light ORB background */
```

### KM (Green)
```css
--agency-km: #10b981          /* KM green */
--agency-km-light: #d1fae5    /* Light KM background */
```

### KDM (Yellow)
```css
--agency-kdm: #f59e0b         /* KDM yellow */
--agency-kdm-light: #fef3c7   /* Light KDM background */
```

### Diamond K (Purple)
```css
--agency-diamond-k: #8b5cf6   /* Diamond K purple */
--agency-diamond-k-light: #ede9fe /* Light Diamond K background */
```

## 📊 Status Colors

### Success
```css
--status-success: #10b981      /* Success green */
--status-success-light: #d1fae5 /* Light success background */
```

### Warning
```css
--status-warning: #f59e0b      /* Warning yellow */
--status-warning-light: #fef3c7 /* Light warning background */
```

### Error
```css
--status-error: #ef4444        /* Error red */
--status-error-light: #fef2f2  /* Light error background */
```

### Info
```css
--status-info: #3b82f6         /* Info blue */
--status-info-light: #dbeafe   /* Light info background */
```

## 🎨 Usage Guidelines

### Buttons
- **Primary**: `bg-gradient-jewgo` (mint gradient)
- **Secondary**: `bg-neutral-100 text-neutral-700`
- **Success**: `bg-status-success text-white`
- **Warning**: `bg-status-warning text-white`
- **Error**: `bg-status-error text-white`

### Text Colors
- **Primary**: `text-neutral-900`
- **Secondary**: `text-neutral-600`
- **Muted**: `text-neutral-500`
- **Disabled**: `text-neutral-400`
- **Brand**: `text-jewgo-400`

### Borders
- **Default**: `border-neutral-200`
- **Focus**: `border-jewgo-400`
- **Error**: `border-status-error`
- **Success**: `border-status-success`

### Backgrounds
- **Primary**: `bg-white`
- **Secondary**: `bg-neutral-50`
- **Brand**: `bg-jewgo-50`
- **Overlay**: `bg-neutral-900/50`

## 🎯 Component-Specific Usage

### Restaurant Cards
```css
.restaurant-card {
  @apply bg-white border-neutral-200;
}

.restaurant-card:hover {
  @apply border-jewgo-400/20;
}
```

### Search Bar
```css
.search-bar {
  @apply border-neutral-300 focus:border-jewgo-400;
}
```

### Kosher Badges
```css
.kosher-meat { @apply bg-kosher-meat-light text-kosher-meat; }
.kosher-dairy { @apply bg-kosher-dairy-light text-kosher-dairy; }
.kosher-pareve { @apply bg-kosher-pareve-light text-kosher-pareve; }
```

### Agency Badges
```css
.agency-orb { @apply bg-agency-orb-light text-agency-orb; }
.agency-km { @apply bg-agency-km-light text-agency-km; }
.agency-kdm { @apply bg-agency-kdm-light text-agency-kdm; }
.agency-diamond-k { @apply bg-agency-diamond-k-light text-agency-diamond-k; }
```

## 🌈 Gradients

### Primary Gradient
```css
.bg-gradient-jewgo {
  background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
}
```

### Text Gradient
```css
.text-gradient {
  background: linear-gradient(135deg, var(--jewgo-400), var(--accent-green));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

## 📱 Responsive Considerations

### Mobile
- Use higher contrast colors for better readability
- Ensure touch targets have sufficient contrast
- Consider reduced motion preferences

### Dark Mode (Future)
- Plan for dark mode variants of all colors
- Maintain semantic meaning in dark mode
- Ensure accessibility standards are met

## ♿ Accessibility

### Contrast Ratios
- **Normal Text**: Minimum 4.5:1 contrast ratio
- **Large Text**: Minimum 3:1 contrast ratio
- **UI Components**: Minimum 3:1 contrast ratio

### Color Blindness
- Don't rely solely on color to convey information
- Use icons, patterns, and text labels
- Test with color blindness simulators

### Focus Indicators
- Use `focus:ring-jewgo-400/20` for focus states
- Ensure focus indicators are visible
- Maintain consistent focus styling

## 🔧 Implementation

### Tailwind Classes
```css
/* Primary brand colors */
text-jewgo-400
bg-jewgo-400
border-jewgo-400

/* Neutral colors */
text-neutral-600
bg-neutral-50
border-neutral-200

/* Kosher categories */
bg-kosher-meat-light
text-kosher-dairy

/* Agency colors */
bg-agency-orb-light
text-agency-km

/* Status colors */
bg-status-success
text-status-error
```

### CSS Variables
```css
/* Use CSS variables for custom styling */
color: var(--jewgo-400);
background-color: var(--kosher-meat-light);
border-color: var(--neutral-200);
```

## 📋 Best Practices

1. **Consistency**: Always use the defined color system
2. **Semantic Meaning**: Use colors that match their purpose
3. **Accessibility**: Test contrast ratios and color blindness
4. **Brand Alignment**: Maintain JewGo brand identity
5. **Future-Proofing**: Plan for dark mode and new features

## 🚀 Migration Guide

### From Old Colors
```css
/* Old */
text-gray-500 → text-neutral-500
bg-blue-100 → bg-accent-blue-light
border-gray-200 → border-neutral-200

/* New */
text-jewgo-400 → text-jewgo-400
bg-kosher-meat-light → bg-kosher-meat-light
border-neutral-200 → border-neutral-200
```

### Legacy Support
- Old color classes are maintained for backward compatibility
- Gradually migrate components to new system
- Update documentation as components are migrated

---

**Last Updated**: July 2024
**Version**: 2.0
**Maintainer**: Development Team 