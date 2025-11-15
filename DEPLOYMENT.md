# Deployment Guide - Deep Agent E2B

This guide covers deployment strategies, pipeline architecture, and production considerations for the Deep Agent E2B system.

## Deployment Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Deployment Architecture                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │   Client     │  (User/API/Scheduler)                     │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ├─── Interactive Mode ────┐                         │
│         │                         │                         │
│         ├─── Single Task Mode ────┤                         │
│         │                         │                         │
│         └─── Queue Mode ──────────┤                         │
│                                   │                         │
│                          ┌────────▼────────┐               │
│                          │   deploy.py     │               │
│                          │  (Orchestrator) │               │
│                          └────────┬────────┘               │
│                                   │                         │
│                          ┌────────▼────────┐               │
│                          │ DeepAgentServer │               │
│                          │   (Manager)     │               │
│                          └────────┬────────┘               │
│                                   │                         │
│                          ┌────────▼────────┐               │
│                          │  DeepAgentE2B    │               │
│                          │   (Core Agent)   │               │
│                          └────────┬────────┘               │
│                                   │                         │
│                    ┌──────────────┴──────────────┐         │
│                    │                             │         │
│            ┌───────▼──────┐            ┌────────▼──────┐  │
│            │ E2B Sandbox  │            │  File System  │  │
│            │   (Cloud)   │            │  (Queue/Logs) │  │
│            └──────────────┘            └───────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Modes

### Mode 1: Interactive Development

**Use Case**: Development, testing, one-off tasks

**Command:**
```bash
uv run main.py
```

**Characteristics:**
- Single process
- Interactive chat interface
- Sandbox created per session
- No persistence between sessions
- Best for: Development, debugging, exploration

**Flow:**
```
User Input → Agent → Sandbox → Results → User
```

### Mode 2: Single Task Execution

**Use Case**: One-off automation, scheduled tasks, CI/CD

**Command:**
```bash
uv run deploy.py task "Your task description"
```

**Characteristics:**
- Single process per task
- Sandbox created per task
- Task executed and process exits
- Logs written to `/tmp/deep_agent_logs/`
- Best for: Scheduled jobs, automation scripts

**Flow:**
```
Task → Agent → Sandbox → Results → Log → Exit
```

### Mode 3: Server Mode (Queue-Based)

**Use Case**: Production deployment, persistent service

**Start Server:**
```bash
uv run deploy.py server
```

**Add Tasks:**
```bash
uv run deploy.py queue "Task description"
```

**Characteristics:**
- Persistent process
- Polls queue every 10 seconds (configurable)
- Processes tasks sequentially
- Maintains agent instance
- Logs all operations
- Best for: Production, high-volume processing

**Flow:**
```
Server Start → Initialize Agent → Poll Queue
    ↓
Task Available? → Process Task → Log Results → Continue Polling
    ↓
No Tasks → Wait → Poll Again
```

## Pipeline Flow

### Complete Execution Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    Task Execution Pipeline                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Task Submission                                         │
│     ├─ Interactive: User types in terminal                  │
│     ├─ Single Task: Command line argument                  │
│     └─ Queue: Written to /tmp/deep_agent_queue.json        │
│                                                              │
│  2. Agent Initialization                                    │
│     ├─ Load environment variables                           │
│     ├─ Create E2B sandbox                                   │
│     │   ├─ Configure MCP servers (GitHub, Notion)          │
│     │   ├─ Set environment variables                       │
│     │   └─ Get sandbox ID                                  │
│     ├─ Configure Claude CLI in sandbox                      │
│     │   ├─ Get MCP gateway URL                              │
│     │   ├─ Get MCP token                                    │
│     │   └─ Run: claude mcp add ...                         │
│     ├─ Create E2B tools (LangChain)                        │
│     └─ Initialize deep agent                               │
│                                                              │
│  3. Task Processing                                         │
│     ├─ Agent receives task                                  │
│     ├─ Planning phase                                       │
│     │   ├─ Task decomposition (write_todos)                 │
│     │   └─ Step-by-step plan creation                      │
│     ├─ Execution phase                                      │
│     │   ├─ Tool selection                                   │
│     │   ├─ Tool execution                                  │
│     │   │   ├─ Sandbox commands                            │
│     │   │   ├─ File operations                             │
│     │   │   ├─ MCP actions (GitHub/Notion)                 │
│     │   │   └─ Package installation                        │
│     │   └─ Result collection                               │
│     └─ Synthesis phase                                      │
│         ├─ Result aggregation                               │
│         └─ Response generation                               │
│                                                              │
│  4. Result Handling                                         │
│     ├─ Interactive: Display to user                         │
│     ├─ Single Task: Print and exit                         │
│     └─ Server Mode: Log to file                            │
│                                                              │
│  5. Cleanup                                                 │
│     ├─ Close sandbox (or timeout)                          │
│     ├─ Save logs                                            │
│     └─ Update queue (if server mode)                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Server Mode Pipeline Detail

