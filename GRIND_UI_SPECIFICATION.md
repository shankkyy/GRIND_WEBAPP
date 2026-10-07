# GRIND - Task-Based Chat Application
## Complete UI/UX Specification & Implementation Guide

---

## **PROJECT OVERVIEW**

**Name:** GRIND  
**Type:** Real-time chat app with gamified task-based rewards  
**Tech Stack:** FastAPI (Backend), React (Frontend), Supabase (Database)  
**Theme:** Minecraft-inspired pixelated aesthetic (retro 2D, NOT fantasy)  
**Target Audience:** Gen Z (18-28 years)  

---

## **DESIGN PHILOSOPHY**

- **Retro Authenticity:** Pixel-perfect 16x16 grid design inspired by early Minecraft
- **Zero LLM Vibes:** Hand-crafted components, intentional spacing, organic interactions
- **Fast & Responsive:** Sub-100ms interactions, instant feedback
- **Mobile-First:** Designed for 5" phones, works on desktop
- **Accessibility:** High contrast, readable fonts, clear hierarchy

---

## **DESIGN SYSTEM**

### **Color Palette**

```
PRIMARY COLORS:
- Background Dark:    #0a0e27 (Deep Navy)
- Grid Background:    #121830 (Slightly lighter, for depth)
- Accent Green:       #00ff41 (Terminal green, high energy)
- Accent Blue:        #00d4ff (Cyan, secondary action)
- Accent Gold:        #ffcc00 (Rewards, important)
- Accent Red:         #ff3333 (Alerts, urgent)
- Accent Purple:      #b366ff (Rare cosmetics, premium)

TEXT COLORS:
- Primary Text:       #ffffff (Pure white)
- Secondary Text:     #b0b8c8 (Muted gray)
- Success:            #00ff41 (Matches accent green)
- Error:              #ff3333 (Matches accent red)
- Disabled:           #4a5568 (Dark gray)

BORDER/DIVIDER:
- Border Default:     #2a3550 (Dark gray-blue)
- Border Hover:       #4a6590 (Lighter blue)
- Grid Lines:         #1a2640 (Subtle 16px grid)
```

### **Typography**

```
PRIMARY FONT: "Minecraft" or fallback stack
- Font Stack: 'Minecraftia', 'Press Start 2P', monospace
- Fallback: Arial, Helvetica, sans-serif (if licensed font unavailable)

FONT SIZES (px):
- H1 (Page Title):    32px, weight: bold, line-height: 1.2
- H2 (Section Title): 24px, weight: bold, line-height: 1.3
- H3 (Card Title):    18px, weight: bold, line-height: 1.3
- Body (Normal):      14px, weight: 400, line-height: 1.5
- Body (Small):       12px, weight: 400, line-height: 1.4
- Button Text:        14px, weight: bold, line-height: 1
- Badges/Tags:        11px, weight: bold, letter-spacing: 0.5px

LETTER SPACING:
- Headings:           1px
- Body:               0px
- UI Elements:        0.5px
```

### **Spacing System**

```
Use 8px base grid for consistency:
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px

Margins & Padding:
- Card padding:       16px (md)
- Section padding:    24px (lg)
- Component gap:      8px (sm)
- Page padding:       16px on mobile, 24px on desktop
```

### **Borders & Corners**

```
Border Style:
- Primary: 2px solid border (not rounded)
- Secondary: 1px solid border
- Dotted: For grid overlays

Corner Radius:
- Corners: 0px (sharp, Minecraft style)
- Button: 2px (subtle softness)
- Only use radius for badges/small elements

Box Shadows:
- Inactive:   none
- Hover:      inset 0 0 8px rgba(0, 255, 65, 0.2)
- Active:     0 0 12px rgba(0, 255, 65, 0.4)
- Floating:   0 4px 12px rgba(0, 0, 0, 0.5)
```

---

## **COMPONENT SPECIFICATIONS**

### **1. NAVIGATION BAR (Bottom Fixed)**

```
Layout: Fixed bottom bar, full width
Height: 64px
Background: #121830 with top border (#2a3550)

Tabs (5):
- 🏠 HOME (Messages + Quick Actions)
- ⚡ CHALLENGES (Daily tasks)
- 🏆 LEADERBOARD (Rankings)
- 🎁 REWARDS (Cosmetics shop, mystery boxes)
- 👤 PROFILE (User profile, stats)

Active State:
- Text Color: #00ff41 (Accent green)
- Border Top: 3px solid #00ff41
- Icon: Scale 1.1

Inactive State:
- Text Color: #b0b8c8 (Gray)
- Icon: Normal scale

Implementation:
- Use React Router for navigation
- Icons: Custom SVG sprites (not icon library)
- Smooth transition: 150ms ease-out
- Click feedback: 80ms flash animation
```

---

### **2. CHAT SCREEN (HOME)**

