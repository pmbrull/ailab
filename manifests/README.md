# AI Lab Ubuntu setup

- [docker](https://docs.docker.com/engine/install/ubuntu/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- [microk8s](https://microk8s.io/)
  - `alias k='microk8s kubectl'`
  - `sudo microk8s.kubectl config view --raw > $HOME/.kube/config`
  - `microk8s kubectl create token default` to enter the dashboard
- [ArgoCD](https://argo-cd.readthedocs.io/en/stable/getting_started/)
  - [CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/)
  - `admin`: `BgAeLC71fQBubq5R` (from `argocd admin initial-password -n argocd` or ` k -n argocd get secrets/argocd-initial-admin-secret --template={{.data.password}} | base64 -d`)
  - Connect repo from the UI ([guide](https://www.webagesolutions.com/blog/deploy-an-application-using-argocd))
  - Install [AppSource](https://blog.argoproj.io/introducing-the-appsource-controller-for-argocd-52f21d28d643)
  - Install [guestbook example](https://argo-cd.readthedocs.io/en/stable/getting_started/) from GitHub `manifests/apps/guestbook`
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
  LocalForward 9888 localhost:8080   # argocd
  LocalForward 9889 localhost:10443  # dashboard-proxy
```

Then `ssh lima`

# AI Lab setup

## Expose all services in systemd

1. Create script `/usr/local/bin/expose.sh`
   ```bash
   #!/bin/bash
   mkdir -p /tmp/expose.service & \
   microk8s kubectl port-forward svc/argocd-server -n argocd 8080:443 > /tmp/expose.service/port-forward-argocd.log & \
   microk8s dashboard-proxy > /tmp/expose.service/dashboard-proxy.log &
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