```
┌─────────────────────────────────────────────────────────────┐
│              Server Mode Detailed Pipeline                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  START                                                       │
│    │                                                         │
│    ├─> Initialize DeepAgentServer                           │
│    │   ├─ Create log directory                              │
│    │   ├─ Check queue file                                  │
│    │   └─ Set retry configuration                           │
│    │                                                         │
│    ├─> Initialize Agent (lazy)                              │
│    │   ├─ Create sandbox                                    │
│    │   ├─ Configure MCP                                     │
│    │   └─ Setup tools                                       │
│    │                                                         │
│    └─> Enter Main Loop                                      │
│        │                                                     │
│        ├─> Poll Queue (every 10s)                           │
│        │   └─> Read /tmp/deep_agent_queue.json             │
│        │                                                     │
│        ├─> Queue Empty?                                     │
│        │   ├─ Yes → Wait → Poll Again                      │
│        │   └─ No → Continue                                │
│        │                                                     │
│        ├─> Get First Task                                  │
│        │   └─> Remove from queue                           │
│        │                                                     │
│        ├─> Process Task                                     │
│        │   ├─> Ensure agent initialized                    │
│        │   ├─> Execute task                                │
│        │   ├─> Handle errors                               │
│        │   └─> Log results                                 │
│        │                                                     │
│        ├─> Save Updated Queue                               │
│        │                                                     │
│        └─> Continue Loop                                    │
│                                                              │
│  STOP (Ctrl+C or error)                                     │
│    ├─> Close agent                                          │
│    ├─> Close sandbox                                        │
│    └─> Exit                                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Production Deployment

### System Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4 GB
- Disk: 10 GB
- Network: Stable internet connection

**Recommended:**
- CPU: 4+ cores
- RAM: 8+ GB
- Disk: 50+ GB (for logs)
- Network: High-speed, reliable connection

### Process Management

#### Option 1: systemd (Linux)

Create `/etc/systemd/system/deep-agent.service`:

```ini
[Unit]
Description=Deep Agent E2B Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/e2b-mcp-py
Environment="PATH=/path/to/e2b-mcp-py/.venv/bin"
ExecStart=/path/to/e2b-mcp-py/.venv/bin/python deploy.py server
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits
LimitNOFILE=65536
MemoryMax=8G
CPUQuota=400%

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable deep-agent
sudo systemctl start deep-agent
sudo systemctl status deep-agent
```

#### Option 2: Supervisor

Create `/etc/supervisor/conf.d/deep-agent.conf`:

```ini
[program:deep-agent]
command=/path/to/e2b-mcp-py/.venv/bin/python deploy.py server
directory=/path/to/e2b-mcp-py
user=your-user
autostart=true
autorestart=true
stderr_logfile=/var/log/deep-agent/error.log
stdout_logfile=/var/log/deep-agent/output.log
environment=PATH="/path/to/e2b-mcp-py/.venv/bin"
```

Reload and start:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start deep-agent
```

#### Option 3: PM2 (Node.js process manager)

```bash
npm install -g pm2

# Create ecosystem file: ecosystem.config.js
pm2 start ecosystem.config.js
```

`ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: 'deep-agent',
    script: 'deploy.py',
    args: 'server',
    interpreter: '/path/to/e2b-mcp-py/.venv/bin/python',
    cwd: '/path/to/e2b-mcp-py',
    env: {
      PATH: '/path/to/e2b-mcp-py/.venv/bin'
    },
    autorestart: true,
    watch: false,
    max_memory_restart: '8G',
    error_file: '/var/log/deep-agent/error.log',
    out_file: '/var/log/deep-agent/output.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }]
};
```

### Log Management

#### Log Rotation

Create `/etc/logrotate.d/deep-agent`:

```
/tmp/deep_agent_logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 your-user your-group
}
```

#### Centralized Logging

Consider integrating with:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Loki** (Grafana Loki)
- **Cloud Logging** (AWS CloudWatch, Google Cloud Logging, Azure Monitor)