**Layout Structure:**
```
┌─────────────────────────────┐
│  ROOM NAME | Settings ⚙️    │ ← Header (64px)
├─────────────────────────────┤
│                             │
│   [Messages List]           │ ← Scrollable chat area
│                             │
│   UserA: Message text       │
│   UserB: Message text       │ ← Each message bubble
│   YOU: Message text (right) │
│                             │
│                             │
├─────────────────────────────┤
│  [Input Box] [Send Button]  │ ← Input area (80px)
├─────────────────────────────┤
│  🎡 🎮 💰 🔥 ⚡             │ ← Quick Action Buttons (64px)
└─────────────────────────────┘
```

**Header:**
- Left: Room name (bold, 18px) + member count (small gray)
- Right: Settings icon (clickable)
- Divider line below

**Message Bubbles:**

```
USER MESSAGE (Left):
┌────────────────────┐
│ Username ⭐        │  ← Name + rank badge (12px)
├────────────────────┤
│ Message text here  │  ← 14px, white text
│ with wrapping      │
├────────────────────┤
│ 2:45 PM    ❤️  ↪️  │  ← Time + reactions + reply
└────────────────────┘
- Background: #1a2640
- Border: 1px solid #2a3550
- Padding: 12px
- Max width: 85% of screen
- Margin: 8px 8px

YOUR MESSAGE (Right):
┌────────────────────┐
│ Message text here  │
│                    │
│ 2:46 PM  ✓✓        │  ← Checkmarks for read status
└────────────────────┘
- Background: #00ff41 with 20% opacity (rgba(0, 255, 65, 0.2))
- Border: 1px solid #00ff41
- Align: Right
- Same padding/margin as user messages

REACTION SYSTEM:
- Show inline below message
- Format: [emoji count] [emoji count] [emoji count]
- Example: ⭐ 5  💎 2  🔥 1
- Clickable: Add own reaction
- Hover: Show tooltip "Click to react"

READ RECEIPT:
- Single checkmark ✓ = Sent
- Double checkmark ✓✓ = Delivered
- Blue double checkmark = Read
- Position: Bottom right of message
```

**Input Area:**

```
┌─────────────────────────────┐
│ Type a message...           │ ← Placeholder text
└─────────────────────────────┘
[Emoji]  [File]  [📤 SEND]

Input Box:
- Height: 48px
- Padding: 12px
- Border: 2px solid #2a3550
- On focus: Border becomes #00ff41
- Font: 14px monospace
- Max chars: 500 (show counter at 400+)

Send Button:
- Width: 56px
- Height: 48px
- Background: #00ff41
- Text: "SEND" (14px bold)
- On hover: Background #00cc33 (darker)
- On click: 100ms shrink animation to 95%
- Active state: Glow effect

Emoji/File icons:
- Size: 20px
- Color: #b0b8c8
- On hover: #00ff41
- Clickable: Open emoji picker or file upload
```

**Quick Action Buttons (Fixed Bottom):**

```
┌─────────────────────────────┐
│ 🎡 🎮 💰 🔥 ⚡ 📊          │
└─────────────────────────────┘

Buttons (Left to right):
1. 🎡 SPIN WHEEL - Opens daily spin modal
2. 🎮 CLASH - Start random clash battle
3. 💰 EMERALDS - Shows balance (animated if earned)
4. 🔥 STREAK - Shows current streak (days)
5. ⚡ QUICK CHALLENGE - Mini 10-second game
6. 📊 STATS - Shows today's earnings

Style:
- Size: 48px × 48px
- Background: #2a3550
- Border: 1px solid #00ff41
- Hover: Glow effect
- Click: 80ms pulse animation
- Active: Background #00ff41, text dark

Floating number for earned emeralds:
- Position: Top-right of 💰 button
- Format: "+150 Emeralds"
- Color: #ffcc00
- Animation: Slide up + fade out over 2 seconds
- Only show when earned in this session
```

---

### **3. CLASH BATTLES SCREEN (CHALLENGES TAB)**

**Layout:**

```
┌──────────────────────────────┐
│  AVAILABLE CHALLENGES        │ ← Header
├──────────────────────────────┤
│                              │
│ [30s Speed Tap] [Easy]       │ ← Challenge cards grid
│ Earn: 100 Emeralds          │
│ Your best: 45 taps          │
│ [PLAY NOW]                  │
│                              │
│ [Pattern Memory] [Medium]    │
│ Earn: 150 Emeralds          │
│ [PLAY NOW]                  │
│                              │
│ [Rapid Choice] [Hard]        │
│ Earn: 200 Emeralds          │
│ [PLAY NOW]                  │
│                              │
├──────────────────────────────┤
│ TODAY'S CLASH BATTLES        │ ← Live battles
├──────────────────────────────┤
│ YOU vs RandomUser23          │
│ 🔴 LIVE NOW                 │
│ You: 45 pts | Opp: 38 pts   │
│ [WATCH]                     │
│                              │
└──────────────────────────────┘
```

**Challenge Card:**

```
┌────────────────────────┐
│ 🖱️  SPEED TAPPING      │ ← Icon + Title
│ ⏱️ 30 SECONDS          │ ← Duration
├────────────────────────┤
│ Tap as fast as you can │ ← Description
│ to beat opponents       │
├────────────────────────┤
│ 💰 100 Emeralds        │ ← Base reward
│ Your Best: 45 taps     │ ← Personal best (if played)
│ Global Best: 87 taps   │ ← Global record
├────────────────────────┤
│ [PLAY NOW] [WATCH]     │ ← CTA buttons
└────────────────────────┘

Card sizing:
- Width: 100% with 16px margin on sides
- Height: Auto, min 200px
- Margin bottom: 16px
- Background: #1a2640
- Border: 2px solid #2a3550
- On hover: Border #00ff41, slight scale up
```

