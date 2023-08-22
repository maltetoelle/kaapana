## Step-by-Step Development Environment Setup Instructions
1. Install the server dependencies as declared in the [official guide](https://kaapana.readthedocs.io/en/stable/installation_guide/server_installation.html#installation-of-server-dependencies).

	<div style="padding: 15px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 4px; color: #31708f; background-color: #d9edf7; border-color: #bce8f1;">
	If the DNS lookup fails, try changing the <a href="https://github.com/maltetoelle/kaapana/blob/dacd5a00f3733454a1a7d12a4cf35ef3feea8249/server-installation/server_installation.sh#L507">DNS Variable</a> to your local IP.
	</div>

2. Install Requirements as in [Build Guide](https://kaapana.readthedocs.io/en/stable/installation_guide/build.html).

3. Create a GitLab-Repo or a different container registry.
	
	<div style="padding: 15px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 4px; color: #31708f; background-color: #d9edf7; border-color: #bce8f1;">
	The "build without remote registry" is not working since <code>deploy_platform.sh</code> does not support an empty CONTAINER_REGISTRY_URL.
	</div>

4. Set the registry URL as [default_registry](https://github.com/maltetoelle/kaapana/blob/dacd5a00f3733454a1a7d12a4cf35ef3feea8249/build-scripts/build-config-template.yaml#L2) just as described in the [Build Guide](https://kaapana.readthedocs.io/en/stable/installation_guide/build.html).

5. Modify the Container and Helm Chart for Development (e.g. comment the [production part of the Dockerfile](https://github.com/maltetoelle/kaapana/blob/develop/services/base/landing-page-kaapana/docker/Dockerfile#L20-L26), uncomment the [development part](https://github.com/maltetoelle/kaapana/blob/develop/services/base/landing-page-kaapana/docker/Dockerfile#L15) and set the [dev_files](https://github.com/maltetoelle/kaapana/blob/dacd5a00f3733454a1a7d12a4cf35ef3feea8249/services/base/landing-page-kaapana/landing-page-kaapana-chart/values.yaml#L3) variable to your local [src](https://github.com/maltetoelle/kaapana/tree/develop/services/utils/base-landing-page/files/kaapana_app/src) path for Landingpage as declared in the [Readme](https://github.com/maltetoelle/kaapana/blob/develop/services/base/landing-page-kaapana/README.md)).

5. Run the [start_build.py](https://github.com/maltetoelle/kaapana/blob/develop/build-scripts/start_build.py) Script.

	<div style="padding: 15px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 4px; color: #31708f; background-color: #d9edf7; border-color: #bce8f1;">
	Add parameters -u and -p with your GitLab credentials to let the build run in the background (takes around 1h). Rebuilding already existing containers on the registry, the duration is significantly decreased.
	</div>

6. Deploy as in [Deployment Guide](https://kaapana.readthedocs.io/en/stable/installation_guide/deployment.html#deployment) using the generated ```build/deploy_platform.sh```.

	<div style="padding: 15px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 4px; color: #31708f; background-color: #d9edf7; border-color: #bce8f1;">
	Since this command is often used to start and stop the cluster, it is recommended to use the following commands:<br>
	- Start the cluster: <code>printf "&lt;local_url&gt;\n" | bash &lt;path_to_kaapana_folder&gt;/build/kaapana-admin-chart/deploy_platform.sh</code> where &lt;local_url&gt; is the URL with which to reach the website. <br>
	- Stop the cluster: <code>printf "&lt;delete_permanent_volumes&gt;\n" | bash &lt;path_to_kaapana_folder&gt;/build/kaapana-admin-chart/deploy_platform.sh —no-hooks</code> where &lt;delete_permanent_volumes&gt; is either yes or no.
	</div>

7. Watch cluster and pod logs using:
	- Cluster:
	
		```kubectl get pods -A -w -o wide```
	- Pod:
	
		```while :; do clear; kubectl logs -n services deploy/<pod_name>; sleep 2; done```
		
		where <pod_name> can be found in the ```kubectl get pods -A -w -o wide``` output (without the added random characters e.g. "landingpage")

	<div style="padding: 15px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 4px; color: #31708f; background-color: #d9edf7; border-color: #bce8f1;">
	Depending on your hardware, fully starting all pods can take 30 minutes. In some cases (like Landingpage) a host that only allows a small number of concurrently opened files can cause the pod to crash repeatedly before starting successfully.
	</div>

## Update a single pod (using the example pod: Landingpage)
- After changes to a local container, build the local container and push it to the registry e.g:

	```cd <path_to_kaapana_folder>/services/utils/base-landing-page && docker build -t local-only/base-landing-page:latest -f Dockerfile . && cd <path_to_kaapana_folder>/services/base/landing-page-kaapana/docker && docker build -t <registry_url>/landing-page-kaapana:<tag> . && docker push <registry_url>/landing-page-kaapana:<tag>```
	
	where &lt;tag&gt; is the tag of the current container on the registry which is to be updated.
- Force the pod to be recreated using the newly pushed container by changing its scaling:
	1. Decrease the replicas of the pod to 0:
	
		```kubectl scale deployment -n <namespace> <pod_name> --replicas=0```
		
		where &lt;namespace&gt; can be found as the first column in the ```kubectl get pods -A -w -o wide``` output.
	2. Increase the replicas of the pod to 1:
	
		```kubectl scale deployment -n <namespace> <pod_name> --replicas=1``` 