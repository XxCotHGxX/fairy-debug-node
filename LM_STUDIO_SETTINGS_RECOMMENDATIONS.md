# LM Studio Settings Recommendations for Fairy Debugger

## Your Hardware
- **CPU**: i9-14900K (24 cores - 8P + 16E)
- **GPU**: Intel A770 16GB
- **RAM**: 128GB DDR5

## Recommended Settings

### 1. **Context Length: 45000** ✅
- Keep at 45000 (good for code analysis)
- Model supports up to 262144, but 45000 is sufficient and faster
- Lower context = faster inference, less memory

### 2. **GPU Offload: 30-35 / 48** (Adjust based on model size)
- Your A770 has 16GB VRAM
- For a 30B model: Start with 30-35 layers
- For a 7B-13B model: Try 35-40 layers
- **Strategy**: Offload as much as possible to GPU, fall back to CPU

### 3. **CPU Thread Pool Size: 16-20**
- Your i9-14900K has 24 threads (8P + 16E)
- Set to 16-20 for optimal performance
- Leave some threads for system overhead
- Too high = thread contention, too low = underutilized CPU

### 4. **Evaluation Batch Size: 256-512** ✅
- Current 512 is fine
- Lower (256) = more consistent, slower
- Higher (512+) = faster but may use more memory
- 512 is a good balance

### 5. **RoPE Settings: Auto** ✅
- Keep both on "Auto" - model handles this automatically

### 6. **KV Cache Settings:**
- **Offload KV Cache to GPU Memory: ON** ✅
- Use GPU memory for KV cache when available
- Frees up RAM for other operations

### 7. **Memory Management:**
- **Keep Model in Memory: ON** ✅ (if you have enough RAM)
- **Try mmap(): ON** ✅
- mmap allows efficient memory-mapped file access

### 8. **Advanced Settings:**
- **Flash Attention: OFF** (usually better for NVIDIA, Intel GPUs may not support)
- **Seed: Random Seed** ✅ (good for diverse responses)

## Performance Tuning Strategy

### For Code Generation/Analysis (Your Use Case):

**Best Quality Settings:**
```
Context Length: 45000
GPU Offload: 30-35 layers
CPU Threads: 18
Batch Size: 512
KV Cache to GPU: ON
Keep Model in Memory: ON
mmap: ON
```

**Faster Inference (Lower Quality):**
```
Context Length: 30000
GPU Offload: 25-30 layers
CPU Threads: 20
Batch Size: 1024
KV Cache to GPU: ON
Keep Model in Memory: OFF (if running out of RAM)
```

## Intel Arc GPU Considerations

1. **GPU Offload**: Intel Arc GPUs work but may be slower than NVIDIA
   - Start conservative (30 layers), increase if stable
   - Monitor VRAM usage - don't exceed 14GB (leave 2GB buffer)

2. **Mixed Precision**: LM Studio should handle this automatically
   - If you see errors, reduce GPU offload layers

3. **Driver**: Make sure Intel Arc drivers are up to date
   - Check Intel Arc Control for GPU utilization

## Testing Recommendations

1. **Start with moderate settings** (30 GPU layers, 16 CPU threads)
2. **Run a test analysis** and monitor:
   - GPU utilization (should be 60-90%)
   - RAM usage (should be reasonable)
   - Generation speed (tokens/sec)
   - Response quality

3. **Adjust based on results:**
   - Slow but good quality → Increase GPU offload
   - Fast but poor quality → Decrease batch size, increase threads
   - GPU memory full → Decrease GPU offload layers
   - CPU bottleneck → Increase CPU threads (up to 20)

## Expected Performance

With your hardware, you should see:
- **30B models**: 5-15 tokens/sec (GPU offload dependent)
- **13B models**: 15-30 tokens/sec
- **7B models**: 30-50 tokens/sec

For code analysis (which is what Fairy Debugger does), quality > speed, so prioritize accuracy over throughput.

## Quick Start Config

```
Context Length: 45000
GPU Offload: 32
CPU Thread Pool: 18
Batch Size: 512
Offload KV Cache: ON
Keep Model in Memory: ON
mmap: ON
Flash Attention: OFF
```

Start here and adjust based on your model size and performance!

