# Kubernetes deployment strategies

This folder contains example manifests for the deployment strategies requested in the assignment.

- `rolling/`: default Kubernetes rolling update deployment.
- `blue-green/`: separate blue and green environments with a service switch.
- `canary/`: stable and canary releases with NGINX ingress canary annotations.
- `shadow/`: primary production service plus mirrored traffic to a shadow release.
- `ab-testing/`: route traffic to version A or version B based on a request header.

Update the container image values before applying the manifests:

```bash
gouravj224/aceest-fitness-gym
```

Ingress-based examples assume the NGINX ingress controller is installed in Minikube.
