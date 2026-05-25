# Higgsfield CLI — Cost Calculator (May 2026)

## Image Models

| Model | ID | Cost | Best For |
|-------|-----|-----:|:---------|
| Z Image | `z_image` | **0.15** | Cheapest test runs, drafts |
| Nano Banana | `nano_banana` | **1** | Fast product shots, good quality |
| FLUX.2 | `flux_2` | **1** | Artistic, stylized images |
| Grok Image | `grok_image` | **1** | General purpose |
| Seedream 4.5 | `seedream_v4_5` | **1** | High quality, realistic |
| Seedream V5 Lite | `seedream_v5_lite` | **1** | Newer Seedream, balanced |
| Nano Banana 2 | `nano_banana_flash` | **1.5** | Faster Nano Banana variant |
| Flux Kontext | `flux_kontext` | **1.5** | Style transfer, reference-based |
| **Nano Banana Pro** | `nano_banana_2` | **2** | **Best overall — 4K, text, product photos** |
| Cinematic Studio 2.5 | `cinematic_studio_2_5` | **2** | Cinematic stills, dramatic lighting |
| Image Auto | `image_auto` | **2** | Auto-selects best model |
| **GPT Image 2** | `gpt_image_2` | **7** | Highest quality, complex scenes |

### Budget Packs (Images Only)

| Budget | Z Image | Nano Banana | Nano Banana Pro | GPT Image 2 |
|-------:|--------:|------------:|----------------:|------------:|
| 10 cr | 66 imgs | 10 imgs | 5 imgs | 1 img |
| 50 cr | 333 imgs | 50 imgs | 25 imgs | 7 imgs |
| 150 cr | 1000 imgs | 150 imgs | 75 imgs | 21 imgs |
| 500 cr | 3333 imgs | 500 imgs | 250 imgs | 71 imgs |

---

## Video Models

| Model | ID | 5s | 10s | Notes |
|-------|-----|---:|----:|:------|
| Seedance 1.5 Pro | `seedance1_5` | 4.8 (4s) | 9.6 (8s) | Durations: 4/8/12s only |
| Veo 3.1 Lite | `veo3_1_lite` | 4 (4s) | — | Durations: 4/6/8s |
| Minimax Hailuo | `minimax_hailuo` | — | 11 (10s) | Durations: 6/10s only |
| Cinematic Studio Video V2 | `cinematic_studio_video_v2` | **7.5** | **15** | Great value for cinematic |
| Wan 2.7 | `wan2_7` | **7.5** | **15** | Newest Wan, good value |
| Grok Video | `grok_video` | **7.5** | **15** | General purpose video |
| Cinematic Studio Video | `cinematic_studio_video` | 8 | 18 | Older version |
| Kling 2.6 | `kling2_6` | **10** | **20** | Multi-shot, audio support |
| **Kling 3.0** | `kling3_0` | **10** | **20** | **Best value — audio, 4K mode** |
| Veo 3.1 | `veo3_1` | 11 (4s) | 22 (8s) | Google, durations: 4/6/8s |
| **Seedance 2.0** | `seedance_2_0` | **22.5** | **45** | **Best quality, identity-faithful** |
| Cinematic Studio 3.0 | `cinematic_studio_3_0` | **25** | **50** | Premium cinematic |
| Wan 2.6 | `wan2_6` | 13 | 25 | Older Wan |

### Budget Packs (Video Only — 5s clips)

| Budget | CS Video V2 | Kling 3.0 | Seedance 2.0 | CS 3.0 |
|-------:|------------:|----------:|-------------:|-------:|
| 50 cr | 6 videos | 5 videos | 2 videos | 2 videos |
| 150 cr | 20 videos | 15 videos | 6 videos | 6 videos |
| 500 cr | 66 videos | 50 videos | 22 videos | 20 videos |

---

## Recommended Combos by Use Case

### Landing Page (like the Brewline demo)
| Asset | Model | Count | Credits |
|-------|-------|------:|--------:|
| Hero image | nano_banana_2 | 1 | 2 |
| Product shots | nano_banana_2 | 4 | 8 |
| Lifestyle images | gpt_image_2 | 2 | 14 |
| Feature close-ups | nano_banana_2 | 3 | 6 |
| Colorways | nano_banana_2 | 3 | 6 |
| Hero video loop | seedance_2_0 5s | 1 | 23 |
| **Total** | | **14 assets** | **~59 cr** |

### Affiliate Marketing (TikTok/Pinterest)
| Asset | Model | Count | Credits |
|-------|-------|------:|--------:|
| Product hero | nano_banana_2 | 2 | 4 |
| UGC video | seedance_2_0 5s | 1 | 23 |
| Cinematic ad | cinematic_studio_3_0 5s | 1 | 25 |
| Pinterest pin images | nano_banana_2 | 4 | 8 |
| **Total** | | **8 assets** | **~60 cr** |

### Social Media Content Pack
| Asset | Model | Count | Credits |
|-------|-------|------:|--------:|
| Instagram posts | nano_banana_2 (1:1) | 5 | 10 |
| Reels/TikTok videos | kling3_0 (9:16) 5s | 3 | 30 |
| Story images | seedream_v4_5 (9:16) | 3 | 3 |
| YouTube thumbnail | gpt_image_2 (16:9) | 1 | 7 |
| **Total** | | **12 assets** | **~50 cr** |

### Budget-Conscious Starter
| Asset | Model | Count | Credits |
|-------|-------|------:|--------:|
| Product images | z_image | 10 | 1.5 |
| Hero shots | nano_banana | 5 | 5 |
| One video | cinematic_studio_video_v2 5s | 1 | 7.5 |
| **Total** | | **16 assets** | **~14 cr** |

---

## CLI Quick Reference

```bash
# Check balance
higgsfield account status

# Cost estimate (always run first!)
higgsfield generate cost <model> --prompt "..." [--params]

# Generate image
higgsfield generate create nano_banana_2 --prompt "..." --aspect_ratio 16:9 --resolution 2k --wait

# Generate video
higgsfield generate create seedance_2_0 --prompt "..." --aspect_ratio 9:16 --duration 5 --wait

# List past generations
higgsfield generate list --size 20

# Upload local image for img2img
higgsfield upload create --file ./photo.jpg
```