**Clash Battle In-Progress Screen:**

```
┌──────────────────────────────┐
│ SPEED TAPPING - LIVE          │
├──────────────────────────────┤
│                              │
│        YOU vs Player_47      │
│                              │
│    ⏱️  45 SECONDS LEFT        │
│                              │
│ YOU:         Player_47:      │
│ ████████░░░░░░  62 pts       │
│ ║████░░░░░░░░░░  48 pts      │
│                              │
│         [TAP AREA]           │
│     (entire screen tappable) │
│                              │
│  Points floating above +1    │
│  when tapping                │
│                              │
│     COMBO x3! 🔥             │
│                              │
└──────────────────────────────┘

Timer display:
- Position: Top center
- Font size: 28px, bold
- Color: Changes based on time:
  - Green (#00ff41) when > 20s
  - Yellow (#ffcc00) when 10-20s
  - Red (#ff3333) when < 10s

Score bars:
- Background: #2a3550
- Fill color: Player 1 = #00ff41, Player 2 = #00d4ff
- Height: 8px
- Shows names on sides
- Updates in real-time

Tap feedback:
- Visual: +1 or +2 floating number
- Haptic: Vibration (if supported)
- Animation: Number rises 40px over 500ms then fades
- Sound: Optional click sound

Combo multiplier:
- Shows when tapping rapidly (3+ taps in 1 second)
- Display: "COMBO x2!" in big bold text
- Color: Rainbow gradient effect
- Position: Center screen, animated scale

End game state:
- Winner/loser animation
- Confetti or particle effect (subtle pixelated squares)
- Show rewards earned
- Auto-play again option
```

---

### **4. LEADERBOARD SCREEN**

**Layout:**

```
┌──────────────────────────────┐
│ LEADERBOARD                  │
├──────────────────────────────┤
│ [WEEKLY ▼] [Room ▼]          │ ← Filters
├──────────────────────────────┤
│                              │
│ 🥇  #1  KingSlayer           │
│     2,450 XP  👑             │ ← Special badge for #1
│     ↑ +150 XP from yesterday │ ← Trend indicator
│                              │
│ 🥈  #2  Shadow_Dev           │
│     2,380 XP                 │
│     → No change              │
│                              │
│ 🥉  #3  NovaGamer            │
│     2,250 XP                 │
│     ↑ +20 XP from yesterday  │
│                              │
│ ⭐  #4  YOU                  │
│     2,100 XP                 │
│     [Golden highlight]       │
│     ↑ +85 XP from yesterday  │
│                              │
│     #5  CoolDude             │
│     2,090 XP                 │
│     ↓ -15 XP from yesterday  │
│                              │
│     #6  NoobMaster           │
│     1,980 XP                 │
│                              │
│    [SHOW MORE]               │ ← Load more (pagination)
│                              │
└──────────────────────────────┘
```

**Leaderboard Entry:**

```
┌────────────────────────────┐
│ 🥇 #1  KingSlayer    👑    │ ← Rank badge, name, badge
│ 2,450 XP | ↑ +150 | 7-day 🔥│ ← Stats, trend, streak
│ [Profile] [Challenge]      │ ← CTAs
└────────────────────────────┘

Entry styling:
- Padding: 12px 16px
- Height: 72px
- Border: 1px solid #2a3550
- Background: #1a2640
- Margin bottom: 8px

Rank badges:
- #1: 🥇 (gold), background glow
- #2: 🥈 (silver)
- #3: 🥉 (bronze)
- #4-10: 🔷 (diamond outline)
- #11-100: ◆ (small diamond)

Trend indicators:
- ↑ = Green text, moving up
- → = Gray text, no change
- ↓ = Red text, moving down

Current user highlight:
- ⭐ instead of rank badge
- Background: #00ff41 with 10% opacity
- Border: 2px solid #00ff41
- Slightly larger font

Filter dropdown:
- Tabs: WEEKLY | MONTHLY | ALL-TIME | ROOM
- Position: Top of list
- Active: Green (#00ff41)
- Inactive: Gray (#b0b8c8)
- Font: 12px bold

Streak display:
- Shows 🔥 + number
- Example: 7-day 🔥
- Color: #ffcc00
- Only show if > 2 days
```

**Multiple Leaderboards:**

```
Switch between:
1. Weekly XP (resets Sunday)
2. Daily Clash Winners (top tappers)
3. All-Time Achievements
4. Room Leaderboard (within current room)
5. Friend Rankings (only connected friends)

Implementation:
- Use bottom sheet/modal
- Smooth fade transitions
- Current leaderboard highlighted
```

---

### **5. SPIN WHEEL MODAL**

**Layout:**

