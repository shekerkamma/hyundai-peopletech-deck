# Higgsfield CLI — Prompt Library

Pre-written, copy-paste prompts for every major model. Each prompt includes the exact CLI command.

---

## Nano Banana Pro (`nano_banana_2`) — 2 cr/image

Best for: Product photography, 4K renders, text on images, diagrams.

### Product Hero Shot (16:9)
```bash
higgsfield generate create nano_banana_2 \
  --prompt "Professional product photography of a sleek minimalist espresso machine on a marble counter. Matte ceramic body with brushed brass dial. Soft studio lighting from camera-left, warm oak surface, clean neutral background. Shot on Phase One IQ4 150MP, f/2.8, shallow depth of field. Premium commercial photography aesthetic." \
  --aspect_ratio 16:9 --resolution 4k --wait
```

### Product on White (1:1)
```bash
higgsfield generate create nano_banana_2 \
  --prompt "Clean product shot of a premium espresso machine centered on pure white background. Soft even studio lighting, no shadows, e-commerce style. High detail on ceramic texture and brass accents. Product photography for web catalog." \
  --aspect_ratio 1:1 --resolution 2k --wait
```

### Feature Close-Up (1:1)
```bash
higgsfield generate create nano_banana_2 \
  --prompt "Extreme close-up macro shot of a brushed brass dial on a matte ceramic surface. Warm studio lighting catching the metallic texture. Shallow depth of field, bokeh background. Detail-oriented product photography." \
  --aspect_ratio 1:1 --resolution 4k --wait
```

### Flat Lay (1:1)
```bash
higgsfield generate create nano_banana_2 \
  --prompt "Overhead flat lay of artisan coffee setup: espresso machine, ceramic cup, whole coffee beans scattered on oak surface, linen napkin, small succulent plant. Warm natural lighting, Instagram aesthetic. Clean composition, negative space for text overlay." \
  --aspect_ratio 1:1 --resolution 2k --wait
```

### Pinterest Pin (2:3)
```bash
higgsfield generate create nano_banana_2 \
  --prompt "Aesthetic kitchen counter scene with premium espresso machine as hero. Morning light through window, fresh croissant on plate, steaming cup of espresso. Warm cream and brown tones, cozy Scandinavian minimal style. Pinterest-worthy vertical composition with space at top for text overlay." \
  --aspect_ratio 2:3 --resolution 2k --wait
```

### With Text Overlay (16:9)
```bash
higgsfield generate create nano_banana_2 \
  --prompt "Marketing banner for premium espresso machine brand. Left side: product on dark background with dramatic rim lighting. Right side: clean space with text 'BREWLINE' in elegant serif font and 'Espresso, Refined.' below in sans-serif. Luxury brand aesthetic, dark moody color palette with gold accents." \
  --aspect_ratio 16:9 --resolution 4k --wait
```

---

## GPT Image 2 (`gpt_image_2`) — 7 cr/image

Best for: Complex scenes, people, lifestyle photography, highest realism.

### Lifestyle Scene (16:9)
```bash
higgsfield generate create gpt_image_2 \
  --prompt "A woman in her 30s in a cozy linen robe making espresso in a bright, modern Scandinavian kitchen. Morning golden hour light streaming through large windows. She's smiling while steaming milk with a premium matte ceramic espresso machine. White oak cabinets, marble counters, monstera plant in corner. Warm, aspirational lifestyle photography." \
  --aspect_ratio 16:9 --quality high --resolution 2k --wait
```

### UGC-Style Product Review (9:16)
```bash
higgsfield generate create gpt_image_2 \
  --prompt "Selfie-style photo of a young woman holding a cup of espresso, looking directly at camera with genuine excitement. Premium espresso machine visible on counter behind her. Bright kitchen, natural lighting. Authentic UGC aesthetic — slightly imperfect framing, real and relatable. Instagram story vibe." \
  --aspect_ratio 9:16 --quality high --wait
```

### Before/After Split (16:9)
```bash
higgsfield generate create gpt_image_2 \
  --prompt "Split image comparison: Left side shows a cluttered messy kitchen counter with cheap drip coffee maker, harsh fluorescent lighting, disorganized mugs — labeled 'Before'. Right side shows the same counter beautifully organized with premium matte ceramic espresso machine, warm lighting, fresh flowers, clean aesthetic — labeled 'After'. Dramatic transformation reveal for social media." \
  --aspect_ratio 16:9 --quality high --wait
```

