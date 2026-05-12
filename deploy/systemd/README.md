# Systemd services

Install:

```bash
sudo cp deploy/systemd/alazab-rasa-*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now alazab-rasa-actions.service alazab-rasa-server.service alazab-rasa-watchdog.service
```

Check:

```bash
systemctl status alazab-rasa-actions alazab-rasa-server alazab-rasa-watchdog
journalctl -u alazab-rasa-server -f
```