```
┌──────────────────────────────┐
│  DAILY SPIN WHEEL  ✨        │ ← Title + close button
├──────────────────────────────┤
│                              │
│      ╭─────────────────╮     │
│      │  100  │ 200     │     │
│      │   ╭───┼────╮    │     │ ← Spinning wheel (SVG)
│      │   │ 500│ 50 │   │     │
│      │   │  ╭─┼─╮ │   │     │
│      │   │  │1000│ │   │     │
│      │   ╰──┼────╯   │     │
│      │  300 │ 150    │     │
│      ╰─────────────────╯     │
│            ⬇️ POINTER         │
│                              │
│       [SPIN NOW!]            │ ← CTA button
│                              │
│   Next spin in: 18h 23m      │ ← Timer
│                              │
└──────────────────────────────┘
```

**Wheel Mechanics:**

```
Wheel SVG:
- Center circle: 120px diameter
- Outer wheel: 240px diameter
- 8 segments (for 8 different rewards)
- Colors: Gradient from segment to segment
  - Segment 1: #00ff41 (100 Emeralds)
  - Segment 2: #00d4ff (200 Emeralds)
  - Segment 3: #ffcc00 (500 Emeralds - RARE)
  - Segment 4: #b366ff (1000 Emeralds - LEGENDARY 5%)
  - Segment 5: #ff3333 (50 Emeralds - trap)
  - Segment 6: #00ff41 (300 Emeralds)
  - Segment 7: #00d4ff (150 Emeralds)
  - Segment 8: #ffcc00 (250 Emeralds)

Pointer (Top center):
- Triangle shape
- Color: #ff3333 (red)
- Height: 24px
- Position: Top center of wheel

Animation on spin:
- Spin duration: 4-6 seconds (random per spin)
- Total rotations: 3-5 complete rotations
- Easing: cubic-bezier(0.25, 0.46, 0.45, 0.94) (ease-out)
- Final segment determined by weighted randomness

Result display:
- Segment glows when landing
- Pointer highlights the winning segment
- Show big number: "+500 EMERALDS!"
- Color matches segment
- Confetti animation (pixelated squares)
- Sound effect (optional)

Button states:
- Enabled: Ready to spin (green button)
- Disabled: Already spun (gray button + timer)
- Spinning: Not clickable (animated spinner)

Timer:
- Format: "Next spin in: 18h 23m 45s"
- Updates every second
- Red when < 1 hour remaining
- Position: Bottom of modal
```

---

### **6. MYSTERY BOX SCREEN (REWARDS TAB)**

**Layout:**

```
┌──────────────────────────────┐
│ MYSTERY BOXES                │
├──────────────────────────────┤
│                              │
│ UNOPENED (3)                 │
│ ┌──────────────┐             │
│ │     📦       │             │ ← Box with glow
│ │   RARE       │             │
│ │ [OPEN NOW]   │             │
│ └──────────────┘             │
│                              │
│ ┌──────────────┐ ┌───────┐   │
│ │     📦       │ │  📦   │   │
│ │   COMMON     │ │COMMON │   │
│ │ [OPEN NOW]   │ │[OPEN] │   │
│ └──────────────┘ └───────┘   │
│                              │
├──────────────────────────────┤
│ OPENED TODAY (7)             │
├──────────────────────────────┤
│ ✨ Purple Glow Effect        │ ← Item + rarity
│ ✓ 150 Emeralds              │
│ ✓ Rainbow badge             │
│                              │
└──────────────────────────────┘
```

**Box Design:**

```
Unopened Box:
┌──────────────┐
│  📦 RARITY   │
│              │
│              │ ← 3D perspective
│  [OPEN NOW]  │
└──────────────┘

Sizing:
- Small: 100×100px (COMMON)
- Medium: 140×140px (RARE)
- Large: 180×180px (LEGENDARY)

Styling:
- Background gradient based on rarity
- Pixel art border (2px)
- Glow effect (colored box-shadow)
- Hover: Scale up 1.05, glow increases

Rarity colors:
- COMMON: #b0b8c8 (gray)
- RARE: #00d4ff (blue)
- LEGENDARY: #ffcc00 (gold)
- MYTHIC: Rainbow gradient effect

Opening animation:
- 1. Box explodes into particles
- 2. Reward reveals with bounce
- 3. Confetti animation
- 4. Sound effect
- 5. Auto-close after 3 seconds or manual close

Opened box display:
- Show item icon
- Item name (14px bold)
- Rarity tag (11px)
- Check mark (✓ in green)
```

---

### **7. PROFILE SCREEN**

**Layout:**

```
┌──────────────────────────────┐
│ PROFILE                      │
├──────────────────────────────┤
│ [Avatar]  USERNAME           │ ← User info header
│ ⭐ Level 24                  │
│ 🔥 12-day streak             │
│                              │
├──────────────────────────────┤
│ STATS                        │
│ 2,450 XP  | 4,320 Emeralds  │
│ 156 Messages | 23 Achievements│
│ 18 Cosmetics | 95% Accuracy  │
│                              │
├──────────────────────────────┤
│ COSMETICS EQUIPPED           │
│ Username Color: Purple       │ ← Can change
│ Glow Effect: Blue            │
│ Border: Neon                 │
│ Badge: "Clash King"          │
│ Title: "The Tapper"          │
│ [CUSTOMIZE]                  │
│                              │
├──────────────────────────────┤
│ ACHIEVEMENTS (4/50)          │
│ 🏆 Speed Demon               │
│ ⚡ Clash Champion            │
│ 💎 Emerald Hoarder           │
│ [VIEW ALL]                   │
│                              │
├──────────────────────────────┤
│ [EDIT PROFILE] [SETTINGS]    │
└──────────────────────────────┘
```

