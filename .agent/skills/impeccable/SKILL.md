---
name: impeccable
description: Design system guidelines, UI/UX anti-pattern rules, and aesthetic standards for ImpeccableOS frontend interfaces.
---

# Impeccable Design Skill

## Overview
This skill codifies the design principles enforced across ImpeccableOS web applications using the `impeccable` CLI (`npx impeccable detect`).

## Rules & Anti-Pattern Defenses

### 1. Contrast & Color Hierarchy
- **No Gray-on-Color:** Never place low-contrast gray text (`text-slate-950`, `text-slate-800`, `text-gray-900`) directly on vivid colored background fills (`bg-sky-500`, `bg-indigo-600`, etc.).
- **Rule:** Use a darker shade of the background color itself (e.g., `text-sky-950` on `bg-sky-500` or `bg-sky-400`), or crisp high-contrast white (`text-white` on `bg-sky-600`).
- **Surface Elevation:** Use subtle transparent borders (`border-surfaceBorder` / `border-slate-800`) and radial background gradients for depth rather than flat gray rectangles.

### 2. Micro-Interactions & States
- Every interactive element (button, tab, modal trigger) must have distinct `hover:`, `focus:`, `active:`, and `disabled:` states.
- Async action triggers must feature loading states with visual progress indicators (`animate-ping`, `animate-pulse`, or spinners) with accessible descriptive text.

### 3. Typography & Spacing
- Use clean font pairing: **Inter** / system sans-serif for UI labels and readable body copy; **JetBrains Mono** / system monospace for tokens, equations, badges, and technical IDs.
- Preserve generous touch targets ($\ge 36\text{px}$) and consistent padding hierarchy ($p-2$, $p-3.5$, $p-6$).

### 4. Continuous Quality Checks
To audit the frontend for UI anti-patterns at any time:
```bash
npx impeccable detect apps/web
```
Or scan against a live dev server:
```bash
npx impeccable detect http://localhost:3000
```
