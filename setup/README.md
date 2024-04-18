# AI Lab Ubuntu setup

- [docker](https://docs.docker.com/engine/install/ubuntu/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- [microk8s](https://microk8s.io/)
  - `alias k='microk8s kubectl'`
  - `sudo microk8s.kubectl config view --raw > $HOME/.kube/config`
- [ArgoCD](https://argo-cd.readthedocs.io/en/stable/getting_started/)
  - [CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/)
  - `admin`: `BgAeLC71fQBubq5R` (from `argocd admin initial-password -n argocd`)
- [Nexus]
  - https://devopscube.com/setup-nexus-kubernetes/ ??
  - Better using helm?
- [BentoML Transformer Release]

# Laptop setup

## /etc/hosts

```
192.168.1.203   lima
```

## ~/.ssh/config

```
Host lima
  Hostname 192.168.1.203
  User pere
  LocalForward 9888 localhost:8080
  LocalForward 9889 localhost:10443
```

Then `ssh lima`

# AI Lab setup

## Expose all services in systemd

1. Create script `/usr/local/bin/expose.sh`
   ```bash
   #!/bin/bash
   mkdir /tmp/expose.service & \
   microk8s kubectl port-forward svc/argocd-server -n argocd 8080:443 > /tmp/expose.service/port-forward-argocd.log & \
   microk8s dashboard-proxy # https://localhost:10443 > /tmp/expose.service/dashboard-proxy.log &
   ```
2. `chmod +x expose.sh`
3. Create `/etc/systemd/system/expose.service`
   ```ini
   [Unit]
   Description=Expose services
   After=network.target

   [Service]
   ExecStart=/usr/local/bin/expose.sh
   Restart=always
   User=pere
   Type=Simple

   [Install]
   WantedBy=multi-user.target
   ```
4. Reload `systemd`:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable expose.service
    sudo systemctl start expose.service
    ```