**User Header:**

```
Layout:
- Avatar (64px circle) on left
- Name (20px bold) + level badge on right
- Streak counter below name

Avatar:
- Default: Pixelated silhouette
- Custom: Allows upload (square, 64×64px min)
- Border: 2px solid #00ff41
- Background: #1a2640

Level badge:
- Position: Top-right of avatar
- Shape: Pentagon (Minecraft-style)
- Content: Level number (bold 14px)
- Color: Gold (#ffcc00)
- Glow: Subtle shadow

Streak indicator:
- Format: "🔥 12-day streak"
- Color: #ffcc00
- Position: Below name
- Shows only if active
```

**Stats Grid:**

```
4 columns on desktop, 2 on mobile:
┌──────────────┬──────────────┐
│ 2,450 XP     │ 4,320 Embers │
│ [Total XP]   │ [Balance]    │
├──────────────┼──────────────┤
│ 156 Messages │ 23 Badges    │
│ [Sent]       │ [Unlocked]   │
└──────────────┴──────────────┘

Card style:
- Background: #1a2640
- Border: 1px solid #2a3550
- Padding: 16px
- Text center-aligned

Number: 28px bold, color based on type
- XP: #00ff41
- Emeralds: #ffcc00
- Messages: #00d4ff
- Badges: #b366ff
```

---

## **ANIMATIONS & INTERACTIONS**

### **Button Interactions**

```
Default button:
- Background: #00ff41
- Text: #0a0e27
- Border: 2px solid #00ff41

Hover:
- Background: #00cc33 (darker)
- Scale: 1.02
- Transition: 150ms ease-out
- Box-shadow: 0 0 12px rgba(0, 255, 65, 0.4)

Active/Pressed:
- Scale: 0.95
- Duration: 100ms
- Feedback: Haptic vibration (if available)

Disabled:
- Background: #4a5568
- Opacity: 0.6
- Cursor: not-allowed
- No hover effects
```

### **Loading States**

```
Spinner (pixelated loading indicator):
- SVG 24×24px
- Rotating square animation
- Color: #00ff41
- Speed: 1 rotation per 1 second
- Position: Center of screen or button

Skeleton loader:
- Placeholder boxes with pulsing effect
- Color: #2a3550 → #1a2640 (subtle pulse)
- Duration: 1.5 seconds per cycle

Progress bar:
- Height: 3px
- Color: #00ff41
- Gradient from left to right
- Animation: Smooth fill

Confetti animation:
- Pixelated squares (8×8px)
- Colors: Mix of theme colors
- Fall direction: Downward
- Duration: 2 seconds
- Quantity: 40-60 pieces
- Randomized velocity
```

### **Toast Notifications**

```
Position: Top-center or bottom-center
Duration: Auto-close after 4 seconds (unless error)

Types:

SUCCESS:
- Background: #00ff41 with 90% opacity
- Text: #0a0e27
- Icon: ✓
- Border: 2px solid #00ff41
- Example: "+150 Emeralds earned!"

ERROR:
- Background: #ff3333 with 90% opacity
- Text: #ffffff
- Icon: ✗
- Border: 2px solid #ff3333
- Example: "Failed to complete challenge. Try again."

INFO:
- Background: #00d4ff with 90% opacity
- Text: #0a0e27
- Icon: ℹ️
- Border: 2px solid #00d4ff

WARNING:
- Background: #ffcc00 with 90% opacity
- Text: #0a0e27
- Icon: ⚠️
- Border: 2px solid #ffcc00

Styling:
- Padding: 16px 24px
- Font: 14px bold
- Border-radius: 2px
- Box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3)
- Animation: Slide down from top + fade in (200ms)
- Exit: Fade out (150ms)

Stack multiple toasts:
- Max 3 visible at once
- Additional ones queue below
```

### **Transitions & Timing**

```
Page navigation:
- Fade out current: 150ms
- Fade in new: 200ms
- Delay: 50ms (slight overlap for smooth feel)

Modal/Dialog:
- Background fade: 200ms
- Modal slide up: 250ms ease-out
- Close: Reverse 200ms

List item entry:
- Fade + slide-right: 200ms
- Staggered delay: 20ms between items (max 10 items)

Hover effects:
- Scale: 150ms ease-out
- Color: 100ms ease-out

Click feedback:
- Scale transform: 100ms
- Instant response (no delay)
```

---

## **RESPONSIVE DESIGN**

### **Breakpoints**