---

## Flux Kontext (`flux_kontext`) — 1.5 cr/image

Best for: Style transfer, editing existing images, reference-based generation.

### Style Transfer
```bash
# First upload your reference image
higgsfield upload create --file ./my-product.jpg
# Then use the upload ID:
higgsfield generate create flux_kontext \
  --prompt "Transform this product photo into a warm, moody editorial style. Add dramatic side-lighting, dark background, and golden tones. Keep the product exactly the same but change the mood to luxury magazine aesthetic." \
  --input_images <upload_id> --wait
```

---

## Seedance 2.0 (`seedance_2_0`) — 22.5 cr/5s

Best for: Highest quality video, identity-faithful, reference-driven.

### UGC Skincare Demo (9:16)
```bash
higgsfield generate create seedance_2_0 \
  --prompt "Realistic UGC-style video of a woman in her mid-20s in a bright clean bathroom applying glowing serum from a dropper onto her cheek, gently patting it in. Her skin visibly catches the light with a dewy glass-like finish. Korean skincare bottles arranged neatly on counter. Soft morning light from frosted window. Authentic, not overly produced." \
  --aspect_ratio 9:16 --duration 5 --wait
```

### Product Hero Loop (16:9)
```bash
higgsfield generate create seedance_2_0 \
  --prompt "Cinematic loop of espresso pouring from a premium matte ceramic machine into a clear glass cup. Rich golden-brown crema forming on top. Steam rising gently. Warm studio lighting on dark background. Shallow depth of field. Smooth, satisfying pour motion. Perfect for website hero background video." \
  --aspect_ratio 16:9 --duration 5 --wait
```

### Cinematic Product Reveal (16:9)
```bash
higgsfield generate create seedance_2_0 \
  --prompt "Cinematic product reveal: camera slowly dollies in toward a premium espresso machine on a marble pedestal. Dramatic side-lighting creates long shadows. Golden bokeh particles float in the air. The brass dial catches a glint of light. Luxury brand commercial aesthetic. Slow, deliberate camera movement." \
  --aspect_ratio 16:9 --duration 10 --genre epic --wait
```

---

## Kling 3.0 (`kling3_0`) — 10 cr/5s

Best for: Best value video, multi-shot, built-in audio, 4K mode.

### Product Demo with Audio (16:9)
```bash
higgsfield generate create kling3_0 \
  --prompt "Hands-on demonstration of premium espresso machine. A person turns the brass dial, the machine whirs to life, espresso pours into a cup with satisfying crema. Sound of grinding, steaming, and pouring. Clean kitchen counter, warm lighting." \
  --aspect_ratio 16:9 --duration 5 --sound on --wait
```

### TikTok Vertical (9:16)
```bash
higgsfield generate create kling3_0 \
  --prompt "POV selfie-style video: person picks up their morning espresso from a sleek ceramic machine, takes a sip, and gives a satisfied nod to camera. Bright modern kitchen, morning light. Casual, authentic UGC feel." \
  --aspect_ratio 9:16 --duration 5 --sound on --wait
```

---

## Cinematic Studio 3.0 (`cinematic_studio_3_0`) — 25 cr/5s

Best for: Premium cinematic ads, dramatic lighting, film-quality.

### Brand Film Opening (16:9)
```bash
higgsfield generate create cinematic_studio_3_0 \
  --prompt "Opening shot of a luxury coffee brand film. Dawn light breaks through floor-to-ceiling windows of a minimalist loft apartment. Camera slowly reveals a premium espresso machine on a concrete island counter. A person's hand enters frame and presses the brass dial. Rich, cinematic color grading — warm highlights, cool shadows. Anamorphic lens flare." \
  --aspect_ratio 16:9 --duration 5 --wait
```

---

## Budget-Friendly Options

### Z Image (`z_image`) — 0.15 cr/image
```bash
# Cheapest option — great for rapid prototyping
higgsfield generate create z_image \
  --prompt "Minimalist espresso machine product shot, white background, clean lighting" \
  --wait
```

### Cinematic Studio Video V2 (`cinematic_studio_video_v2`) — 7.5 cr/5s
```bash
# Best value for video
higgsfield generate create cinematic_studio_video_v2 \
  --prompt "Smooth cinematic shot of espresso being poured, warm lighting, shallow depth of field" \
  --aspect_ratio 16:9 --duration 5 --wait
```