### Monitoring

#### Health Checks

Create a health check script:

```python
# health_check.py
import json
from pathlib import Path

def check_server_health():
    queue_file = Path("/tmp/deep_agent_queue.json")
    log_dir = Path("/tmp/deep_agent_logs")
    
    # Check if queue file exists and is readable
    if not queue_file.exists():
        return {"status": "error", "message": "Queue file not found"}
    
    # Check if log directory exists
    if not log_dir.exists():
        return {"status": "error", "message": "Log directory not found"}
    
    # Check recent logs for errors
    recent_logs = sorted(log_dir.glob("*.log"), key=lambda p: p.stat().st_mtime)
    if recent_logs:
        latest_log = recent_logs[-1]
        with open(latest_log) as f:
            log_data = json.load(f)
            if log_data.get("status") == "error":
                return {"status": "warning", "message": "Recent task failed"}
    
    return {"status": "healthy"}

if __name__ == "__main__":
    health = check_server_health()
    print(json.dumps(health))
    exit(0 if health["status"] == "healthy" else 1)
```

#### Metrics Collection

Consider adding metrics for:
- Tasks processed per hour
- Average task duration
- Error rate
- Sandbox creation time
- Queue depth
- API call counts

### Security Considerations

1. **Environment Variables**
   - Use secret management (AWS Secrets Manager, HashiCorp Vault)
   - Never commit `.env` files
   - Rotate API keys regularly

2. **File Permissions**
   ```bash
   chmod 600 .env
   chmod 755 /tmp/deep_agent_logs
   ```

3. **Network Security**
   - Use VPN for production deployments
   - Restrict outbound connections if possible
   - Monitor API usage

4. **Sandbox Isolation**
   - E2B sandboxes are already isolated
   - Set appropriate timeouts
   - Monitor resource usage

### Scaling Considerations

#### Horizontal Scaling

Run multiple server instances:

```bash
# Server 1
uv run deploy.py server

# Server 2 (different queue file)
DEEP_AGENT_QUEUE_FILE=/tmp/deep_agent_queue_2.json uv run deploy.py server
```

Use a load balancer or message queue (RabbitMQ, Redis Queue) for distribution.

#### Vertical Scaling

Increase resources:
- More CPU for parallel processing
- More RAM for larger sandboxes
- Faster disk for log I/O

### Backup Strategy

1. **Queue Backup**
   ```bash
   # Backup queue file
   cp /tmp/deep_agent_queue.json /backup/queue_$(date +%Y%m%d).json
   ```

2. **Log Archival**
   ```bash
   # Archive old logs
   tar -czf /backup/logs_$(date +%Y%m%d).tar.gz /tmp/deep_agent_logs/
   ```

3. **Configuration Backup**
   ```bash
   # Backup .env (encrypted)
   gpg -c .env > .env.backup.gpg
   ```

## Deployment Checklist

### Pre-Deployment

- [ ] All API keys obtained and tested
- [ ] Environment variables configured
- [ ] Dependencies installed (`uv sync`)
- [ ] Basic functionality tested
- [ ] Log directory created and permissions set
- [ ] Queue file location configured

### Deployment

- [ ] Process manager configured (systemd/supervisor/pm2)
- [ ] Service enabled and started
- [ ] Health check implemented
- [ ] Monitoring configured
- [ ] Log rotation configured
- [ ] Backup strategy implemented

### Post-Deployment

- [ ] Service status verified
- [ ] Test task submitted and processed
- [ ] Logs reviewed for errors
- [ ] Monitoring alerts configured
- [ ] Documentation updated
- [ ] Team notified of deployment

## Troubleshooting Deployment

### Server Won't Start

1. Check logs: `journalctl -u deep-agent` or `supervisorctl tail deep-agent`
2. Verify Python path: `which python` in service context
3. Check permissions: User has access to project directory
4. Verify environment variables are loaded

### Tasks Not Processing

1. Check queue file exists and is readable
2. Verify queue file format (valid JSON)
3. Check server is running: `ps aux | grep deploy.py`
4. Review logs for errors

### High Resource Usage

1. Reduce sandbox timeout
2. Implement task rate limiting
3. Add queue size limits
4. Monitor sandbox creation frequency

### API Rate Limits

1. Implement exponential backoff
2. Add rate limiting to task processing
3. Monitor API usage
4. Consider API key rotation

---

For more information, see:
- [README.md](README.md) - General usage and examples
- [SETUP.md](SETUP.md) - Detailed setup instructions