```
Mobile (320px - 767px):
- Single column layout
- Full-width buttons
- Bottom navigation fixed
- 16px page padding
- Simplified cards

Tablet (768px - 1023px):
- 2-column grid for cards
- Side navigation (optional)
- Optimized spacing

Desktop (1024px+):
- 3-4 column layout
- Side navigation bar
- Wider max-content
- Hover states enabled

Testing devices:
- iPhone SE (375px)
- iPhone 14 (390px)
- iPad (768px)
- Desktop (1920px)
```

### **Mobile Optimizations**

```
Touch targets:
- Minimum 48×48px for buttons
- 8px padding around clickables
- Enough spacing to prevent mis-taps

Font sizes:
- Increase base font to 16px on mobile (prevent zoom)
- Headings scale proportionally

Layout:
- Stack vertically on mobile
- Full-width modals
- Bottom sheet for secondary actions

Performance:
- Lazy load images
- Defer non-critical JS
- Minimize animations on low-end devices

Viewport meta:
- width=device-width
- initial-scale=1
- viewport-fit=cover (for notches)
```

---

## **FEATURE-SPECIFIC UI FLOWS**

### **Flow 1: User Sends Message & Earns Reward**

```
1. User types message + taps SEND
2. Message appears immediately (optimistic UI)
3. "Sent" status shows (1 checkmark)
4. Floating number: "+10 XP" appears near bottom
5. Number animates upward + fades (1.5 seconds)
6. Server confirms → 2 checkmarks appear
7. Badge earned notification? Show toast: "Achievement: Chatter!"
8. If streak active → Multiply XP (visual indicator: 1.2x multiplier badge)
```

### **Flow 2: User Wins Clash Battle**

```
1. Clash timer counts down: 60s → 0s
2. Real-time score updates (opponent score visible)
3. Timer turns red at 10 seconds
4. At 0s: Game ends with flash animation
5. Winning screen appears:
   - "YOU WIN! 🎉"
   - Score display: "62 vs 48"
   - Reward box animates in: "+200 Emeralds"
   - Mystery box unlocks with floating animation
6. Buttons: [Play Again] [Back]
7. Sound effect plays (if enabled)
8. Confetti animation (2 seconds)
```

### **Flow 3: User Spins Wheel & Gets Rare Reward**

```
1. Spin button clicked
2. Wheel rotates smoothly (4-6 seconds)
3. Pointer highlights segments as wheel spins
4. Wheel decelerates (ease-out animation)
5. Final segment glows
6. Wheel stops (snappy, no bounce)
7. Result popup appears:
   - "+1000 EMERALDS!" (huge text)
   - Color matches segment (#ffcc00 for legendary)
   - Confetti explodes from center (200 pieces)
   - Score floating upward
8. Sound effect (triumphant)
9. Auto-close after 3 seconds
10. Balance updates in top bar with animated number change
```

### **Flow 4: User Unlocks Achievement**

```
1. Condition met (e.g., reach level 10)
2. Screen fades slightly
3. Modal pops with celebration:
   - "🏆 ACHIEVEMENT UNLOCKED"
   - "Emerald Hoarder"
   - "Collect 1000 Emeralds"
   - Glow animation around badge
   - Particle effects
4. Sound: Ding (optional)
5. Confetti animation
6. Button: [Awesome!] or auto-close in 5s
7. Badge appears in profile immediately
```

---

## **REAL-TIME UPDATES**

### **WebSocket Integration Points**

```
Events to sync in real-time:

1. LEADERBOARD_UPDATE
   - User's rank changes
   - Toast: "↑ You're now #5!"
   - Leaderboard refreshes
   - Animation: User row highlights + bounces

2. STREAK_MILESTONE
   - Reached 7-day, 14-day, 30-day streak
   - Toast: "🔥 30-day Streak!"
   - Confetti + sound

3. CHALLENGE_COMPLETE
   - Other user completes challenge in room
   - Quick notification: "Player_X earned 200 Emeralds"
   - Auto-refreshes leaderboard

4. MESSAGE_REACTION
   - Someone reacts to your message
   - Reaction count updates live
   - Animation: Number pulses

5. FRIEND_ACTIVITY
   - Friend comes online
   - Friend completes challenge
   - Notification badge on profile tab

6. REWARD_EARNED
   - Real-time emerald updates
   - Animated number change in top bar
   - Never shows stale balance

Reconnection logic:
- Show "Connecting..." banner if disconnected
- Auto-reconnect every 5 seconds
- Catch up on missed events
- No data loss
```

---

## **ERROR HANDLING & EDGE CASES**

### **Error States**

```
Network Error:
┌──────────────────────────────┐
│ ⚠️ CONNECTION LOST            │
│                              │
│ Unable to reach server.       │
│ Check your internet.          │
│                              │
│    [RETRY] [OFFLINE MODE]    │
└──────────────────────────────┘

Challenge Failed:
│ ❌ CHALLENGE FAILED           │
│ You scored: 0 points         │
│ Try again in 15 minutes      │
│    [TRY AGAIN]               │

Loading timeout:
│ ⏱️ TAKING TOO LONG...         │
│ Reload page?                 │
│    [RELOAD]                  │

Permission denied:
│ 🔒 ACCESS DENIED              │
│ You don't have permission    │
│ to join this room.           │

Styling (all errors):
- Background: #ff3333 with 20% opacity
- Border: 2px solid #ff3333
- Text: white
- Icon: 24px
- Padding: 24px
- Border-radius: 2px
```

