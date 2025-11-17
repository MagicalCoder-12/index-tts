# IndexTTS2 Deployment Guide

This guide covers deploying IndexTTS2 in production environments, including containerization and cloud deployment options.

## Table of Contents

1. [Docker Deployment](#docker-deployment)
2. [Inference Server](#inference-server)
3. [Cloud Platforms](#cloud-platforms)
4. [Performance Optimization](#performance-optimization)
5. [Monitoring](#monitoring)

## Docker Deployment

### Building a Docker Image

A Dockerfile is available for containerized deployment:

```bash
docker build -t indextts2:latest .
```

### Running with Docker

```bash
# Basic inference
docker run --gpus all -v $(pwd)/outputs:/app/outputs indextts2:latest

# With WebUI
docker run --gpus all -p 7860:7860 indextts2:latest uv run webui.py --listen 0.0.0.0
```

### Docker Compose

For production deployments with multiple services:

```yaml
version: '3.8'
services:
  indextts:
    image: indextts2:latest
    container_name: indextts-inference
    ports:
      - "7860:7860"
    volumes:
      - ./checkpoints:/app/checkpoints
      - ./outputs:/app/outputs
    environment:
      - CUDA_VISIBLE_DEVICES=0
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## Inference Server

### FastAPI Server Setup

Create a `server.py` for API-based inference:

```python
from fastapi import FastAPI, File, UploadFile
from indextts.infer_v2 import IndexTTS2
import tempfile
import os

app = FastAPI(title="IndexTTS2 API")
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints", use_fp16=True)

@app.post("/synthesize")
async def synthesize(
    text: str,
    voice_file: UploadFile = File(...),
    emotion: str = None
):
    """Synthesize speech from text with voice cloning"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        contents = await voice_file.read()
        tmp.write(contents)
        tmp.flush()
        
        try:
            output_path = "output.wav"
            tts.infer(
                spk_audio_prompt=tmp.name,
                text=text,
                output_path=output_path,
                verbose=False
            )
            return {"status": "success", "output": output_path}
        finally:
            os.unlink(tmp.name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run the server:

```bash
uv run server.py
```

### Using the API

```bash
curl -X POST "http://localhost:8000/synthesize" \
  -F "text=Hello, this is a test" \
  -F "voice_file=@reference.wav"
```

## Cloud Platforms

### AWS Deployment

**Using AWS SageMaker:**

```bash
# Create SageMaker instance
aws sagemaker create-notebook-instance \
  --notebook-instance-name indextts2 \
  --instance-type ml.p3.2xlarge \
  --role-arn <your-iam-role>

# Clone and setup on the instance
git clone https://github.com/index-tts/index-tts.git
cd index-tts
git lfs pull
pip install -U uv
uv sync --all-extras
```

### Google Cloud Platform

**Using Vertex AI:**

1. Create a Compute Engine instance with GPU:
   ```bash
   gcloud compute instances create indextts2 \
     --zone=us-central1-a \
     --machine-type=n1-highmem-8 \
     --accelerator=type=nvidia-tesla-v100,count=1
   ```

2. SSH into the instance and follow the INSTALL.md guide

### Azure Deployment

**Using Azure Container Instances:**

```bash
az container create \
  --resource-group myResourceGroup \
  --name indextts2 \
  --image indextts2:latest \
  --gpu 1 \
  --ports 7860
```

## Performance Optimization

### GPU Memory Management

For low-VRAM systems, use FP16 inference:

```python
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=True,  # Enable half-precision
    use_deepspeed=False  # Disable if unstable
)
```

### Model Quantization

For faster inference on limited hardware:

```bash
# Export to ONNX (requires onnx and onnx-simplifier)
python -m indextts.export_onnx \
  --model_dir checkpoints \
  --output_dir onnx_models
```

### Batch Processing

For multiple synthesis requests:

```python
texts = ["Hello", "World", "Test"]
audio_refs = ["ref1.wav", "ref2.wav", "ref3.wav"]

for text, ref in zip(texts, audio_refs):
    tts.infer(
        spk_audio_prompt=ref,
        text=text,
        output_path=f"output_{texts.index(text)}.wav"
    )
```

### Caching

Implement caching for repeated requests:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def synthesize_with_cache(text: str, voice_ref: str) -> str:
    output = f"cache/{hash((text, voice_ref))}.wav"
    if not os.path.exists(output):
        tts.infer(spk_audio_prompt=voice_ref, text=text, output_path=output)
    return output
```

## Monitoring

### Logging

Configure logging for production:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('indextts.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks

Implement health check endpoints:

```python
@app.get("/health")
async def health():
    try:
        # Verify model is loaded
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 503
```

### Metrics Collection

Use Prometheus for metrics:

```python
from prometheus_client import Counter, Histogram

inference_counter = Counter('indextts_inferences_total', 'Total inferences')
inference_duration = Histogram('indextts_inference_duration_seconds', 'Inference time')

@inference_duration.time()
def infer_with_metrics(*args, **kwargs):
    inference_counter.inc()
    return tts.infer(*args, **kwargs)
```

## Environment Variables

Key environment variables for deployment:

```bash
# Model paths
INDEXTTS_MODEL_DIR=/path/to/models
INDEXTTS_CONFIG_PATH=/path/to/config.yaml

# Performance
CUDA_VISIBLE_DEVICES=0
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/indextts.log

# API
API_HOST=0.0.0.0
API_PORT=8000

# Features
USE_FP16=True
USE_DEEPSPEED=False
```

## Troubleshooting

### Out of Memory

1. Enable FP16 inference
2. Reduce batch size
3. Use gradient checkpointing
4. Increase GPU memory allocation:
   ```bash
   export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
   ```

### Slow Inference

1. Check GPU utilization: `nvidia-smi`
2. Enable CUDA kernels for vocoder
3. Use mixed precision (FP16)
4. Profile with PyTorch profiler

### Model Not Loading

1. Verify Git LFS files are downloaded: `git lfs ls-files`
2. Check checkpoint paths
3. Ensure correct Python/PyTorch versions
4. Review logs for detailed errors

## Security Considerations

1. **API Authentication**: Add authentication middleware for public APIs
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Input Validation**: Validate all user inputs
4. **File Uploads**: Restrict file types and sizes
5. **HTTPS**: Always use HTTPS in production
6. **Secrets Management**: Use environment variables for sensitive data

## Backup and Recovery

```bash
# Backup configuration and models
tar -czf indextts-backup.tar.gz checkpoints/ config.yaml

# Restore from backup
tar -xzf indextts-backup.tar.gz
```

## Support

- **Documentation**: See [README.md](README.md) and [INSTALL.md](INSTALL.md)
- **Issues**: [GitHub Issues](https://github.com/index-tts/index-tts/issues)
- **Community**: [Discord](https://discord.gg/uT32E7KDmy)