### **Empty States**

```
No messages:
┌──────────────────────────────┐
│                              │
│         👋 Start Chat        │
│                              │
│  Be the first to message in  │
│  this room!                  │
│                              │
│     [Send a message]         │
│                              │
└──────────────────────────────┘

No achievements:
│         🏆 No Achievements   │
│                              │
│  Complete challenges to      │
│  unlock achievements!        │
│                              │
│  [VIEW CHALLENGES]           │

No leaderboard (yet):
│      📊 Leaderboard Loading  │
│                              │
│  [Spinning animation]        │
│                              │
│  Fetching rankings...        │

Styling:
- Icon: 64px, gray (#b0b8c8)
- Text: 18px, bold, gray
- Subtext: 14px, light gray
- Padding: 48px top/bottom
- Center aligned
```

---

## **ACCESSIBILITY REQUIREMENTS**

```
Colors:
- Ensure 4.5:1 contrast ratio for text
- Don't rely on color alone for meaning
- Use patterns/icons in addition to colors

Text:
- Minimum 14px font size for body text
- Clear, simple language (no jargon)
- Max line length: 70 characters

Keyboard navigation:
- Tab order: Logical (left-to-right, top-to-bottom)
- Focus visible: 2px solid outline (#00ff41)
- All buttons/inputs accessible via keyboard

Aria labels:
- Buttons: aria-label="Spin Wheel"
- Icons: aria-hidden="true" for decorative
- Form inputs: associated labels
- Live regions: aria-live="polite" for updates

Mobile accessibility:
- Minimum 48×48px touch targets
- Sufficient padding around elements
- Clear focus states

Testing:
- Use axe DevTools for automated checks
- Manual testing with screen readers
- Keyboard-only navigation test
```

---

## **PERFORMANCE REQUIREMENTS**

```
Page Load:
- First Contentful Paint (FCP): < 2 seconds
- Largest Contentful Paint (LCP): < 3 seconds
- Cumulative Layout Shift (CLS): < 0.1

Interactions:
- Button click response: < 100ms
- Scroll smoothness: 60 FPS
- Animation smoothness: 60 FPS
- Modal open: < 200ms

Data:
- Message send: < 500ms
- Challenge submit: < 800ms
- Leaderboard refresh: < 1 second
- Spin wheel animation: Consistent 4-6 seconds

Bundle size:
- Initial JS: < 150KB (gzipped)
- CSS: < 30KB (gzipped)
- Images: Lazy load, WebP format
- Dependencies: Minimize third-party libs

Optimization:
- Code splitting by route
- Image optimization (next/image)
- CSS-in-JS minimal
- Debounce user input events
- Memoize expensive computations
```

---

## **TECHNICAL IMPLEMENTATION GUIDE**

### **Architecture**

```
Frontend Structure:

/src
  /components
    /Chat
      - MessageList.jsx (scrollable with virtualization)
      - MessageBubble.jsx (with reactions)
      - InputBox.jsx (with emoji picker)
      - QuickActionButtons.jsx (fixed bottom)
    /Challenges
      - ChallengeCard.jsx
      - ClashBattle.jsx (real-time canvas/div-based)
      - ClashUI.jsx
    /Rewards
      - SpinWheel.jsx (SVG animation)
      - MysteryBox.jsx
      - MysteryBoxOpening.jsx
    /Leaderboard
      - LeaderboardEntry.jsx
      - LeaderboardList.jsx
      - LeaderboardFilters.jsx
    /Profile
      - ProfileHeader.jsx
      - StatsGrid.jsx
      - CosmeticsEquipped.jsx
      - AchievementList.jsx
    /Common
      - Navigation.jsx (bottom nav bar)
      - Toast.jsx (notifications)
      - Modal.jsx (generic)
      - Loading.jsx (spinner)
      - ErrorBoundary.jsx

  /hooks
    - useWebSocket.js (real-time updates)
    - useLeaderboard.js (fetch + cache)
    - useUserStats.js (user data)
    - useAnimation.js (shared animations)

  /utils
    - constants.js (colors, sizes, animations)
    - animations.js (shared keyframes)
    - format.js (number/time formatting)
    - validation.js (input validation)

  /styles
    - global.css (Minecraft font, color vars)
    - animations.css (all animations)
    - responsive.css (media queries)

  /api
    - client.js (axios instance)
    - challenges.js (challenge endpoints)
    - leaderboard.js (leaderboard endpoints)
    - rewards.js (spin, boxes, etc)
    - chat.js (messages)

State management:
- React Context for user data
- Zustand or Redux for global state
- React Query for server state
```

### **Key Libraries**

```
animations:
- Framer Motion (smooth animations, spring physics)
- React Spring (alternative to Framer)

utilities:
- axios (HTTP client)
- date-fns (date formatting)
- zustand (state management)

WebSocket:
- Socket.io-client (real-time updates)

SVG:
- react-svg (SVG components)
- or raw SVG inline

Validation:
- Zod or Yup (input validation)

Dev tools:
- Vite (fast build)
- ESLint + Prettier (code quality)
- Vitest (unit tests)
```

### **CSS Variables (Theme System)**

```css
:root {
  /* Colors */
  --color-bg-dark: #0a0e27;
  --color-bg-grid: #121830;
  --color-accent-green: #00ff41;
  --color-accent-blue: #00d4ff;
  --color-accent-gold: #ffcc00;
  --color-accent-red: #ff3333;
  --color-accent-purple: #b366ff;
  
  --color-text-primary: #ffffff;
  --color-text-secondary: #b0b8c8;
  --color-text-disabled: #4a5568;
  
  --color-border-default: #2a3550;
  --color-border-hover: #4a6590;
  
  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  
  /* Typography */
  --font-family-primary: 'Minecraftia', monospace;
  --font-size-h1: 32px;
  --font-size-body: 14px;
  --font-weight-bold: 700;
  
  /* Animations */
  --duration-fast: 150ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --easing-out: cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
```

### **Animation Examples**

```javascript
// Floating number animation
const floatingNumberVariants = {
  initial: { y: 0, opacity: 1 },
  animate: { y: -40, opacity: 0 },
  transition: { duration: 1.5 }
};

// Pulse effect
const pulseVariants = {
  animate: {
    scale: [1, 1.1, 1],
    transition: { duration: 1.5, repeat: Infinity }
  }
};

// Slide-in modal
const modalVariants = {
  initial: { y: 50, opacity: 0 },
  animate: { y: 0, opacity: 1 },
  exit: { y: 50, opacity: 0 },
  transition: { duration: 0.25 }
};

// Confetti particle
const confettiVariants = {
  initial: { y: 0, opacity: 1, rotate: 0 },
  animate: {
    y: [0, Math.random() * 300 - 150],
    opacity: [1, 0],
    rotate: 360,
    transition: { duration: 2 }
  }
};
```

---

## **TESTING CHECKLIST**

```
Functionality:
☐ All buttons clickable and functional
☐ WebSocket real-time updates working
☐ Leaderboard refreshes correctly
☐ Rewards calculate accurately
☐ Cosmetics apply correctly
☐ Streak tracking working

UI/UX:
☐ Responsive on all screen sizes
☐ Animations smooth (60 FPS)
☐ No layout shifts
☐ Focus states visible
☐ Hover states working
☐ Touch-friendly spacing

Performance:
☐ Page loads < 2 seconds
☐ Interactions responsive (< 100ms)
☐ Memory leaks checked
☐ Unused code removed
☐ Images optimized

Browser compatibility:
☐ Chrome (latest)
☐ Firefox (latest)
☐ Safari (latest)
☐ Mobile Safari (iOS)
☐ Chrome Mobile (Android)

Accessibility:
☐ Keyboard navigation works
☐ Screen reader compatible
☐ Color contrast sufficient
☐ Focus visible everywhere
☐ No WCAG violations

Error handling:
☐ Network errors handled
☐ Input validation working
☐ Error messages clear
☐ Offline mode graceful
☐ Timeouts handled
```

---

## **DEPLOYMENT & MONITORING**

```
Frontend deployment:
- Vercel or Netlify (auto-deploy from GitHub)
- Environment variables for API URLs
- Source maps uploaded for error tracking

Monitoring:
- Sentry for error tracking
- Google Analytics for user behavior
- Performance monitoring (Web Vitals)
- Real-time error alerts

Analytics events to track:
- Page views
- Button clicks (Spin, Clash, etc)
- Challenge completions
- Leaderboard views
- Cosmetic purchases
- User retention metrics

CI/CD pipeline:
- Run tests on every commit
- Automated browser testing
- Lighthouse performance checks
- Deploy to staging first
- Manual approval for production
```

---

## **ADDITIONAL CONSIDERATIONS**

### **Dark/Light Theme**
```
Currently: Dark theme only (fits Minecraft aesthetic)
Future: Add light mode toggle if needed
- Invert colors while maintaining contrast
- Keep Minecraft pixel aesthetic
```

### **Internationalization**
```
Currently: English only
Setup i18n framework (i18next) for future languages
- All text in constants files
- No hardcoded strings
- RTL-ready layouts (if adding Arabic, Hebrew, etc)
```

### **Future Features**
```
Phase 2:
- Friend system (add friends, private chats)
- Crew/Group rankings
- Trading cosmetics
- Seasonal battle pass
- Voice/video calls

Phase 3:
- Mobile app (React Native)
- Desktop app (Electron)
- Streaming integration (Twitch overlay)
- Esports tournament mode
```

---

## **SUMMARY**

This specification provides a complete, production-ready UI/UX design for the GRIND chat application. The design prioritizes:

1. **Pixel-perfect Minecraft aesthetic** without sacrificing modern UX
2. **Addictive gamification mechanics** with clear visual feedback
3. **Mobile-first responsive design** for seamless experience
4. **Real-time WebSocket integration** for live updates
5. **Smooth 60 FPS animations** for buttery interactions
6. **Accessibility-first approach** for all users
7. **Performance optimization** for fast load times

Implementation should follow this specification precisely while maintaining flexibility for bug fixes and minor refinements based on user testing.
